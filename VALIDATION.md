# Revised-package verification

Reviewed and revised on 2026-10-17.

## Checks completed for this revision

- Seven dependency-free regression tests passed against the actual contact parsing and routing functions, covering valid name components, placeholder rejection, mixed complaint/order requests, complaints with contacts, unsupported topics in orders, policy/price questions, and user-origin contacts.
- All Python source files pass compilation.
- The notebook implementation cell matches the revised `core_bot.py`.
- The existing MP4 and saved live API evidence are preserved byte-for-byte.
- Two additional SDK integration regressions cover executing both tools for a mixed request and recording feedback while contacts are still missing.

## Final verification before repository submission

- All **34 offline tests passed** on 2026-10-17 using `python -m unittest discover -s tests -v`, including SDK integration tests with simulated model responses and seven contact/routing checks.
- The executed notebook also reports 34 passing tests. Its implementation cell matches `core_bot.py` after trimming the final newline.
- The supplied continuous screen recording is included as `demo/RanaEzzeddine_C3_Demo.mp4` (approximately 2 minutes 20 seconds). It shows the revised local app using live Gemini responses; the original MOV is unchanged.
- `demo/recording_evidence.json` contains six actual audit entries from the recording session, with email addresses redacted. Its runtime SHA-256 matches the submitted `core_bot.py`.
- The recording demonstrates grounded answers, six-person pricing, enquiry collection, unanswered-question logging, and feedback. It does not demonstrate every regression scenario; mixed-intent behavior is covered by the offline tests.
- The new recording and audit entries verify the revised local runtime. The existing Hugging Face Space has not been redeployed and still represents the older version.

## Historical evidence

The original notebook reported 25 passing tests, and `demo/live_verification.json` contains a previously captured successful live run for runtime `6c1df436f3abd8e14cf3f850da96dc6bbbf20cba`. That evidence and the existing edited video describe the earlier runtime; they do not verify this revision. The final notebook contains fresh offline execution output; historical live API output is explicitly labeled and supplemented by the new recording-session audit evidence. The existing public Space was not updated by this ZIP revision.

## Changes

- Valid multiword names such as An Nguyen and To Lam are accepted while standalone placeholders are still rejected.
- Explicit orders are preserved when the same message contains a complaint; contact details alone do not turn a complaint into an order.
- Mixed requests expose and require the feedback tool as appropriate, including before a customer has supplied their contacts.
- Recognized unsupported topics use the same detection in routing and mixed-request tool handling.
- The optional deployment wrapper runs the packaged source rather than downloading a pinned older GitHub runtime. Deploy as a CPU Gradio Space using app.py.
- The live verification script no longer labels every new run with a hardcoded old commit. Set DEPLOYED_RUNTIME_REVISION to your actual deployed revision when recording new evidence.
