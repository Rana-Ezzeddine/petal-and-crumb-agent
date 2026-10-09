# Petal & Crumb Atelier Agent

This repository is a complete solution for the “Agent-Powered Business Assistant” assignment. Petal & Crumb Atelier is a fictional botanical patisserie, flower boutique, and creative studio. The implementation includes every required component plus the optional reflection step.

## Demonstration video

[Watch the narrated live-interface demonstration](demo/petal_and_crumb_demo.mp4)

## Submission contents

- `me/about_business.pdf` - polished three-page business profile
- `me/business_summary.txt` - compact factual grounding source
- `business_agent.ipynb` - self-contained, fully executed notebook with saved model and tool outputs
- `core_bot.py` - persona, instructions, router, tools, model loop, and reflection
- `app.py` - Gradio ChatInterface entry point
- `.env.example` - safe API configuration template
- `requirements.txt` - required Python libraries
- `tests/test_core_bot.py` - offline checks for all router branches and both tools
- `GRADING_AUDIT.md` - requirement-by-requirement quality review
- `demo/petal_and_crumb_demo.mp4` - narrated 1280x720 demonstration captured from the running Gradio app
- `logs/` - local JSONL lead, feedback, and reflection logs created at runtime

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Create a free-tier Gemini API key at <https://aistudio.google.com/app/apikey>, open `.env`, and replace `your_key_here` with the key. The default model is `gemini-3.5-flash-lite`. Then run:

```bash
python3 -m unittest discover -s tests -v
python3 app.py
```

Open the local address printed by Gradio, normally <http://127.0.0.1:7860>.

The router and direct tool demonstrations in the notebook run without an API key. Live Gemini model and reflection cells require a key. The committed notebook contains successful saved demonstrations using fictional data. `.env` and runtime logs are excluded by `.gitignore`.

## Agent design

Flora is an elegant, lightly botanical digital hostess. Persona and operational instructions are deliberately separate. A deterministic router classifies each message as `general_question`, `lead_collection`, or `feedback_unanswered`. It distinguishes questions about an offering from actual transaction intent and gives complaints priority over lead keywords. That route is passed to the model along with recent conversation history, both required business sources, and two MCP-style tool schemas.

The tool loop executes `record_customer_interest` only when a name and email are available. Explicit feedback and unanswered questions use `record_feedback`. The model receives each tool result before composing its reply. A second reflection pass checks the draft for invented facts, missed lead details, allergy risks, tone, and excessive length, then logs the original and revised replies. The complete prompt includes the text summary and text extracted from all three pages of the PDF profile.

## Suggested presentation sequence

1. Ask: “What is included in Glaze & Sip?”
2. Say: “I want to reserve it for four people.”
3. Provide fictional contact details, a date, and notes; show `logs/leads.jsonl`.
4. Ask: “Can you deliver today to my neighborhood?”; show `logs/feedback.jsonl`.
5. Show the printed router label and `logs/reflection.jsonl`.

This project is fictional and intended only for coursework demonstration. It is deployment-ready but has not been deployed or submitted.
