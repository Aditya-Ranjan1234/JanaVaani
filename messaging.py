"""Messaging utilities for SMS and WhatsApp via Twilio."""
import os
from typing import Optional
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Your Twilio number

if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN):
    client = None
else:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def _send_message(body: str, to: str, channel: str = "sms") -> Optional[str]:
    """Generic send. channel: 'sms' or 'whatsapp'. Returns message SID or None."""
    if client is None:
        return None
    if channel == "whatsapp":
        from_number = f"whatsapp:{TWILIO_PHONE_NUMBER}"
        to_number = f"whatsapp:{to}"
    else:
        from_number = TWILIO_PHONE_NUMBER
        to_number = to
    msg = client.messages.create(body=body, from_=from_number, to=to_number)
    return msg.sid


def send_sms_summary(body: str, to: str):
    return _send_message(body, to, channel="sms")


def send_whatsapp_summary(body: str, to: str):
    return _send_message(body, to, channel="whatsapp")
