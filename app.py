import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv

from stt_whisper import transcribe_audio
from groq_agent import get_groq_response
from agents.orchestrator import AgentOrchestrator
from tts import synthesize_speech
from scheme_finder import find_schemes
from translator import translate_text
from messaging import send_sms_summary, send_whatsapp_summary

load_dotenv()

PORT = int(os.getenv("PORT", 5000))
app = Flask(__name__)
CORS(app)

@app.route("/voice", methods=["POST"])
def voice():
    """Initial Twilio webhook when call connects."""
    vr = VoiceResponse()

    # Prompt user to speak issue
    gather = Gather(input="speech", action="/process_speech", method="POST", timeout=5,
                    speechTimeout="auto", language="en-IN")
    gather.say("Namaste! Please briefly describe your issue after the beep.")
    vr.append(gather)
    # If no speech detected
    vr.redirect("/voice")
    return str(vr)

@app.route("/process_speech", methods=["POST"])
def process_speech():
    """Handle speech transcript from Twilio (native transcription) or fetch recording URL."""
    recording_url = request.values.get("RecordingUrl")
    transcript = request.values.get("SpeechResult")

    if not transcript and recording_url:
        # Fallback to Whisper transcription if Twilio didn't transcribe
        transcript = transcribe_audio(recording_url)

    if not transcript:
        vr = VoiceResponse()
        vr.say("Sorry, we could not hear you. Please call again.")
        return str(vr)

    # Process via LLM and scheme finder
    from_number = request.values.get("From")
    response_text = handle_conversation_logic(transcript, caller_number=from_number)

    # TTS generation
    audio_path = synthesize_speech(response_text)

    from store import log_call
    # Send SMS and WhatsApp summaries back to the caller
    from_number = request.values.get("From")
    summary_body = f"MSP Summary:\nYour issue: {transcript}\nResponse: {response_text}"
    if from_number:
        send_sms_summary(summary_body, from_number)
        send_whatsapp_summary(summary_body, from_number)
        # Store call log
        log_call({"from": from_number, "transcript": transcript, "response": response_text})

    vr = VoiceResponse()
    vr.play(audio_path)
    vr.say("Thank you for calling. Goodbye.")
    return str(vr)


orchestrator = AgentOrchestrator()

def handle_conversation_logic(user_text: str, caller_number: str | None = None) -> str:
    """Core logic to decide reply using Groq & scheme database."""
    # Translate to English for LLM if required (assume mixed languages supported)
        # Context passed to agents
    context = {"caller_number": caller_number}
    agent_reply = orchestrator.route(user_text, context)
    if agent_reply:
        return agent_reply

    # Fallback to generic LLM flow if orchestrator did not handle
    user_en = translate_text(user_text, target_language="en")
    llm_reply = get_groq_response(user_en)
    # Scheme suggestion on top (optional)
    schemes = find_schemes(user_en)
    if schemes:
        scheme_lines = [f"- {row['Scheme']}: {row['Description']} (Contact: {row['Contact']})" for row in schemes]
        llm_reply += "\n\nYou may also find these government schemes useful:\n" + "\n".join(scheme_lines)
    final_reply = translate_text(llm_reply, target_language="hi")
    return final_reply


@app.route("/admin/calls", methods=["GET"])
def admin_calls():
    """Return last 100 calls for dashboard purposes"""
    from store import get_last_calls
    return jsonify(get_last_calls()), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
