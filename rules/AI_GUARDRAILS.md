# AI Guardrails & Development Rules

## 1. Tone & Ethics
- AI must sound professional, polite, and human.
- Avoid speculation or casual banter.
- Use disclaimers if required by law ("This is an automated system...").

## 2. Data Privacy
- Only collect name, phone, address/unit, and reason for the call.
- Encrypt transcripts and redact sensitive data.
- Logs must be PII-safe.

## 3. Error Handling
- TTS fail = fallback message or sound
- STT fail = repeat question or escalate
- LLM fail = polite fallback + create manual ticket

## 4. Regulatory Compliance
- CCPA/GDPR handling (deletion requests, retention control)
- Call consent and recording laws per state

## 5. Monitoring & QA
- Audit transcripts monthly
- Use feedback to refine prompts and behavior
