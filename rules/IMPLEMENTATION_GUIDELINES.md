# Project Implementation Guidelines

## 1. Overview
- **Project Name:** Real Estate Management Voice Agent
- **Objective:** Develop an AI-driven voice agent to handle inbound calls, gather caller info, answer FAQs, and produce structured callback tickets.

## 2. Tools Used (Based on Reference Project)
- **Telephony:** LiveKit (Twilio/Telnyx optional)
- **Streaming STT:** AssemblyAI, Deepgram, Whisper
- **TTS:** Cartesia, ElevenLabs
- **LLM:** OpenAI GPT (or Ollama with Gemma)
- **Backend:** Flask API
- **Storage:** SQLite/PostgreSQL or CSV for MVP

## 3. Architecture Summary
- Real-time audio streaming (LiveKit)
- Streaming transcription → LLM for logic → TTS playback
- Ticket creation stored as JSON (can be upgraded later)

## 4. Milestones
- A: Local real-time streaming
- B: End-to-end info capture + ticket
- C: MVP deployment (single tenant)
- D: Multi-tenant & dashboard

## 5. Team Roles
- Project Lead, Telephony Engineer, AI/ML Dev, Backend Dev, QA
