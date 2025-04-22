# Project Milestones & Tasks

## 🎯 Milestone 1: Basic Infrastructure & Agent Setup
**Goal**: Establish the core Flask application and a LiveKit agent capable of connecting.

- [x] Initialize Flask project structure & config (`config.py`, `.env`).
- [x] Install core dependencies (`Flask`, `python-dotenv`, `livekit-agents`).
- [x] Create basic health check endpoint (`/`).
- [x] Configure LiveKit Cloud credentials (`.env` with `LIVEKIT_URL`, keys).
- [x] Create basic agent structure (`app/agents/voice_agent.py`).
- [x] Implement agent connection logic using `agents.cli.run_app` and `entrypoint` function.
- [x] Verify agent successfully registers with LiveKit Cloud (`python app/agents/voice_agent.py start`).

## 🎯 Milestone 2: Agent Interaction & Core Functionality (MVP)
**Goal**: Enable the agent to handle basic voice interactions, collect information, and log it.

- [ ] **Agent Connection & Basic Interaction Testing**
    - [ ] **Task 2.1:** Test agent interaction via LiveKit Agents Playground.
        - [ ] Run agent in `dev` mode: `python app/agents/voice_agent.py dev`.
        - [ ] Connect using the Playground URL from logs.
        - [ ] Verify connection and presence in Playground.
    - [ ] **Task 2.2:** Configure Basic Agent Plugins (STT/LLM/TTS).
        - [ ] Ensure necessary API keys (OpenAI, Cartesia) are in `.env`.
        - [ ] Install required plugin packages (`livekit-agents[openai,cartesia]`).
        - [ ] Uncomment and configure `stt`, `llm`, `tts` in `AgentSession` (`app/agents/voice_agent.py`).
        - [ ] Download required plugin models (`python app/agents/voice_agent.py download-files`).
    - [ ] **Task 2.3:** Test basic STT/LLM/TTS interaction via Playground.
        - [ ] Run agent in `dev` mode.
        - [ ] Speak to the agent via Playground.
        - [ ] Verify audio transcription (STT).
        - [ ] Verify basic response generation (LLM).
        - [ ] Verify spoken response (TTS).
    - [ ] **Task 2.4:** (Placeholder) Test agent interaction via simulated call.
        - [ ] *(Requires call routing setup - `app/routes/call_routes.py`)*.
- [ ] **Implement Core Agent Logic**
    - [ ] Define initial conversation flow (greeting, info gathering).
    - [ ] Implement basic FAQ handling.
    - [ ] Structure agent to collect caller details (name, phone, property, reason).
- [ ] **Implement Basic Ticket Creation/Logging**
    - [ ] Define simple structured format (JSON).
    - [ ] Log collected details + summary to file/console.
- [ ] **Basic Call Routing Setup (Flask)**
    - [ ] Create Flask routes (`app/routes/call_routes.py`) for call webhooks.
    - [ ] Implement logic to trigger the agent on incoming calls.
- [ ] **MVP Deployment Strategy**
    - [ ] Outline deployment steps (Docker, cloud service).

## 🎯 Milestone 3: Multi-Tenant System
**Goal**: Convert to a multi-tenant SaaS system.

- [ ] Implement User Authentication & Accounts.
- [ ] Create Client Dashboards.
- [ ] Implement Per-Client Agent Configuration.
- [ ] Integrate Database (User/Client Data, Tickets).

## 🎯 Milestone 4: Integrations
**Goal**: Connect the system with external platforms.

- [ ] Implement CRM Integration (e.g., Salesforce, HubSpot).
- [ ] Implement Property Management Software Integration (e.g., AppFolio).
- [ ] Develop API for external access.

## 🎯 Milestone 5: Premium Features
**Goal**: Enhance functionality and user experience.

- [ ] Implement Custom Voice Cloning (TTS).
- [ ] Add Multilingual Support.
- [ ] Develop Advanced Call Analytics & Reporting.
- [ ] Implement Sentiment Analysis.

## Current Focus: Milestone 2 - Agent Connection & Basic Interaction Testing
Next immediate tasks:
1.  **Task 2.1:** Test agent interaction via LiveKit Agents Playground.
2.  **Task 2.2:** Configure Basic Agent Plugins (STT/LLM/TTS).
3.  **Task 2.3:** Test basic STT/LLM/TTS interaction via Playground.

This structure uses the `🎯 Milestone X` format and `- [ ]` task lists as before, while incorporating the detailed steps for testing and MVP development. The "Current Focus" section highlights the immediate next steps from Task 2.1 onwards.