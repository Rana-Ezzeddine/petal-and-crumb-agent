# Verification record

Verified on 2026-10-17T08:44:53.657379+00:00 using Python 3.13.

- All 25 offline regression tests passed, including user-origin contact validation, Gradio 6 history, tool-result echoing, failed storage, service outages, duplicate-call handling, and truthful enquiry confirmations.
- All 8 notebook code cells executed successfully with saved outputs. The implementation cell matches `core_bot.py` exactly. The notebook explicitly labels its saved live-model evidence.
- Seven consecutive messages to the deployed Gemini app passed: grounded workshop answer, remembered USD 152 calculation, enquiry intake, missing-name validation, model-called lead recording, unknown-question logging, and complaint logging.
- A separate fresh conversation passed the mixed bouquet-order / unsupported-delivery check. Both tools recorded successfully; history was empty for the new client.
- The narrated video presents these real replies and tool outcomes. It is an edited walkthrough of captured API evidence, rather than a continuous screen recording.
- Live runtime: `6c1df436f3abd8e14cf3f850da96dc6bbbf20cba`. Complete per-turn replies, model tool arguments/results, draft/revised replies, and capture time are in `demo/live_verification.json`.

## Reproduction

Install `requirements-dev.txt`, add your own key to `.env`, and follow `README.md`. Use `python -m unittest discover -s tests -v` for offline checks and `python demo/verify_live.py` for a new real-model run. Live API calls depend on service availability and quotas; the saved run is evidence of the capture time, not a guarantee of future responses. The fictional customer contacts are demonstration data. Leads are enquiries requiring human confirmation.
