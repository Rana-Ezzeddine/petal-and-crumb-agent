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

# Petal & Crumb Atelier

Flora is a fictional botanical patisserie, flower boutique, and workshop assistant for EECE 503P/798S C3.

**Student:** Rana Ezzeddine

**[Full source, notebook, tests, and demonstration video](https://github.com/Rana-Ezzeddine/petal-and-crumb-agent)**

This Space runs the revised source from GitHub commit `6ea51be2ec264377aecbb59ee218581f1cec27ff` on the existing free ZeroGPU hardware. A startup-only ZeroGPU compatibility hook is retained; chat requests never allocate a GPU. Gemini requests use the existing private `GEMINI_API_KEY` Space secret.

Try asking what Glaze & Sip includes, then ask for the cost for four people. A booking enquiry requests a name and email before the model calls `record_customer_interest`. Unknown business questions and feedback use `record_feedback`. Expand **Coursework demo: router, tools, and reflection** to inspect model-selected tools, actual results, and original/revised replies.

Use fictional contacts only. Saved enquiries are not confirmed reservations. Local JSONL records can disappear when the Space restarts; this coursework demo does not process payments or send callbacks.
