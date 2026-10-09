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
