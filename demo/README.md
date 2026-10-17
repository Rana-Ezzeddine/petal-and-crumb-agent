# Demonstration evidence

- `petal_and_crumb_demo.mp4`: narrated walkthrough of the actual captured Gemini conversation and per-turn tool results. This is an edited presentation of live API evidence, not a continuous screen recording.
- `live_verification.json`: full replies, router labels, prior-message counts, model-selected tool arguments, actual tool results, and draft/revised replies. Contacts are fictional. The capture includes a timestamp and the deployed runtime revision.
- `verify_live.py`: reruns the live sequence and asserts calculation/memory, missing-name handling, both model-called tools, independent conversations, and mixed lead-plus-delivery handling.
- `build_demo.py`: optional macOS helper that builds the video from that evidence using Pillow, imageio-ffmpeg, and the system `say` voice.

The notebook displays the saved live evidence when no local API key is configured. Set `RUN_LIVE_DEMO=1` to rerun the public app checks, or add your own `GEMINI_API_KEY` to run the complete implementation locally.
