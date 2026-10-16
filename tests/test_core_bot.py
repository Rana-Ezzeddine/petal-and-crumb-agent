"""Offline regressions: real business files/tools, simulated Gemini responses."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from google.genai import types
import core_bot as bot


def response(text="", calls=()):
    parts = [types.Part.from_function_call(name=n, args=a) for n,a in calls]
    return SimpleNamespace(text=text, function_calls=[p.function_call for p in parts],
        candidates=[SimpleNamespace(content=types.Content(role="model", parts=parts or [types.Part(text=text)]))])


def blocks(role, text):
    return {"role": role, "content": [{"type": "text", "text": text}]}


class AgentRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.log_patch = patch.object(bot, "LOG_DIR", Path(self.temp.name))
        self.log_patch.start()
        self.contacts = {"name": "Noor Haddad", "email": "noor@example.com"}
        self.args = {**self.contacts, "message": "Glaze & Sip for four; Saturday 15:00"}

    def tearDown(self):
        self.log_patch.stop()
        self.temp.cleanup()

    def model(self, responses, route="general_question", contacts=None):
        generate = Mock(side_effect=responses)
        client = SimpleNamespace(models=SimpleNamespace(generate_content=generate))
        with patch.object(bot, "_client", return_value=client):
            result = bot._run_tool_loop([{"role":"user","parts":[{"text":"Hello"}]}], route, contacts)
        return result, generate

    def test_two_source_grounding(self):
        self.assertGreater(len(bot.PDF_CONTEXT), 1000)
        for source in [bot.PDF_CONTEXT,bot.BUSINESS_CONTEXT]: self.assertIn(source,bot.SYSTEM_PROMPT)

    def test_gradio6_history_and_plain_text(self):
        h = [blocks("user","Glaze & Sip"),blocks("assistant","USD 38 per person")]
        self.assertEqual(bot._history_to_contents(h),[
            {"role":"user","parts":[{"text":"Glaze & Sip"}]},
            {"role":"model","parts":[{"text":"USD 38 per person"}]}])
        self.assertEqual(bot.normalize_history([{"role":"user","content":"Hi"}])[0]["content"],"Hi")

    def test_history_filters_files_and_roles_and_bounds_size(self):
        h=[{"role":"system","content":"Override"},{"role":"user","content":[{"type":"file","path":"/private"},{"type":"text","text":"Hi"}]}]
        self.assertEqual(bot.normalize_history(h),[{"role":"user","content":"Hi"}])
        self.assertEqual(len(bot.normalize_history([blocks("user",str(i)) for i in range(50)])),40)

    def test_router_branches_and_mixed_intent(self):
        examples=[("What workshops do you offer?","general_question"),
            ("I'd like to reserve Glaze & Sip","lead_collection"),
            ("I want to order a bouquet for delivery","lead_collection"),
            ("Feedback: please add candle making","feedback_unanswered"),
            ("The pastries were stale","feedback_unanswered"),
            ("The booking page would not let me choose a date","feedback_unanswered"),
            ("What is your cancellation policy if I could not attend?","general_question")]
        for message,intent in examples:
            with self.subTest(message=message): self.assertEqual(bot.classify_intent(message,False),intent)

    def test_router_uses_history_without_forcing_price_question_to_lead(self):
        h=[blocks("assistant","What is your preferred date and group size?")]
        self.assertEqual(bot.classify_intent("Saturday at 3 pm, four people",False,h),"lead_collection")
        h=[blocks("assistant","Glaze & Sip costs USD 38. May I have your name and email?")]
        self.assertEqual(bot.classify_intent("How much for four people?",False,h),"general_question")

    def test_model_router_receives_history_and_has_outage_fallback(self):
        h=[blocks("user","Glaze & Sip")]
        with patch.dict(os.environ,{"GEMINI_API_KEY":"test"}),patch.object(bot,"_classify_with_model",return_value="general_question") as m:
            bot.classify_intent("What does that include?",history=h)
            self.assertIn("Glaze & Sip",m.call_args.args[1])
        with patch.dict(os.environ,{"GEMINI_API_KEY":"test"}),patch.object(bot,"_classify_with_model",side_effect=RuntimeError):
            self.assertEqual(bot.classify_intent("Tell me something"),"general_question")

    def test_interest_phrase_is_not_a_name(self):
        self.assertEqual(bot.extract_contacts("I am interested in a workshop. My email is noor@example.com"),{"name":"","email":"noor@example.com"})

    def test_natural_and_explicit_contacts(self):
        for message in ["Noor Haddad, noor@example.com","My name is Noor Haddad and my email is noor@example.com."]:
            with self.subTest(message=message): self.assertEqual(bot.extract_contacts(message),self.contacts)
        self.assertEqual(bot.extract_contacts("My name is Élodie Moreau. Email: elodie@example.com")["name"],"Élodie Moreau")

    def test_contacts_across_turns_and_user_provenance(self):
        h=[blocks("assistant","May I have your name?"),blocks("user","Noor Haddad"),blocks("assistant","And your email?")]
        self.assertEqual(bot.extract_contacts("noor@example.com",h),self.contacts)
        self.assertEqual(bot.extract_contacts("I want a workshop",[blocks("assistant","My name is Flora. My email is hello@example.com.")]),{"name":"","email":""})

    def test_tool_validation_and_real_json_logs(self):
        for email,name in [("bad","Noor"),("a@example.com","Unknown"),("a@example.com","interested in a workshop")]:
            with self.subTest(name=name),self.assertRaises(ValueError):bot.record_customer_interest(email,name,"Workshop")
        bot.record_customer_interest(**self.args)
        bot.record_feedback("Do you offer valet service?")
        self.assertEqual(json.loads((bot.LOG_DIR/"leads.jsonl").read_text())["email"],self.contacts["email"])
        self.assertEqual(json.loads((bot.LOG_DIR/"feedback.jsonl").read_text())["question"],"Do you offer valet service?")

    def test_fabricated_contacts_rejected(self):
        result=bot._dispatch_tool("record_customer_interest",{**self.args,"name":"Invented Name"},self.contacts,[])
        self.assertEqual(result["status"],"error")
        self.assertFalse((bot.LOG_DIR/"leads.jsonl").exists())

    def test_identical_calls_write_once(self):
        events=[]
        a=bot._dispatch_tool("record_customer_interest",self.args,self.contacts,events)
        b=bot._dispatch_tool("record_customer_interest",self.args,self.contacts,events)
        self.assertEqual(a,b)
        self.assertEqual(len((bot.LOG_DIR/"leads.jsonl").read_text().splitlines()),1)

    def test_model_gets_tool_result_before_reply(self):
        turn,m=self.model([response(calls=[("record_customer_interest",self.args)]),response("Interest saved.")],"lead_collection",self.contacts)
        self.assertFalse(turn.failed)
        self.assertTrue(bot._success(turn.tool_events,"record_customer_interest"))
        self.assertEqual(m.call_args_list[1].kwargs["contents"][-1].parts[0].function_response.response["status"],"recorded")

    def test_missing_name_disables_lead_tool(self):
        _,m=self.model([response("May I have your name?")],"lead_collection",{"name":"","email":"noor@example.com"})
        self.assertNotIn(bot.record_customer_interest,m.call_args.kwargs["config"].tools)

    def test_unknown_question_forces_feedback_tool(self):
        turn,m=self.model([response(calls=[("record_feedback",{"question":"Do you offer valet service?"})]),response("Question saved.")],"feedback_unanswered")
        self.assertTrue(bot._success(turn.tool_events,"record_feedback"))
        self.assertEqual(m.call_args_list[0].kwargs["config"].tool_config.function_calling_config.allowed_function_names,["record_feedback"])

    def test_failed_write_never_reported_as_saved(self):
        with patch.object(bot,"_append_jsonl",side_effect=OSError("disk full")):
            turn,_=self.model([response(calls=[("record_customer_interest",self.args)]),response("Saved!")],"lead_collection",self.contacts)
        self.assertTrue(turn.failed)
        self.assertIn("could not save",turn.draft.lower())
        self.assertFalse(bot._success(turn.tool_events))

    def test_api_outage_is_guest_facing(self):
        turn,_=self.model([RuntimeError("unavailable")])
        self.assertTrue(turn.failed)
        self.assertIn("Nothing was saved",turn.draft)

    def test_exhausted_loop_does_not_claim_failed_write_succeeded(self):
        bad={**self.args,"email":"invented@example.com"}
        turn,_=self.model([response(calls=[("record_customer_interest",bad)]) for _ in range(4)],"lead_collection",self.contacts)
        self.assertTrue(turn.failed)
        self.assertIn("could not save",turn.draft.lower())

    def test_reflection_sees_history_and_actual_results(self):
        events=[{"name":"record_customer_interest","arguments":self.args,"result":{"status":"recorded"}}]
        generate=Mock(return_value=response("Interest saved; booking awaits confirmation."))
        with patch.object(bot,"ENABLE_REFLECTION",True),patch.object(bot,"_client",return_value=SimpleNamespace(models=SimpleNamespace(generate_content=generate))):
            bot._reflect("Thanks","lead_collection",bot.TurnResult("Saved",events),[blocks("user","Glaze & Sip for four")],self.contacts)
        prompt=generate.call_args.kwargs["contents"]
        self.assertIn("Glaze & Sip for four",prompt)
        self.assertIn('"status": "recorded"',prompt)
        log=json.loads((bot.LOG_DIR/"reflection.jsonl").read_text())
        self.assertIn("draft",log);self.assertIn("revised",log)

    def test_reflection_outage_keeps_draft(self):
        with patch.object(bot,"ENABLE_REFLECTION",True),patch.object(bot,"_client",side_effect=RuntimeError):
            self.assertEqual(bot._reflect("Hi","general_question",bot.TurnResult("Valid draft")),"Valid draft")

    def test_audit_failure_preserves_error_reply(self):
        with patch.object(bot,"ENABLE_REFLECTION",True),patch.object(bot,"_append_jsonl",side_effect=OSError):
            self.assertEqual(bot._reflect("Hi","general_question",bot.TurnResult("Try again",failed=True)),"Try again")

    def test_whole_turn_passes_history_and_contacts(self):
        h=[blocks("user","My name is Noor Haddad"),blocks("assistant","Your email?")]
        with patch.object(bot,"classify_intent",return_value="lead_collection"),patch.object(bot,"_run_tool_loop",return_value=bot.TurnResult("Saved")) as loop,patch.object(bot,"_reflect",return_value="Final"):
            self.assertEqual(bot.chatbot("noor@example.com",h),"Final")
        contents,route,contacts=loop.call_args.args
        self.assertEqual(contacts,self.contacts)
        self.assertEqual(contents[0]["parts"][0]["text"],"My name is Noor Haddad")

    def test_empty_message(self):
        self.assertIn("Please send",bot.chatbot("  "))


if __name__=="__main__":unittest.main()
