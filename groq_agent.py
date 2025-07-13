"""Wrapper around Groq chat completion API."""
import os
from groq import Groq
from typing import List, Dict

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are MSP, a helpful phone assistant for Indian citizens. "
    "Provide concise, polite answers. If user asks about government schemes, suggest relevant ones." 
)

def get_groq_response(text: str, conversation: List[Dict[str, str]] | None = None) -> str:
    """Send user text and get assistant reply. conversation holds previous messages."""
    if client is None:
        raise RuntimeError("GROQ_API_KEY not configured")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if conversation:
        messages.extend(conversation)
    messages.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0.2,
    )
    return completion.choices[0].message.content.strip()
