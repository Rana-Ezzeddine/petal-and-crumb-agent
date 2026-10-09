import tempfile
import unittest
from pathlib import Path

import core_bot


class CoreBotTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_log_dir = core_bot.LOG_DIR
        core_bot.LOG_DIR = Path(self.temp_dir.name)

    def tearDown(self):
        core_bot.LOG_DIR = self.original_log_dir
        self.temp_dir.cleanup()

    def test_all_router_branches(self):
        self.assertEqual(core_bot.classify_intent("What is in the Sweet Bloom box?"), "general_question")
        self.assertEqual(core_bot.classify_intent("I want to reserve a pottery workshop"), "lead_collection")
        self.assertEqual(core_bot.classify_intent("Feedback: please add candle making"), "feedback_unanswered")
        self.assertEqual(core_bot.classify_intent("Can you deliver today?"), "feedback_unanswered")

    def test_router_does_not_treat_products_as_automatic_leads(self):
        self.assertEqual(core_bot.classify_intent("What workshops do you offer?"), "general_question")
        self.assertEqual(core_bot.classify_intent("How much is a bouquet?"), "general_question")
        self.assertEqual(core_bot.classify_intent("Tell me about pottery and painting"), "general_question")

    def test_router_recognizes_natural_lead_language(self):
        self.assertEqual(core_bot.classify_intent("I want a birthday bouquet"), "lead_collection")
        self.assertEqual(core_bot.classify_intent("I'm interested in a private workshop"), "lead_collection")
        self.assertEqual(core_bot.classify_intent("Please contact me about an event"), "lead_collection")

    def test_router_prioritizes_problems_and_unknown_questions(self):
        self.assertEqual(core_bot.classify_intent("Do you have parking?"), "feedback_unanswered")
        self.assertEqual(
            core_bot.classify_intent("The booking page would not let me choose a date."),
            "feedback_unanswered",
        )
        self.assertEqual(core_bot.classify_intent("The reservation page is broken"), "feedback_unanswered")

    def test_pdf_and_summary_both_ground_the_system_prompt(self):
        self.assertTrue(core_bot.BUSINESS_CONTEXT.strip())
        self.assertTrue(core_bot.PDF_CONTEXT.strip())
        self.assertIn("Verified short business summary", core_bot.SYSTEM_PROMPT)
        self.assertIn("Verified full PDF business profile", core_bot.SYSTEM_PROMPT)

    def test_interest_tool_logs_jsonl(self):
        result = core_bot.record_customer_interest("guest@example.com", "Demo Guest", "Four-person floral workshop")
        self.assertEqual(result["status"], "recorded")
        self.assertTrue((core_bot.LOG_DIR / "leads.jsonl").exists())

    def test_feedback_tool_logs_jsonl(self):
        result = core_bot.record_feedback("Do you deliver outside the listed area?")
        self.assertEqual(result["status"], "recorded")
        self.assertTrue((core_bot.LOG_DIR / "feedback.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
