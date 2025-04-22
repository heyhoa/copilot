import os
import asyncio
from livekit import api
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_livekit_connection():
    # Get LiveKit connection details from environment
    ws_url = os.environ.get("LIVEKIT_HOST")  # WebSocket URL
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not all([ws_url, api_key, api_secret]):
        logger.error("Missing required LiveKit environment variables")
        return False

    try:
        # Convert WebSocket URL to HTTP URL for API calls
        http_url = ws_url.replace('wss://', 'https://')
        
        # Create room service client
        room_client = api.RoomServiceClient(
            host=http_url,
            api_key=api_key,
            api_secret=api_secret
        )

        # Create a test room
        room_name = "test-room-1"
        await room_client.create_room(
            name=room_name,
            empty_timeout=10  # Room will be deleted after 10 minutes if empty
        )
        logger.info(f"Created room: {room_name}")

        # Create token service client
        token_client = api.TokenServiceClient(api_key=api_key, api_secret=api_secret)

        # Generate participant token
        token = token_client.create_participant_token(
            room_name=room_name,
            participant_name="test-participant",
            participant_identity="test-identity",
            can_publish=True,
            can_subscribe=True
        )
        logger.info(f"Generated participant token: {token[:30]}...")

        # Clean up - delete the test room
        await room_client.delete_room(name=room_name)
        logger.info(f"Deleted room: {room_name}")

        return True

    except Exception as e:
        logger.error(f"Error during LiveKit connection test: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_livekit_connection())
    if success:
        logger.info("LiveKit connection test completed successfully")
    else:
        logger.error("LiveKit connection test failed") 