"""Verify the deployed Gemini assistant; use only fictional demonstration data."""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from gradio_client import Client

SPACE = "RanaEzzeddine/petal-and-crumb-atelier"
APP_URL = "https://ranaezzeddine-petal-and-crumb-atelier.hf.space"

def verify(output=None):
    client = Client(APP_URL, verbose=False)
    messages = [
        "What is included in Glaze & Sip?",
        "How much would that experience cost for four people?",
        "I would like to reserve that experience for four people next Saturday at 3 pm.",
        "I am interested. My email is noor.demo@example.com.",
        "Noor Haddad, noor.demo@example.com",
        "Do you offer valet service?",
        "Feedback: the pastries were stale.",
    ]
    results=[]
    for message in messages:
        reply, trace = client.submit(message, api_name="/chat").result(timeout=120)
        result={"message":message,"reply":reply,"trace":trace}
        results.append(result)
        print(json.dumps(result,ensure_ascii=False),flush=True)
        if output:
            Path(output).with_suffix('.partial.json').write_text(json.dumps({"cases":results,"passed":False},ensure_ascii=False,indent=2))
        time.sleep(12)
    assert '152' in results[1]['reply'], 'Four-person follow-up must remember Glaze & Sip and calculate USD 152.'
    assert not results[3]['trace']['tool_calls'], 'Missing name must not create a lead.'
    assert any(e['name']=='record_customer_interest' and e['result']['status']=='recorded' for e in results[4]['trace']['tool_calls'])
    assert any(e['name']=='record_feedback' and e['result']['status']=='recorded' for e in results[5]['trace']['tool_calls'])
    assert any(e['name']=='record_feedback' and e['result']['status']=='recorded' for e in results[6]['trace']['tool_calls'])
    assert all(not r['trace']['failed'] for r in results)
    assert 'not a confirmed reservation' in results[4]['reply']
    assert 'shortly' not in results[4]['reply']
    fresh = Client(APP_URL, verbose=False)
    mixed = "I want to order a birthday bouquet for delivery. My name is Maya Rahal and my email is maya.demo@example.com."
    mixed_reply, mixed_trace = fresh.submit(mixed, api_name="/chat").result(timeout=120)
    assert mixed_trace['history_messages'] == 0, 'A new client must not inherit another conversation.'
    assert not mixed_trace['failed'], 'The mixed request must finish successfully.'
    recorded = {e['name'] for e in mixed_trace['tool_calls'] if e['result']['status']=='recorded'}
    assert recorded == {'record_customer_interest', 'record_feedback'}, 'Preserve both lead and unsupported delivery question.'
    print(json.dumps({'mixed_request':mixed,'reply':mixed_reply,'trace':mixed_trace},ensure_ascii=False),flush=True)
    if output:
        Path(output).write_text(json.dumps({"space":SPACE,"runtime_commit":os.getenv("DEPLOYED_RUNTIME_REVISION", "unverified; set DEPLOYED_RUNTIME_REVISION to the actual deployed revision"), "captured_at":datetime.now(timezone.utc).isoformat(),"cases":results,"mixed_case":{"message":mixed,"reply":mixed_reply,"trace":mixed_trace},"passed":True},ensure_ascii=False,indent=2))
        Path(output).with_suffix('.partial.json').unlink(missing_ok=True)
    return results

if __name__=='__main__':
    verify(Path(__file__).with_name('live_verification.json'))
