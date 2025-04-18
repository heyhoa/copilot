# LiveKit Python SDKs

LiveKit provides two Python packages:

## 1. Server API SDK (livekit-api)
For server-side operations like managing rooms and generating tokens.

### Installation
```bash
pip install livekit-api
```

### Usage
```python
from livekit import api

# Initialize API client
api_client = api.LiveKitAPI(
    host='https://my-livekit-host.com',
    api_key='api_key',
    api_secret='secret'
)

# Create a room
room = api_client.create_room("my-room")

# Generate token
token = api_client.create_token(
    room="my-room",
    identity="user123",
    can_publish=True
)
```

## 2. Real-time Client SDK (livekit)
For real-time features like audio/video streaming.

### Installation
```bash
pip install livekit
```

[Source: https://github.com/livekit/python-sdks]

# LiveKit Voice Agent Integration

## Official Recipes
LiveKit provides several relevant examples for voice agent implementation:

### Voice AI Quickstart
Basic setup for voice AI agent with real-time audio streaming.
[Source: https://docs.livekit.io/recipes/]

### Key Components
1. Room Creation & Token Generation (Server-side)
```python
from livekit import api

# Initialize API client
api_client = api.LiveKitAPI(
    host='wss://my-livekit-host.cloud',  # WebSocket URL
    api_key=LIVEKIT_API_KEY,
    api_secret=LIVEKIT_API_SECRET
)

# Create room
room = api_client.create_room("call_123")

# Generate participant token
token = api_client.create_token(
    room="call_123",
    identity="agent",
    can_publish=True,
    can_subscribe=True
)
```

2. Audio Stream Handling
```python
from livekit.rtc import Room, RoomOptions

# Connect to room
room = Room(
    url=LIVEKIT_URL,
    token=token
)

# Handle audio streams
@room.on("track_subscribed")
async def on_track_subscribed(track, publication, participant):
    if track.kind == "audio":
        # Process audio track
        pass
```

[Source: https://docs.livekit.io/recipes/voice-ai-quickstart/] 