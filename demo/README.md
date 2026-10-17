# Demonstration evidence

## Primary recording

[RanaEzzeddine_C3_Demo.mp4](RanaEzzeddine_C3_Demo.mp4) is the student's continuous screen recording of the revised local Gradio app on October 17, 2026, lasting approximately 2 minutes 20 seconds. It shows grounded workshop information, memory and a six-person USD 228 calculation, enquiry collection, an unanswered valet-service question, and feedback logging. The MP4 preserves the recording sequence and audio, with browser-compatible video compression; the original MOV is unchanged.

[recording_evidence.json](recording_evidence.json) contains the six actual reflection/audit entries from that recording's UTC time window. It shows the route, original/revised replies, model-selected tool arguments, and real tool results. Email addresses are redacted. The file records the SHA-256 of the revised `core_bot.py` to identify the runtime. It is supporting structured evidence, not a new simulated conversation or a replacement for the recording.

## Historical supplementary material

- `petal_and_crumb_demo.mp4`: the earlier narrated, edited walkthrough of captured live API evidence.
- `live_verification.json`: earlier complete live replies and tool traces, including a timestamp and the old deployed runtime revision; fictional contacts only.
- `verify_live.py`: reruns the public app sequence and checks memory, calculation, missing-name handling, model tool execution, and conversation isolation. The Space now runs the revised runtime; the old `live_verification.json` remains historical. Set `DEPLOYED_RUNTIME_REVISION` to the actual deployed revision when capturing new evidence.
- `build_demo.py`: optional helper that rebuilds the older edited walkthrough from its historical evidence.

The notebook labels earlier saved API evidence separately from the new recording-session audit entries.

## Current hosted bonus evidence

`hosted_verification.json` is the successful post-deployment live run at Hugging Face revision `b6dd0ad18a9060e771f87716a7a258907a963a0d`. It contains seven conversation turns and a separate mixed order/delivery request, with actual model-selected tools, results, reflection, and successful assertions. All contact details in this file are fictional.
