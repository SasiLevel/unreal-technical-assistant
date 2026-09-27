Read architecture.md and the existing Day 1 agent implementation.

Convert the existing Unreal Technical Assistant into a simple web application.

## TECH STACK:
- Python
- FastAPI
- OpenAI Python SDK
- HTML
- CSS
- Vanilla JavaScript

## ARCHITECTURE:
Browser
→ Chat UI
→ FastAPI backend
→ Unreal Technical Assistant
→ OpenAI Responses API
→ FastAPI
→ Chat UI

REQUIREMENTS:

## Backend:
- Keep OPENAI_API_KEY only in .env.
- Never expose the API key to frontend JavaScript.
- Create a POST /chat endpoint.
- Input should contain the user's message.
- Send that message to the existing Unreal Technical Assistant.
- Return the assistant response as JSON.
- Add basic error handling.

## Model Settings

- Model: gpt-4o-mini
- Max output tokens: 500

## Frontend:
- Create a clean dark chat interface.
- Title: Unreal Technical Assistant
- Chat history area
- User text input
- Send button(Every button should be in muted orange color)
- User messages and assistant messages should appear separately.
- Show "Cogitateing..."
       "Noodleing..."
       "Manefesting..."
      show this text word while waiting for the API,and that text should be change once 3 sec with little animation.
- Allow Enter to send the message.

## FILES:
- app.py
- templates/index.html
- static/style.css
- static/app.js
- requirements.txt

Do not modify .env.
Do not expose secrets.
Do not add authentication, databases, tools, memory, or multiple agents yet.

Keep the implementation beginner friendly.

After implementation:
1. Explain the files created.
2. Explain the request flow.
3. Give me the exact commands required to run it.