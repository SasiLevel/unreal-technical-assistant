"""
Day 1 - Unreal Technical Assistant (single agent, no tools, no memory)

A simple terminal chatbot that uses the OpenAI Responses API to help
answer Unreal Engine 5 technical questions. See architecture.md for
the design this implements.
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are the Unreal Technical Assistant, an expert helper for
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


def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: OPENAI_API_KEY not found.\n"
            "Create a .env file in this folder with a line like:\n"
            "OPENAI_API_KEY=sk-...\n"
        )
        sys.exit(1)
    return api_key


def main() -> None:
    api_key = load_api_key()
    client = OpenAI(api_key=api_key)

    print("Unreal Technical Assistant (type 'exit' or 'quit' to stop)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = client.responses.create(
                model=MODEL,
                instructions=SYSTEM_PROMPT,
                input=user_input,
            )
            print(f"\nAssistant: {response.output_text}\n")

        except OpenAIError as e:
            print(f"\n[OpenAI API error] {e}\n")
        except Exception as e:
            print(f"\n[Unexpected error] {e}\n")


if __name__ == "__main__":
    main()
