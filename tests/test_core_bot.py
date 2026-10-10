import tempfile
import unittest
import os
from pathlib import Path
from unittest.mock import patch

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
        self.assertEqual(core_bot.classify_intent("What is in the Sweet Bloom box?", use_model=False), "general_question")
        self.assertEqual(core_bot.classify_intent("I want to reserve a pottery workshop", use_model=False), "lead_collection")
        self.assertEqual(core_bot.classify_intent("Feedback: please add candle making", use_model=False), "feedback_unanswered")
        self.assertEqual(core_bot.classify_intent("Can you deliver today?", use_model=False), "feedback_unanswered")

    def test_router_does_not_treat_products_as_automatic_leads(self):
        self.assertEqual(core_bot.classify_intent("What workshops do you offer?", use_model=False), "general_question")
        self.assertEqual(core_bot.classify_intent("How much is a bouquet?", use_model=False), "general_question")
        self.assertEqual(core_bot.classify_intent("Tell me about pottery and painting", use_model=False), "general_question")

    def test_router_recognizes_natural_lead_language(self):
        self.assertEqual(core_bot.classify_intent("I want a birthday bouquet", use_model=False), "lead_collection")
        self.assertEqual(core_bot.classify_intent("I'm interested in a private workshop", use_model=False), "lead_collection")
        self.assertEqual(core_bot.classify_intent("Please contact me about an event", use_model=False), "lead_collection")

    def test_router_prioritizes_problems_and_unknown_questions(self):
        self.assertEqual(core_bot.classify_intent("Do you have parking?", use_model=False), "feedback_unanswered")
        self.assertEqual(
            core_bot.classify_intent("The booking page would not let me choose a date.", use_model=False),
            "feedback_unanswered",
        )
        self.assertEqual(core_bot.classify_intent("The reservation page is broken", use_model=False), "feedback_unanswered")

    def test_model_router_handles_a_novel_unknown_question(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}), patch.object(
            core_bot, "_classify_with_model", return_value="feedback_unanswered"
        ) as classifier:
            self.assertEqual(core_bot.classify_intent("Do you offer valet service?"), "feedback_unanswered")
        classifier.assert_called_once_with("Do you offer valet service?")

    def test_model_router_has_a_safe_offline_fallback(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}), patch.object(
            core_bot, "_classify_with_model", side_effect=RuntimeError("offline")
        ):
            self.assertEqual(core_bot.classify_intent("Tell me something unusual"), "general_question")

    def test_explicit_intents_do_not_spend_a_router_call(self):
        with patch.object(core_bot, "_classify_with_model") as classifier:
            self.assertEqual(core_bot.classify_intent("I want to book a workshop"), "lead_collection")
            self.assertEqual(core_bot.classify_intent("Feedback: the page is broken"), "feedback_unanswered")
        classifier.assert_not_called()

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
