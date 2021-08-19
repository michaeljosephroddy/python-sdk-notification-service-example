# Genesys Cloud Python SDK Notification Service

A simple notification service demonstrating how to listen to notification events from v2.routing.queues.{id}.users using the Python SDK

1. Create a notifications channel
`POST /api/v2/notifications/channels`
The following is an example response
You will use the `connectUri` and `id` in the next step

```
{
    "connectUri": "wss://streaming.mypurecloud.com/channels/streaming-0-fmtdmf8cdis7jh14udg5p89t6z",
    "id": "streaming-0-fmtdmf8cdis7jh14udg5p89t6z",
    "expires": "2020-08-12T12:41:54.707Z"
}
```

2. Subscribe to a topic
`POST /api/v2/notifications/channels/{channelId}/subscriptions`
Add one or more topics to the request body
The following is an example that adds `v2.routing.queues.{id}.users` topic to an existing subscriptions list

```
[
   {"id": "v2.routing.queues.fd1738bd-3b06-4b20-9dd0-37bd0248f00z.users"},
]
```

3. Open a web socket connection to the notifications channel by copying the `connectUri` into a web socket tool
(in our case Pythons "websockets" library)
The following is an example of connecting to a web socket tool

```
websockets.connect(connectUri)
```

Note: to continuously receive notifications you must keep the web socket connection open
Note: Each web socket connection is limited to 1000 topics.
