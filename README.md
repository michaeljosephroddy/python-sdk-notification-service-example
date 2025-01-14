# Genesys Cloud Python SDK: Notification Service

This guide explains how to use the Genesys Cloud Python SDK to create a notification service that listens to `v2.routing.queues.{id}.users` events.

## Prerequisites

Before you begin, ensure you have the **queue ID** for the desired queue.  

### How to Retrieve the Queue ID:
1. Make a `GET` request to the following endpoint, replacing `queue_name` with the desired queue name:  
   ```
   GET /api/v2/routing/queues?name=queue_name
   ```  
2. The response will contain details about the queue. Extract the `id` field, which represents the queue ID.

---

## Steps to Use the Notification Service

### 1. Create a Notifications Channel  
Make a `POST` request to create a notifications channel:  
```
POST /api/v2/notifications/channels
```  
The response will include a `connectUri` and `id`. You'll use these in subsequent steps.

**Example Response:**  
```json
{
    "connectUri": "wss://streaming.mypurecloud.com/channels/streaming-0-fmtdmf8cdis7jh14udg5p89t6z",
    "id": "streaming-0-fmtdmf8cdis7jh14udg5p89t6z",
    "expires": "2020-08-12T12:41:54.707Z"
}
```

### 2. Subscribe to a Topic  
Add the desired topics to the subscription list by making a `POST` request:  
```
POST /api/v2/notifications/channels/{channelId}/subscriptions
```  

**Request Body Example:**  
```json
[
    { "id": "v2.routing.queues.fd1738bd-3b06-4b20-9dd0-37bd0248f00z.users" }
]
```

### 3. Open a WebSocket Connection  
Use the `connectUri` from Step 1 to establish a WebSocket connection. You can use Python’s `websockets` library for this:  

**Example Code:**  
```python
import websockets

connect_uri = "wss://streaming.mypurecloud.com/channels/streaming-0-fmtdmf8cdis7jh14udg5p89t6z"
async with websockets.connect(connect_uri) as websocket:
    print("WebSocket connection established.")
```

### Notes:
- The WebSocket connection must remain open to continuously receive notifications.  
- Each WebSocket connection can subscribe to a maximum of 1,000 topics.

---

This documentation provides a streamlined approach for setting up and using the Genesys Cloud Notification Service with Python. Let me know if you need further clarification!
