from PureCloudPlatformClientV2.rest import ApiException
import websockets
import asyncio
import PureCloudPlatformClientV2
import base64 
import requests
import sys
import os
import signal
import json


print("\n-----------------------------------------------------")
print("--- Genesys Cloud Python SDK Notification Service ---")
print("-----------------------------------------------------")


CLIENT_ID = os.environ["GENESYS_CLOUD_CLIENT_ID"]
CLIENT_SECRET = os.environ["GENESYS_CLOUD_CLIENT_SECRET"]
ENVIRONMENT = os.environ["GENESYS_CLOUD_ENVIRONMENT"] # eg. mypurecloud.com or mypurecloud.ie


def get_access_token():
    # Base64 encode the client ID and client secret
    authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")
    # Prepare request headers and request body
    request_headers = {
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    request_body = {
        "grant_type": "client_credentials"
    }
    response = requests.post(f"https://login.{ENVIRONMENT}/oauth/token", data=request_body, headers=request_headers)
    # Get JSON response body
    response_json = response.json()
    # extract access token from response body
    access_token = response_json["access_token"]
    return access_token


def find_queue_id(queue_name, routing_api_instance):
    try:
        response = routing_api_instance.get_routing_queues(name=queue_name)
        for entity in response.entities:
            if entity.name == queue_name: 
                print("\nHurray we found your queue!\n")
                print(f"Queue name = { entity.name }")
                print(f"Queue id = { entity.id }")
                return entity.id
    except ApiException as e:
        print("Exception when calling RoutingApi->get_routing_queues: %s\n" % e)
    
  
def create_notifications_channel(notifications_api_instance):
    try:
        print("\nCreating notifications channel..")
        # Create a new channel
        response = notifications_api_instance.post_notifications_channels()
        return response
    except ApiException as e:
        print("Exception when calling NotificationsApi->post_notifications_channels: %s\n" % e)


def subscribe_to_topic(queue_id, channel_id, notifications_api_instance):
    # the topic we want to subscribe to
    body = [
        {"id": f"v2.routing.queues.{queue_id}.users"}
    ]
    try:
        # Replace the current list of subscriptions with a new list.
        print(f"\nSubscribing to v2.routing.queues.{queue_id}.users")
        notifications_api_instance.put_notifications_channel_subscriptions(channel_id, body)
    except ApiException as e:
        print("\nException when calling NotificationsApi->post_notifications_channel_subscriptions: %s\n" % e)


async def listen(uri, queue_name):
    print("\nOpening web socket connection to notifications channel..")
    async with websockets.connect(uri) as websocket:
        print(f"\nConnected! You can now listen to notification events from {queue_name}")
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, loop.create_task, websocket.close())
        async for response in websocket:
            print()
            json_object = json.loads(response)
            json_formatted_str = json.dumps(json_object, indent=4)
            print(json_formatted_str)


def main():
    my_access_token = get_access_token()
    # Configure OAuth2 access token for authorization: PureCloud OAuth
    PureCloudPlatformClientV2.configuration.access_token = my_access_token
    # create an instance of the API class
    notifications_api_instance = PureCloudPlatformClientV2.NotificationsApi()
    routing_api_instance = PureCloudPlatformClientV2.RoutingApi()
    queue_name = input("\nEnter queue name: ")
    queue_id = find_queue_id(queue_name, routing_api_instance)
    response = create_notifications_channel(notifications_api_instance)
    # extract connect uri and channel id from response
    uri = response.connect_uri
    channel_id = response.id
    subscribe_to_topic(queue_id, channel_id, notifications_api_instance)
    asyncio.get_event_loop().run_until_complete(listen(uri, queue_name))


if __name__ == "__main__":
    main()