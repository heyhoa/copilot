# --- Remove Diagnostics ---
# Remove the diagnostic code added previously (lines 2-27 approx)
# --- End Remove Diagnostics ---

import asyncio
import logging
import os
from dotenv import load_dotenv
# Updated imports based on AgentSession pattern
from livekit.agents import JobContext, JobRequest, WorkerOptions, cli, AgentSession, Agent # Added AgentSession, Agent
# Removed VoiceAgent import
from livekit.agents.llm import LLM, ChatContext, ChatMessage, ChatRole # Keep LLM related imports if needed elsewhere, though Agent handles context now
from livekit.agents.stt import STT # Keep STT import if needed elsewhere
from livekit.agents.tts import TTS # Keep TTS import if needed elsewhere
from livekit.plugins import openai, cartesia

# Load environment variables from .env file at the start
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Removed SimpleVoiceAgent Class ---
# The logic is now handled directly in job_request_cb using AgentSession

# --- Updated Worker Entry Point ---
async def job_request_cb(job: JobContext):
    """Callback function to handle incoming job requests using AgentSession."""
    logger.info(f"Worker received job request for room: {job.room.name}, participant: {job.agent.identity}")

    # --- Initialize Plugins ---
    openai_key = os.getenv("OPENAI_API_KEY")
    cartesia_key = os.getenv("CARTESIA_API_KEY")

    if not openai_key:
        logger.error("OPENAI_API_KEY not found in environment variables. Agent cannot start.")
        # In a real scenario, you might want to signal an error back to LiveKit
        return
    if not cartesia_key:
        logger.error("CARTESIA_API_KEY not found in environment variables. Agent cannot start.")
        return

    # Initialize STT, LLM, TTS directly here
    try:
        stt = openai.STT(api_key=openai_key)
        llm = openai.LLM(api_key=openai_key)
        tts = cartesia.TTS(api_key=cartesia_key)
        logger.info("STT, LLM, TTS plugins initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize plugins: {e}", exc_info=True)
        # Signal failure appropriately
        return # Stop processing this job

    # --- Create Agent Session ---
    # Configure the session with the plugins
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        # Add other components like VAD if needed, e.g., from livekit.plugins import silero
        # vad=silero.VAD.load(),
    )
    logger.info("AgentSession created.")

    # --- Define Agent Logic ---
    # Create the Agent instance with instructions
    agent = Agent(
        instructions=(
            "You are a helpful voice assistant for a real estate management company. "
            "Your goal is to collect caller information (name, address, phone, reason for calling) "
            "and answer basic questions. Keep your responses concise and clear."
        ),
        # Define tools here if needed
        # tools=[...]
    )
    logger.info("Agent instance created with instructions.")

    # --- Start the Session ---
    # The AgentSession manages the interaction loop (STT -> LLM -> TTS)
    # Start the session, passing the room from the JobRequest and the agent logic
    logger.info(f"Starting AgentSession for job {job.id} in room {job.room.name}")
    try:
        await session.start(
            room=job.room, # Pass the room object from the job
            agent=agent,
            # Add RoomInputOptions if needed (e.g., noise cancellation)
            # from livekit.agents import RoomInputOptions
            # room_input_options=RoomInputOptions(...)
        )
        logger.info(f"AgentSession finished for job {job.id}")
    except Exception as e:
        logger.error(f"Error during AgentSession execution for job {job.id}: {e}", exc_info=True)
        # Handle session errors appropriately

# --- Removed the second SimpleVoiceAgent class definition ---


if __name__ == "__main__":
    # Load LiveKit connection details from environment variables
    livekit_host = os.getenv("LIVEKIT_HOST")
    livekit_api_key = os.getenv("LIVEKIT_API_KEY")
    livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")

    if not all([livekit_host, livekit_api_key, livekit_api_secret]):
        logger.error("LiveKit connection details (HOST, API_KEY, API_SECRET) not found in environment variables.")
        exit(1)

    logger.info(f"Starting LiveKit Agent Worker for host: {livekit_host}")

    # Configure WorkerOptions, explicitly passing connection details
    worker_options = WorkerOptions(
        entrypoint_fnc=job_request_cb,
        ws_url=livekit_host,         # Pass the host URL
        api_key=livekit_api_key,     # Pass the API key
        api_secret=livekit_api_secret # Pass the API secret
    )

    # Use the CLI helper to start the worker with the configured options
    # It will now call job_request_cb for each incoming job
    cli.run_app(worker_options)

    logger.info("LiveKit Agent Worker finished.") 