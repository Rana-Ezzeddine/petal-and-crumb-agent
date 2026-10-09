# Petal & Crumb Atelier Agent

This repository is a complete solution for the “Agent-Powered Business Assistant” assignment. Petal & Crumb Atelier is a fictional botanical patisserie, flower boutique, and creative studio. The implementation includes every required component plus the optional reflection step.

## Demonstration video

[Watch the narrated Petal & Crumb functionality demo](demo/petal_and_crumb_demo.mp4)

## Submission contents

- `me/about_business.pdf` - polished two-page business profile
- `me/business_summary.txt` - compact factual grounding source
- `business_agent.ipynb` - explained, runnable notebook with visible router output
- `core_bot.py` - persona, instructions, router, tools, model loop, and reflection
- `app.py` - Gradio ChatInterface entry point
- `.env.example` - safe API configuration template
- `requirements.txt` - required Python libraries
- `tests/test_core_bot.py` - offline checks for all router branches and both tools
- `GRADING_AUDIT.md` - requirement-by-requirement quality review
- `demo/petal_and_crumb_demo.mp4` - narrated functionality demonstration
- `logs/` - local JSONL lead, feedback, and reflection logs created at runtime

## Run locally

1. Create a virtual environment and install `requirements.txt`.
2. Create a free-tier Gemini API key at <https://aistudio.google.com/app/apikey>, copy `.env.example` to `.env`, and insert that key. The default model is `gemini-3.5-flash-lite`.
3. Run `python -m unittest discover -s tests -v` for the offline checks.
4. Run `python app.py` to launch the chatbot.

The router and direct tool demonstrations in the notebook run without an API key. Live Gemini model and reflection cells require a key. `.env` and runtime logs are excluded by `.gitignore`.

## Agent design

Flora is an elegant, lightly botanical digital hostess. Persona and operational instructions are deliberately separate. A deterministic router classifies each message as `general_question`, `lead_collection`, or `feedback_unanswered`. That route is passed to the model along with recent conversation history, verified business context, and two MCP-style tool schemas.

The tool loop executes `record_customer_interest` only when a name and email are available. Explicit feedback and unanswered questions use `record_feedback`. The model receives each tool result before composing its reply. A second reflection pass checks the draft for invented facts, missed lead details, allergy risks, tone, and excessive length, then logs the original and revised replies.

## Suggested presentation sequence

1. Ask: “What is included in Glaze & Sip?”
2. Say: “I want to reserve it for four people.”
3. Provide fictional contact details, a date, and notes; show `logs/leads.jsonl`.
4. Ask: “Can you deliver today to my neighborhood?”; show `logs/feedback.jsonl`.
5. Show the printed router label and `logs/reflection.jsonl`.

This project is fictional and intended only for coursework demonstration. It is deployment-ready but has not been deployed or submitted.
