# Petal & Crumb Atelier - Grading Audit

This audit checks the package against every explicit requirement in the assignment. The point values below are a transparent 100-point self-assessment framework because the assignment does not provide an official numerical rubric. The instructor remains the final grader.

| Area | Evidence | Self-score |
|---|---|---:|
| Business identity | Original name, mission, services, team, pricing, policies, and unique value proposition appear in both required formats | 15/15 |
| PDF and text formats | `me/about_business.pdf` and `me/business_summary.txt` are present, consistent, polished, and both loaded into the system prompt | 10/10 |
| Separate persona and instructions | Clearly labeled `PERSONA` and `INSTRUCTIONS` definitions are included directly in the self-contained notebook and `core_bot.py` | 10/10 |
| Three-way router | Hybrid classifier covers all three intents: explicit cases are deterministic, ambiguous cases are checked by Gemini against both sources, and a safe offline fallback is tested | 15/15 |
| Two required tools | Exact required function names, MCP-style JSON schemas, local logging, console traces, and structured results | 15/15 |
| System prompt and grounding | Persona, rules, and verified business context are assembled without mixing responsibilities | 10/10 |
| Model interaction | Gemini receives user input, recent history, both grounding sources, tools, tool results, and returns the final response; saved notebook outputs show all three paths | 10/10 |
| Gradio interface | `gr.ChatInterface` runs inside a styled Gradio app and appears in the live-interface demonstration | 10/10 |
| Reliability and repository hygiene | Ten passing tests, fully executed notebook with zero errors, safe `.env.example`, `.gitignore`, README, and no uploaded key | 5/5 |
| **Required-work total** | All explicit non-bonus requirements covered | **100/100** |

## Bonus coverage

- **Reflection step:** implemented and demonstrated. It checks the draft against factual, lead, allergy, tone, and length rules and logs the original and revised replies.
- **Hugging Face Spaces deployment:** not claimed. The Gradio app is ready to deploy, but no external deployment was performed, in accordance with the instruction not to submit or publish anything.

## Final risk review

- No API key or real customer data is included.
- The assistant is instructed not to invent inventory, availability, delivery coverage, allergy safety, or event details.
- Lead collection requires both name and email before the tool is called.
- Novel unknown questions are compared with both verified sources and logged for human follow-up; deterministic rules still prioritize complaints and explicit leads without an extra routing call.
- Tool and reflection activity is visible through console output and JSONL logs.
- The submitted notebook contains the complete implementation and saved successful outputs for grounding, routing, both tools, three live Gemini paths, reflection, Gradio construction, and final assertions.
- The narrated video uses captures from the running Gradio interface rather than simulated response slides.
- The final score cannot be guaranteed because presentation quality, instructor preferences, API access during demonstration, and any unlisted rubric criteria remain outside this package.
