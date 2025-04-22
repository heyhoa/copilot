# --- Remove Diagnostics ---
# Remove the diagnostic code added previously (lines 2-27 approx)
# --- End Remove Diagnostics ---

import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Load environment variables *first*
load_dotenv()

# Import LiveKit Agents components AFTER load_dotenv
from livekit import agents # Use 'agents' namespace as per docs
from livekit.agents import AgentSession, Agent, JobContext # Import specific classes needed
# Import plugins if you use them (adjust based on your actual usage)
# from livekit.plugins import openai, cartesia, deepgram, silero, noise_cancellation
# from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# Define your Agent class (Simplified based on docs example)
class MyAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")
        logger.info("MyAssistant Agent initialized.")
        # Add any specific initialization for your agent here

    # You can override methods like process_speech, process_text if needed
    # async def process_speech(self, source, stream): ...
    # async def process_text(self, text): ...


# Define the entrypoint function as shown in the documentation
async def entrypoint(ctx: JobContext):
    """
    This function is called by the LiveKit Agent Framework for each new job.
    It sets up and runs the AgentSession.
    """
    logger.info(f"Agent entrypoint called for job: {ctx.job.id}, room: {ctx.room.name}")

    # Example session setup (Adapt plugins based on your .env keys and installed packages)
    # Ensure you have the necessary API keys in .env for the plugins you use.
    session = AgentSession(
        # Example STT (Requires DEEPGRAM_API_KEY in .env and livekit-agents[deepgram])
        # stt=deepgram.STT(model="nova-2", language="en"),

        # Example LLM (Requires OPENAI_API_KEY in .env and livekit-agents[openai])
        # llm=openai.LLM(model="gpt-4o-mini"),

        # Example TTS (Requires CARTESIA_API_KEY in .env and livekit-agents[cartesia])
        # tts=cartesia.TTS(),

        # Example VAD (Requires livekit-agents[silero] and downloaded models)
        # vad=silero.VAD.load(),

        # Example Turn Detection (Requires livekit-agents[turn-detector] and downloaded models)
        # turn_detection=MultilingualModel(),
    )
    logger.info(f"AgentSession created for job {ctx.job.id}")

    # Connect the agent to the room specified by the job context
    # This replaces the need for job_request_cb creating the session
    await ctx.connect()
    logger.info(f"Agent connected to room: {ctx.room.name}")

    # Start the session processing loop
    # Pass the agent instance and any room input options
    await session.start(
        room=ctx.room,
        agent=MyAssistant(), # Pass an instance of your agent class
        # Example Room Input Options (Requires livekit-plugins-noise-cancellation and downloaded models)
        # room_input_options=agents.RoomInputOptions(
        #     noise_cancellation=noise_cancellation.BVC(),
        # ),
    )
    logger.info(f"AgentSession started for job {ctx.job.id}")

    # Optional: Send an initial greeting or message
    # await session.say("Hello! How can I help you today?") # Requires TTS to be configured

    # The session runs until the job is complete or an error occurs.
    # You don't need the asyncio.sleep(30) here as session.start() handles the lifecycle.
    logger.info(f"Agent entrypoint finished for job {ctx.job.id}")


# Main entry point for the agent worker
if __name__ == "__main__":
    # Check required environment variables (optional but recommended)
    livekit_url = os.environ.get("LIVEKIT_URL")
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not all([livekit_url, livekit_api_key, livekit_api_secret]):
        logger.error("LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set in environment variables.")
        sys.exit(1)

    logger.info(f"Attempting to start LiveKit Agent Worker.")
    logger.info(f"  LIVEKIT_URL: {livekit_url}")
    logger.info(f"  LIVEKIT_AGENT_HTTP_HOST: {os.environ.get('LIVEKIT_AGENT_HTTP_HOST', 'Default')}")
    logger.info(f"  LIVEKIT_AGENT_HTTP_PORT: {os.environ.get('LIVEKIT_AGENT_HTTP_PORT', 'Default (8081)')}")

    # Use the CLI helper as shown in the documentation
    # Pass only the entrypoint function to WorkerOptions
    # cli.run_app should read LIVEKIT_URL, keys, and HTTP settings from ENV VARS
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

    # This line might not be reached if run_app blocks indefinitely
    logger.info("LiveKit Agent Worker finished.") 