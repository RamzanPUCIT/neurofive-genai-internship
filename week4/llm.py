"""
llm.py — the only file that talks to the API.

Both agents call this one function. That means the two agents differ ONLY in
their system prompt and their responsibilities, which is the whole point of
the exercise.

Reads from .env:
    GROQ_API_KEY=gsk_...
    MODEL=llama-3.3-70b-versatile
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")


def call_llm(system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 2000, json_mode: bool = False) -> str:
    """Send one system prompt + one user message, get back plain text.

    json_mode=True forces the model to return valid JSON. The Editor agent uses
    this so its critique comes back as data instead of prose.
    """
    kwargs = {
        "model": MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


# Quick connection test:  python llm.py
if __name__ == "__main__":
    print(f"Model: {MODEL}")
    print(call_llm(
        system="You reply in exactly one short sentence.",
        user="Say hello and confirm the connection works.",
    ))
