"""
Day 1 - Unreal Technical Assistant (web app)

FastAPI backend that exposes the existing Unreal Technical Assistant
(OpenAI Responses API) over a simple chat UI. See architecture.md for
the design this implements.
"""

import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI, OpenAIError
from pydantic import BaseModel
from starlette.requests import Request

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Create a .env file in this folder with a "
        "line like:\nOPENAI_API_KEY=sk-...\n"
    )

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"
MAX_OUTPUT_TOKENS = 500
SESSION_COOKIE = "session_id"

AGENT_INSTRUCTIONS = """You are the Unreal Technical Assistant, an expert helper for
Unreal Engine 5 technical problems.

Rules:
- Explain things clearly, in plain language.
- Give the likely cause(s) of the problem.
- Give practical, actionable troubleshooting tips.
- Do not invent settings, menus, nodes, or APIs that don't exist. If you are
  not sure something exists in UE5, say so instead of guessing.
- If you are missing information you need to help, ask the user for it.

When you answer, structure your response with these sections (skip a
section if it does not apply):
1. Likely Cause
2. Suggested Solution
3. Technical Tips
4. Steps
5. Additional Information Needed (if any)
"""

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory only (no database yet): maps a browser session to the last
# response id returned by the Responses API, so the next turn can chain
# onto it via previous_response_id.
conversations: dict[str, str] = {}


class ChatRequest(BaseModel):
    message: str


def get_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get(SESSION_COOKIE)
    if not session_id:
        session_id = uuid4().hex
        response.set_cookie(SESSION_COOKIE, session_id, httponly=True, samesite="lax")
    return session_id


@app.get("/")
async def index(request: Request):
    template_response = templates.TemplateResponse(request, "index.html")
    get_session_id(request, template_response)
    return template_response


@app.post("/chat")
async def chat(chat_request: ChatRequest, request: Request, response: Response):
    session_id = get_session_id(request, response)
    user_message = chat_request.message.strip()

    if not user_message:
        response.status_code = 400
        return {"error": "Message cannot be empty."}

    previous_response_id = conversations.get(session_id)

    try:
        create_kwargs = dict(
            model=MODEL,
            instructions=AGENT_INSTRUCTIONS,
            input=user_message,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
        if previous_response_id:
            create_kwargs["previous_response_id"] = previous_response_id

        api_response = client.responses.create(**create_kwargs)
        conversations[session_id] = api_response.id
        return {"reply": api_response.output_text}

    except OpenAIError as e:
        response.status_code = 502
        return {"error": f"OpenAI API error: {e}"}
    except Exception as e:
        response.status_code = 500
        return {"error": f"Unexpected error: {e}"}


@app.post("/new-chat")
async def new_chat(request: Request, response: Response):
    session_id = get_session_id(request, response)
    conversations.pop(session_id, None)
    return {"status": "ok"}
