# Real Estate Voice Agent

An AI-powered voice agent for handling real estate management calls. This system automatically answers calls, collects caller information, and creates structured tickets for follow-up.

## Features

- Instant call answering (no hold times)
- Natural-sounding AI voice interaction
- Automated information collection:
  - Caller name
  - Phone number
  - Email (optional)
  - Property/unit address
  - Reason for calling
- Basic FAQ handling
- Structured ticket creation for callbacks
- Secure data handling and PII protection

## Tech Stack

- **Backend**: Flask/Python
- **Database**: SQLAlchemy with SQLite/PostgreSQL
- **Voice Processing**:
  - Speech-to-Text: AssemblyAI/Whisper
  - Text-to-Speech: ElevenLabs/Cartesia
  - LLM: OpenAI GPT/Ollama
- **Telephony**: LiveKit/Twilio

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. Initialize database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## API Endpoints

### Calls
- `POST /api/calls/incoming` - Handle incoming call webhook
- `POST /api/calls/stream` - Process audio stream

### Tickets
- `POST /api/tickets/` - Create new support ticket
- `GET /api/tickets/` - List all tickets

## Project Structure

```
real_estate_voice_agent/
├── app/
│   ├── routes/        # API endpoints
│   ├── models/        # Database models
│   ├── services/      # External service integrations
│   └── utils/         # Helper functions
├── config.py          # Configuration settings
└── run.py            # Application entry point
```

## Development

1. Follow Flask best practices and PEP 8 style guide
2. Write tests for new features
3. Update requirements.txt when adding dependencies
4. Keep sensitive data out of version control

## License

MIT License

## Contact

For support or inquiries, please open an issue on GitHub.
