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

Flora represents a fictional botanical patisserie, flower boutique, and workshop studio. She answers grounded questions, collects enquiries, and records feedback or unknown questions through Gemini function calls. An enquiry is never a confirmed booking.

**Live app:** https://huggingface.co/spaces/RanaEzzeddine/petal-and-crumb-atelier

**Demonstration video:** [Watch the narrated demonstration](demo/petal_and_crumb_demo.mp4)

**Main notebook:** [business_agent.ipynb](business_agent.ipynb)

## Run locally

Use Python 3.13; Python 3.11+ is supported by the source.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Put your own Google AI Studio key in `.env` as `GEMINI_API_KEY`. The default model is `gemini-3.5-flash-lite`; `GEMINI_MODEL` can override it. Set `ENABLE_REFLECTION=false` to disable the optional reflection pass. Neither `.env` nor runtime logs are committed.

The implementation uses Google's current `google-genai` SDK rather than the legacy `google.generativeai` interface named in the brief. It explicitly passes history and tools, dispatches model-selected function calls, and returns each real tool result to Gemini before generating the reply.

```bash
python -m unittest discover -s tests -v
python app.py
```

Open the Gradio address printed in the terminal. Expand **Coursework demo: router, tools, and reflection** to inspect the current turn's intent, successful/error tool results, draft, and revised answer. The panel never reads other conversations' logs.

To run the notebook, install `requirements-dev.txt` and open `business_agent.ipynb` in Jupyter or VS Code using this environment. Run cells from the repository root. Its implementation cell is identical to `core_bot.py`. It constructs the interface without blocking; uncomment `demo.launch()` to serve it from the notebook.

## Assignment requirements and evidence

| Requirement | Implementation / evidence |
|---|---|
| Fictional business name, mission, services, team, unique proposition | `me/about_business.pdf` and `me/business_summary.txt` |
| Separate persona and operational instructions | `PERSONA` and `INSTRUCTIONS` in module and notebook |
| General / lead / feedback router | `classify_intent`; uses normalized conversation history |
| Lead tool `(email, name, message)` | `record_customer_interest`; validates inputs and appends JSONL |
| Unknown-question / feedback tool `(question)` | `record_feedback`; exact question/feedback and timestamp |
| MCP-style tool documentation | `TOOL_SCHEMAS` plus notebook tool section |
| Grounding from PDF and TXT | Both extracted source texts are in `SYSTEM_PROMPT` |
| Gemini interaction and actual model tool calls | `_run_tool_loop`; tool responses are passed back to Gemini |
| Short-term memory | Gradio 6 text blocks and plain strings are normalized consistently |
| Gradio deployment | `app.py`, live Space, and video |
| Reflection bonus | `_reflect`; receives history, validated contacts, and actual tool outcomes; logs draft/revision |
| Hugging Face bonus | Live Space above |

## Suggested demonstration

Use only the fictional details below.

1. Ask **What is included in Glaze & Sip?**
2. Ask **How much would that experience cost for four people?** It should retain the reference and calculate **USD 152**.
3. Say **I would like to reserve that experience for four people next Saturday at 3 pm.**
4. Say **I am interested. My email is noor.demo@example.com.** It must request the missing name and must not record a lead yet.
5. Say **Noor Haddad, noor.demo@example.com**. Inspect the model-called lead tool and its successful result.
6. Ask **Do you offer valet service?** Inspect the feedback tool and an honest unknown-answer reply.
7. Say **Feedback: the pastries were stale.** Inspect the feedback record.
8. Compare draft and revised replies in the evidence panel.

`demo/verify_live.py` runs this sequence against the deployed Gemini app and asserts memory, calculation, validation, and successful model tool calls. Run `python demo/verify_live.py` to refresh `demo/live_verification.json`. The saved evidence uses fictional contacts only. It also checks a separate mixed order-and-delivery request and verifies conversation isolation. Offline tests simulate SDK responses for failure cases; they are separate from these real-model checks.

## Design details and limitations

- The three-way hybrid router handles explicit intent quickly and uses Gemini for ambiguous messages with the recent conversation. Mixed order-plus-delivery requests stay leads; the response model can also log the unsupported question.
- Contact fields are taken only from user messages. A missing name cannot be replaced with an interest phrase or the assistant's identity. Ambiguous names are requested explicitly.
- Model tool calls are dispatched locally. The model receives their JSON results before replying. Repeated identical calls within a turn reuse their first result.
- Reflection checks factual grounding, allergy warnings, missing details, price calculations, and claims of successful logging. A reflection outage preserves the original reply; failed writes are not reported as successes.
- Logs are coursework JSONL storage. They may be cleared by a hosted container restart. This application does not implement payments, confirmed reservations, automated human notifications, or a production CRM.
- The existing Space is configured as ZeroGPU. A startup compatibility hook is defined in the deployment bootstrap, but chatbot requests run on CPU and call Gemini directly; they never allocate a GPU. Its small `app.py` bootstrap loads the exact reviewed GitHub runtime pinned in `deployment/huggingface_app.py`, verifies SHA-256 hashes, and uses the Space's existing private API secret. The local app runs directly from the files in this repository.

This is a fictional course project. No real customer data or API credentials are included.
