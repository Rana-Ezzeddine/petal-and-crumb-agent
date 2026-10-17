---
title: Petal & Crumb Atelier
emoji: "🌸"
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 6.30.0
python_version: 3.13
app_file: app.py
pinned: false
license: mit
---

# Petal & Crumb Atelier — Agent-Powered Business Assistant

Flora represents a fictional botanical patisserie, flower boutique, and workshop studio. She answers grounded business questions, collects enquiries, and records feedback or unanswered questions through actual Gemini function calls. A saved enquiry is never a confirmed booking.

**Course:** EECE 503P/798S — C3: Introduction to Agents

**Student:** Rana Ezzeddine

## Demonstration and evidence

- **[Watch the continuous screen recording](demo/RanaEzzeddine_C3_Demo.mp4)** — approximately 2 minutes 20 seconds, recorded on October 17, 2026. Download the MP4 if GitHub does not display a player.
- **[Recording-session tool and reflection evidence](demo/recording_evidence.json)** — six actual audit entries from the recording's time window, including tool arguments/results and original/revised answers. Email addresses are redacted in this JSON.
- **[Main notebook](business_agent.ipynb)** — full implementation, labeled persona/instructions, router, schemas, demonstrations, test results, and recording evidence.
- **[Hosted live verification](demo/hosted_verification.json)** — seven live conversation turns plus an independent mixed request; all assertions passed after deployment.
- **[Validation record](VALIDATION.md)** — verification details and evidence provenance.
- **[Live Hugging Face Space](https://huggingface.co/spaces/RanaEzzeddine/petal-and-crumb-atelier)** — hosted coursework demonstration, updated on October 17, 2026 to the revised runtime shown in the recording.

The new recording shows workshop information, a remembered six-person calculation (**USD 228 = 6 × USD 38**), enquiry collection, an unanswered valet-service question, and pastry feedback. The structured audit file supplies the tool execution details. The older narrated walkthrough is retained as supplementary historical evidence, not as the primary recording.

## Run locally

Python 3.11+ is supported; this project was checked with Python 3.13.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Put your own Google AI Studio key in `.env` as `GEMINI_API_KEY`. The default model is `gemini-3.5-flash-lite`; `GEMINI_MODEL` can override it. Keep `ENABLE_REFLECTION=true` for the bonus demonstration. API availability and quota depend on the user's account.

```bash
python -m unittest discover -s tests -v
python app.py
```

Open the local address printed by Gradio. Expand **Coursework demo: router, tools, and reflection** to see the current turn's route, tool arguments/results, draft, and revised answer. It updates after each message and does not read other conversations' logs.

For the notebook, install `requirements-dev.txt`, open `business_agent.ipynb` in Jupyter or VS Code with that environment, and run from the repository root. The implementation cell matches `core_bot.py`. Uncomment `demo.launch()` to serve the notebook's interface. Without a local key, the live-evidence cell displays explicitly labeled historical captured results; it does not pretend to make fresh Gemini calls.

## Assignment checklist

| Required component | Location / evidence |
|---|---|
| Fictional business: name, mission, services, team, unique proposition | `me/business_summary.txt`, `me/about_business.pdf` |
| Clearly labeled persona and operational instructions | `PERSONA` and `INSTRUCTIONS` in the notebook and `core_bot.py` |
| General / lead / feedback router | `classify_intent`; heuristic rules plus a model fallback using history |
| Lead tool `(email, name, message)` | `record_customer_interest`; validates user-origin contacts and appends JSONL |
| Feedback / unanswered-question tool `(question)` | `record_feedback`; appends JSONL with a timestamp |
| MCP-style tool documentation | `TOOL_SCHEMAS` and notebook section 5; an MCP server is not claimed |
| Both PDF and TXT ground the model | Extracted source texts included in `SYSTEM_PROMPT` |
| Model-selected tool calls and returned results | `_run_tool_loop`; function responses are returned to Gemini |
| Short-term conversational memory | Gradio history normalized into Gemini conversation contents |
| Gradio interface | `app.py` and recorded local demonstration |
| Reflection bonus | `_reflect`, with original/revised replies and actual tool outcomes |
| Tests | 34 offline regression tests passed, including both tools and mixed intents |

The project uses Google's `google-genai` SDK in place of the legacy `google.generativeai` interface named in the brief. Tool execution remains explicit: the model selects the function, local code validates and runs it, and the real JSON result is returned before the next response.

## Important implementation details

- Name validation accepts components such as **An Nguyen** and **To Lam** without treating standalone placeholders as valid names. Only user messages supply contact fields.
- A complaint combined with an explicit order preserves both actions. A complaint containing only an email remains feedback, not a new order.
- Incomplete leads request the missing name/email; they are not recorded as feedback. Lead logging requires a name, email, and nonempty notes. Other order details can be collected during the enquiry.
- Duplicate identical calls are suppressed within a turn. Failed storage is not described as successful. Logs are local JSONL demonstration storage and can disappear on a hosted container restart.
- The assistant does not process payments, confirm reservations, implement a production CRM, or send human callbacks.
- `.env`, credentials, virtual environments, caches, and raw runtime logs are excluded from Git. The user-supplied recording is included as authorized; the accompanying structured evidence redacts email addresses.

## Deployment

For the revised runtime, use a **CPU Gradio Space** with `app.py` as the entrypoint. Upload `app.py`, `core_bot.py`, `requirements.txt`, the `me/` directory, and this README's configuration. Store `GEMINI_API_KEY` as a private Space secret. The optional `deployment/huggingface_app.py` wrapper now executes packaged source rather than downloading an older GitHub commit.

The existing Space was redeployed at Hugging Face commit `b6dd0ad18a9060e771f87716a7a258907a963a0d`, using the core from GitHub commit `6ea51be2ec264377aecbb59ee218581f1cec27ff`. Its `core_bot.py` matches this repository byte-for-byte. The account could not switch the existing Space from ZeroGPU to CPU, so the host retains the startup-only compatibility hook in `deployment/space_app.py`; chatbot requests do not call it or allocate a GPU. `deployment/README.space.md` preserves the deployed metadata. The earlier captured run remains in `demo/live_verification.json` as historical evidence. See `RECORDING_GUIDE.md` for a longer optional presentation sequence.
