# Record the revised Petal & Crumb assistant

The continuous recording is now included in `demo/RanaEzzeddine_C3_Demo.mp4`, and the public Space was subsequently updated to the revised runtime on October 17, 2026. The sequence below remains an optional guide for a longer recording. The supplied older edited video is unchanged.

## 1. Prepare before recording

1. Extract the revised ZIP into a folder you can find easily.
2. Open Terminal, type `cd ` (including the space), drag that extracted folder into Terminal, and press Return.
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
nano .env
```

4. In nano, replace `your_key_here` with your own Gemini API key. Keep `ENABLE_REFLECTION=true`. Save with Control+O, Return, then Control+X. Do this before recording; never show the key.
5. Run:

```bash
python -m unittest discover -s tests -v
python app.py
```

Do not claim the tests passed unless your own run finishes with `OK`. If dependency installation or an API call fails, resolve that before recording.

6. Open the local URL printed by Gradio in the terminal. Keep Terminal running.
7. Expand **Coursework demo: router, tools, and reflection**. Make the browser wide enough to show the replies and trace. The trace updates on each turn, so inspect it before sending the next prompt.
8. Open `business_agent.ipynb` in your notebook editor, plus `me/business_summary.txt`. If you want executed notebook outputs, select the same virtual environment and run all cells after adding the key. This uses real API requests and may use quota. The notebook's no-key fallback shows historical evidence instead.
9. On Mac, press Command+Shift+5, select Record Selected Portion and enable your microphone under Options. Include only the relevant browser/editor area. Choose a save location. Start recording.

## 2. Opening narration (20–30 seconds)

Show the app title. Say:

> This is Flora, the assistant for Petal & Crumb Atelier, a fictional patisserie, flower boutique, and workshop studio. It uses Gemini with three-way intent routing, conversation history, lead and feedback tools, and an optional reflection step. Business facts come from a text summary and a PDF profile.

Briefly show the `me/` files and the separate `PERSONA` and `INSTRUCTIONS` blocks in the notebook, then return to the app. Avoid scrolling through hundreds of lines.

## 3. Main conversation (approximately 3–5 minutes)

Start with an empty conversation. Enter the following prompts **one at a time**, waiting for each reply to complete.

| Step | Exact message to type | What to show and say |
|---|---|---|
| 1 | `What is included in Glaze & Sip?` | Show the USD 38 price, 90-minute session, ceramic piece, drink and pastry. Show `intent: general_question`. Say: “The answer is grounded in the business information.” |
| 2 | `How much would that experience cost for four people?` | Show USD 152 and the history count. Say: “It remembers which experience I meant and calculates the group total.” |
| 3 | `I would like to reserve that experience for four people on October 24, 2026 at 3 pm.` | Show `lead_collection` and the request for name/email. Say: “This starts an enquiry; it does not confirm availability.” |
| 4 | `I am interested. My email is an.demo@example.com.` | Show that it asks for a name and that `tool_calls` contains no recorded lead. Say: “An email alone is insufficient, so it has not saved a lead yet.” |
| 5 | `My name is An Nguyen.` | Expand `tool_calls`, then show `record_customer_interest`, its arguments and `status: recorded`. Say: “It combines my name with the earlier email and enquiry details, then actually executes the lead tool.” Show the reply's reservation disclaimer. |
| 6 | `Do you offer valet service?` | Show the honest unknown answer and `record_feedback` with a recorded result. Say: “It logs an unanswered question rather than inventing business information.” |
| 7 | `Feedback: the pastries were stale.` | Show the feedback tool and its result. Say: “The same logging tool also records explicit feedback.” |

After step 5 or 7, show `draft` and `revised` in the trace. Say:

> The reflection step reviews the draft against the business rules and actual tool outcomes. A correct draft can remain unchanged. Only a successful tool result supports a claim that something was recorded.

Do not claim a correction occurred unless you can actually see a difference.

## 4. Show the mixed-request fix (45–60 seconds)

Reload the local app page to begin a fresh conversation, then expand the evidence panel again. Type:

```text
Feedback: the pastries were stale. I would like to order a birthday bouquet. My name is Maya Rahal and my email is maya.demo@example.com.
```

Show `intent: lead_collection` and **two** successful tool events: `record_customer_interest` and `record_feedback`. Say:

> This message contains both a complaint and a new order enquiry. The assistant preserves both requests and records them through separate tools.

A further request for a preferred date or other order details is expected. The saved record is an enquiry, not a completed order.

## 5. Finish (15–20 seconds)

Say:

> This demonstrates grounded answers, short-term memory, routing, validated lead collection, unanswered-question and feedback logging, and reflection. Records are stored locally as JSONL. The assistant does not take payments or confirm reservations.

Stop recording from the macOS menu-bar stop button. Save the actual screen recording as `RanaEzzeddine_C3_Demo.mov` (or export to MP4). Watch it once to confirm readable text and microphone audio.

## Optional evidence

After the chat, you may show `logs/leads.jsonl` and `logs/feedback.jsonl` in your editor. Use only the fictional contacts above. Do not open `.env`. Local log files are demonstration storage and should not be treated as a durable production database.

## Submission preparation

Keep the existing video until your new recording is complete. If submitting the new recording inside this project, replace `demo/petal_and_crumb_demo.mp4` with your exported MP4 and update the demo README to describe the new continuous recording accurately. Recreate the ZIP without `.env`, `.venv/`, caches, or runtime logs. Retain `me/`, code, requirements, notebook, and README. The professor's brief determines whether you submit a ZIP, repository link, deployed app link, video, or some combination; that exact list has not been verified here.
