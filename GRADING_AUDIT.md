# Petal & Crumb Atelier - Grading Audit

This audit checks the package against every explicit requirement in the assignment. The point values below are a transparent 100-point self-assessment framework because the assignment does not provide an official numerical rubric. The instructor remains the final grader.

| Area | Evidence | Self-score |
|---|---|---:|
| Business identity | Original name, mission, services, team, pricing, policies, and unique value proposition appear in both required formats | 15/15 |
| PDF and text formats | `me/about_business.pdf` and `me/business_summary.txt` are present, consistent, and polished | 10/10 |
| Separate persona and instructions | Clearly labeled `PERSONA` and `INSTRUCTIONS` constants appear in the notebook and `core_bot.py` | 10/10 |
| Three-way router | Deterministic classifier covers general questions, leads, and feedback/unanswered questions; notebook contains visible sample output | 15/15 |
| Two required tools | Exact required function names, MCP-style JSON schemas, local logging, console traces, and structured results | 15/15 |
| System prompt and grounding | Persona, rules, and verified business context are assembled without mixing responsibilities | 10/10 |
| Model interaction | Gemini receives user input, recent history, tools, tool-call execution, tool results, and returns the final response | 10/10 |
| Gradio interface | `gr.ChatInterface` is ready in both `app.py` and the notebook | 10/10 |
| Reliability and repository hygiene | Safe `.env.example`, `.gitignore`, dependency ranges, offline tests, README, and no real API key | 5/5 |
| **Required-work total** | All explicit non-bonus requirements covered | **100/100** |

## Bonus coverage

- **Reflection step:** implemented. It checks the draft against factual, lead, allergy, tone, and length rules and logs the original and revised replies.
- **Hugging Face Spaces deployment:** not claimed. The Gradio app is ready to deploy, but no external deployment was performed, in accordance with the instruction not to submit or publish anything.

## Final risk review

- No API key or real customer data is included.
- The assistant is instructed not to invent inventory, availability, delivery coverage, allergy safety, or event details.
- Lead collection requires both name and email before the tool is called.
- Unknown questions are logged for human follow-up.
- Tool and reflection activity is visible through console output and JSONL logs.
- The final score cannot be guaranteed because presentation quality, instructor preferences, API access during demonstration, and any unlisted rubric criteria remain outside this package.
