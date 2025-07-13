# 🛠️ JanaVaani – Setup Guide

This guide walks you through installing, configuring and running the multi-agent voice assistant on your local machine or a cloud host.

---

## 1. Prerequisites

1. **Python 3.10+** (recommended 64-bit)
2. **Git**
3. A **Twilio** account with:
   - Verified phone number
   - Programmable Voice/SMS capabilities
4. (Optional) **ngrok** or Cloudflare Tunnel for exposing localhost to the internet during development.

---

## 2. Clone & Install

```bash
git clone https://github.com/Aditya-Ranjan1234/JanaVaani.git
cd JanaVaani
python -m venv .venv
.venv\Scripts\activate        # PowerShell (Windows)
# or: source .venv/bin/activate on Linux/macOS
pip install -r requirements.txt
```

> ℹ️  Installing `openai-whisper` will also download the Whisper model on first run. For faster CPU-only inference you can set:
> ```bash
> WHISPER_MODEL=base
> ```

---

## 3. Environment Variables

Create a `.env` file in the project root (copy from `.env.example`) and fill:

| Variable | Purpose |
| -------- | ------- |
| `TWILIO_ACCOUNT_SID` | Your Twilio project SID |
| `TWILIO_AUTH_TOKEN`  | Auth token from Twilio console |
| `TWILIO_PHONE_NUMBER`| The purchased/verified voice number (+91… or +1…) |
| `GROQ_API_KEY`       | [Groq](https://console.groq.com/) API key for LLM inference |
| `WHISPER_MODEL`      | (Optional) Whisper model name: `base`, `small`, `medium` |
| `PORT`               | Flask port (default `5000`) |

Save & reload your shell to apply.

---

## 4. Run Locally

```bash
python app.py
```

Expose your port:

```bash
ngrok http 5000  # copy the "Forwarding" HTTPS URL
```

In Twilio Console → **Phone Numbers → Voice & Fax → A Call Comes In** set:

```
https://<your-ngrok-id>.ngrok-free.app/voice
```

Call the number – you should hear the prompt and interact with the agents.

---

## 5. Agent Directory Structure

```
agents/
├── base.py          # Abstract class
├── orchestrator.py  # Routes incoming text to domain agent
├── agriculture/     # Recommends farming schemes
├── civic/           # Handles civic complaints
└── emergency/       # Connects to emergency services
```

---

## 6. Extending / Customising

1. **Schemes Database** – Edit `data/schemes.csv` to add more keywords and schemes.
2. **Languages** – Improve `translator.py` to add more language pairs.
3. **Civic APIs** – Integrate real endpoints inside `agents/civic/__init__.py` (currently prints a placeholder).
4. **Emergency Outbound Call** – Use Twilio’s `Calls.create()` API inside `agents/emergency/__init__.py` for auto-dialling services.

---

## 7. Deployment

Free hosting options:

| Platform | Notes |
| -------- | ----- |
| **Render** | One-click deploy; add environment variables in dashboard |
| **Railway** | Simple CI/CD + Postgres/Redis add-ons |
| **Fly.io**  | Global edge deployments |

On deployment, point Twilio webhooks to the public URL `/voice`.

---

## 8. Troubleshooting

| Issue | Fix |
| ----- | ---- |
| Whisper installation slow | Use a smaller model (`WHISPER_MODEL=base`) or preload weights |
| `EADDRINUSE` port in use | Change `PORT` in `.env` or stop other process |
| SMS not sending | Ensure your Twilio number & destination are in same geo-region during trial |

---

## 9. License

This project is MIT-licensed. See `LICENSE` for details.

---

Happy hacking! 🎉
