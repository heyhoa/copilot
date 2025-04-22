# --- Remove Diagnostics ---
# Remove the diagnostic code added previously (lines 2-27 approx)
# --- End Remove Diagnostics ---

import asyncio
import logging
import os
import sys # Import sys for stdout flushing
from dotenv import load_dotenv
# Updated imports based on AgentSession pattern
from livekit.agents import JobContext, JobRequest, WorkerOptions, cli, AgentSession, Agent # Added AgentSession, Agent
# Removed VoiceAgent import
from livekit.agents.llm import LLM, ChatContext, ChatMessage, ChatRole # Keep LLM related imports if needed elsewhere, though Agent handles context now
from livekit.agents.stt import STT # Keep STT import if needed elsewhere
from livekit.agents.tts import TTS # Keep TTS import if needed elsewhere
from livekit.plugins import openai, cartesia
from livekit.protocol.agent import JobType # Import JobType enum

# Load environment variables from .env file at the start
load_dotenv()

# Configure logging
# Set logging level to DEBUG to see more detailed logs from the framework
logging.basicConfig(
    level=logging.DEBUG, # Changed to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout), # Log to standard output
        # You can add other handlers like logging.FileHandler("agent.log") if needed
    ]
)
logger = logging.getLogger(__name__) # Get a logger for this module

# Add this after the imports to inspect the JobType enum
logger.info(f"Available JobType values: {[name for name in JobType.values()]}")

class WorkerType:
    def __init__(self, value):
        self.value = value

# Define the agent logic within a class inheriting from Agent
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__()
        # Initialization logic for the agent, if any
        # Example: Load models, set up state, etc.
        logger.info("MyVoiceAgent initialized.")
        # Setup event listeners if needed, e.g., self.on("track_published", self._handle_track)

    async def process_request(self, session: AgentSession):
        """
        This method is called for each new agent session (job).
        Implement the core agent logic here.
        """
        logger.info(f"Agent processing request for session: {session.id}") # Use session.id

        # Example: Set up STT, LLM, TTS for the session
        # These would typically be configured based on environment variables or job metadata
        stt = openai.STT() # Example STT
        llm = openai.LLM() # Example LLM
        tts = cartesia.TTS() # Example TTS

        # Assign plugins to the session
        session.stt = stt
        session.llm = llm
        session.tts = tts

        # Add initial chat context if needed
        chat_ctx = ChatContext()
        chat_ctx.messages.append(ChatMessage(role=ChatRole.SYSTEM, text="You are a helpful voice assistant."))
        session.chat_context = chat_ctx # Assign the context to the session

        try:
            logger.info("Starting agent session...")
            # The AgentSession manages the connection and interaction loop
            # You can add custom logic by listening to session events or overriding methods
            # For a basic assistant, starting the session might be enough if using default handlers
            await session.start()

            # If you need more control, you might interact with session components directly:
            # async for transcript in session.stt:
            #     logger.info(f"Received transcript: {transcript.text}")
            #     # Process transcript, maybe call LLM
            #     async for chunk in session.llm.chat(session.chat_context):
            #         await session.say(chunk) # Use session.say for TTS output

            logger.info(f"Agent session {session.id} finished.")

        except Exception as e:
            logger.error(f"Error during agent session {session.id}: {e}", exc_info=True)
        finally:
            logger.info(f"Cleaning up session {session.id}")
            # AgentSession handles cleanup like closing connections automatically


# Define the callback function for handling job requests
async def job_request_cb(job: JobContext):
    """
    This function is called by the LiveKit Agent Framework when a new job is assigned to this worker.
    """
    # Access job ID correctly via job.job.id
    logger.info(f"Worker received job request for Job ID: {job.job.id}, Room: {job.room.name}")

    # Create an instance of your agent logic
    agent = MyVoiceAgent()

    # Create an AgentSession - this handles the connection and lifecycle
    # The session needs the JobContext to know which room/participant to act as
    session = AgentSession(job_context=job) # Pass the job context here

    logger.info(f"Created AgentSession with ID: {session.id}")

    # Start the agent's processing logic for this session
    # The AgentSession will connect to the room internally
    await agent.process_request(session)

    logger.info(f"Finished processing job request for Job ID: {job.job.id}")


# Main entry point for the agent worker
if __name__ == "__main__":
    # Get LiveKit connection details from environment variables
    livekit_url = os.environ.get("LIVEKIT_URL")
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET")

    if not all([livekit_url, livekit_api_key, livekit_api_secret]):
        logger.error("LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET must be set")
        sys.exit(1)

    logger.info(f"Starting LiveKit Agent Worker for host: {livekit_url}")

    # Configure worker options
    worker_options = WorkerOptions(
        entrypoint_fnc=job_request_cb,
        worker_type=WorkerType(0),  # Wrap the integer in our custom class
    )

    # Use the CLI helper to start the worker with the configured options
    cli.run_app(worker_options)

    logger.info("LiveKit Agent Worker finished.") 