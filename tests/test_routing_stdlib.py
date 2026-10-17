"""Dependency-free regression checks of actual pure functions in core_bot.py.

The SDK integration suite in test_core_bot.py still requires requirements.txt.
"""
import ast
import re
import unittest
from pathlib import Path
from typing import Any


def load_logic():
    source = Path(__file__).resolve().parents[1] / 'core_bot.py'
    names = {'_content_text', 'normalize_history', '_valid_name', 'extract_contacts',
             '_has_explicit_feedback', '_has_unsupported_topic', '_heuristic_intent'}
    selected = []
    for node in ast.parse(source.read_text()).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            selected.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and
                t.id in {'EMAIL_RE', 'MAX_HISTORY_MESSAGES'} for t in node.targets):
            selected.append(node)
    scope = {'Any': Any, 're': re}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(source), 'exec'), scope)
    return scope


class RoutingContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logic = load_logic()

    def test_name_components_are_not_rejected_as_articles(self):
        for name in ['An Nguyen', 'To Lam', 'Élodie Moreau', 'Noor Haddad']:
            with self.subTest(name=name):
                result = self.logic['extract_contacts'](f'My name is {name} and my email is guest@example.com.')
                self.assertEqual(result['name'], name)

    def test_interest_and_placeholders_are_not_names(self):
        for value in ['an', 'Unknown', 'interested in a workshop']:
            self.assertFalse(self.logic['_valid_name'](value))
        self.assertEqual(self.logic['extract_contacts']('I am interested. My email is guest@example.com.')['name'], '')

    def test_complaint_and_order_preserve_lead_in_both_orders(self):
        for message in ['Feedback: the pastries were stale. I would like to order a bouquet.',
                        'I would like to order a bouquet. Feedback: the pastries were stale.',
                        'The pastries were stale. Can I order a birthday cake?']:
            self.assertEqual(self.logic['_heuristic_intent'](message), 'lead_collection')
            self.assertTrue(self.logic['_has_explicit_feedback'](message))

    def test_complaint_with_contact_is_still_feedback(self):
        self.assertEqual(self.logic['_heuristic_intent']('Feedback: the pastries were stale. My email is guest@example.com.'), 'feedback_unanswered')

    def test_recognized_unknown_topics_survive_a_lead(self):
        for topic in ['delivery', 'valet', 'restroom', 'pet-friendly', 'wheelchair']:
            message = f'I want to order a bouquet. Do you offer {topic}?'
            self.assertEqual(self.logic['_heuristic_intent'](message), 'lead_collection')
            self.assertTrue(self.logic['_has_unsupported_topic'](message))

    def test_price_and_policy_questions_are_not_orders_or_complaints(self):
        for message in ['How much for four people?', 'What is your cancellation policy?']:
            self.assertIsNone(self.logic['_heuristic_intent'](message))

    def test_contact_provenance_and_follow_up(self):
        history = [{'role': 'assistant', 'content': 'My name is Flora. May I have your name?'}]
        self.assertEqual(self.logic['extract_contacts']('An Nguyen', history)['name'], 'An Nguyen')
        self.assertEqual(self.logic['extract_contacts']('Hello', history)['email'], '')


if __name__ == '__main__':
    unittest.main()
