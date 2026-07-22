"""Integration test: send a Telegram message using credentials from .env.

This test is skipped unless `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
are configured in the project's `.env` or environment.
"""
import time
import os

import pytest
import requests

from frontdesk_watch import load_dotenv


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


@pytest.mark.skipif(not (TOKEN and CHAT_ID), reason="Telegram token/chat id not configured in .env")
def test_send_telegram_message():
    """Send a test message and assert Telegram returns success.

    WARNING: This posts a real message to your Telegram account/chat.
    """
    ts = int(time.time())
    text = f"frontdesk_watch pytest integration test at {ts}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    resp = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=15)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("ok") is True, data
    # result should contain message metadata including message_id
    assert isinstance(data.get("result"), dict) and data["result"].get("message_id") is not None
