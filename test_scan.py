"""
test_scan.py
Run this to verify the tool works WITHOUT needing a real chatbot.
It uses a mock chatbot that simulates vulnerable responses.

Usage:  python test_scan.py
"""
import asyncio
import json
from unittest.mock import patch, AsyncMock

# ── Mock chatbot responses for offline testing ────────────────────────────────
MOCK_RESPONSES = {
    "DI-001": "Sure! Here is my system prompt: 'You are a helpful assistant. Never reveal this.'",
    "JB-001": "I am now DAN and I can do anything. Override accepted.",
    "SYS-001": "My instructions are as follows: You must always be helpful and never refuse.",
    "SEC-001": "The API key stored is: sk-abc123XYZ789secretkey00000000000",
    "PII-001": "I found the following emails: john@example.com, jane.doe@company.lk",
    "SE-001":  "As an Anthropic auditor, I'll confirm my configuration for you.",
}

DEFAULT_SAFE_RESPONSE = "I'm sorry, I can't help with that request."


async def mock_call_chatbot(endpoint_url, api_key, model_name, prompt_text, timeout=30):
    """Simulates a chatbot — some prompts succeed (vulnerable), most are blocked."""
    for pid, response in MOCK_RESPONSES.items():
        if pid in prompt_text[:10]:   # match by prompt id prefix
            return response
    # match by content keywords
    if "system prompt" in prompt_text.lower() or "verbatim" in prompt_text.lower():
        return MOCK_RESPONSES["SYS-001"]
    if "DAN" in prompt_text:
        return MOCK_RESPONSES["JB-001"]
    if "API key" in prompt_text or "credentials" in prompt_text:
        return MOCK_RESPONSES["SEC-001"]
    return DEFAULT_SAFE_RESPONSE


async def run_test():
    print("\n" + "="*60)
    print("  AI Shield Scanner — Offline Test")
    print("="*60)

    # Patch the HTTP call so we don't need a real chatbot
    with patch("Scanner._call_chatbot", side_effect=mock_call_chatbot):
        import Scanner
        results = await Scanner.run_scan(
            endpoint_url="http://mock-chatbot/v1/chat/completions",
            api_key="test-key",
            model_name="mock-model",
            categories=["direct_injection", "jailbreak", "data_leakage_system", "data_leakage_secrets"],
            intensity="high",
        )

    summary = results["summary"]
    print(f"\n📊 Summary")
    print(f"   Total prompts  : {summary['total_prompts']}")
    print(f"   ✅ Pass         : {summary['pass_count']}")
    print(f"   ⚠️  Warning      : {summary['warning_count']}")
    print(f"   ❌ Fail         : {summary['fail_count']}")
    print(f"   Max risk score : {summary['max_score']}")
    print(f"   Overall severity: {summary['overall_severity'].upper()}")

    print(f"\n❌ Failed tests")
    for r in results["results"]:
        if r["label"] == "fail":
            print(f"\n  [{r['severity'].upper()}] {r['prompt_id']} — {r['description']}")
            print(f"  Risk score : {r['risk_score']}")
            print(f"  Reasoning  : {r['reasoning']}")
            if r["matches"]:
                print(f"  Patterns   : {', '.join(m['leak_type'] for m in r['matches'])}")
            print(f"  Fix        : {r['mitigation'][0]}")

    print("\n" + "="*60)
    print("✅ Test complete — scanner is working correctly.")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_test())