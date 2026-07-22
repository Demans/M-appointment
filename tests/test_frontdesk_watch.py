import os
from datetime import datetime
from pathlib import Path

from frontdesk_watch import build_telegram_message, load_dotenv, parse_times_from_html


def test_parse_times_from_html_collects_available_slots() -> None:
    html = """
    <html>
      <body>
        <div class="date one-queue">
          <span class="header-text">Tuesday August 4th, 2026</span>
          <span class="available-time">10:30</span>
          <span class="available-time">11:00</span>
        </div>
        <div class="date one-queue">
          <span class="header-text">Thursday August 6th, 2026</span>
          <span class="available-time">09:00</span>
        </div>
      </body>
    </html>
    """

    slots = parse_times_from_html(html)

    assert len(slots) == 3
    assert slots[0].strftime("%Y-%m-%d %H:%M") == "2026-08-04 10:30"


def test_build_telegram_message_is_concise() -> None:
    slots = [datetime(2026, 8, 4, 10, 30), datetime(2026, 8, 4, 11, 0)]
    message = build_telegram_message(slots, "https://example.test")

    assert "Frontdesk booking alert" in message
    assert "2 free slots visible" in message
    assert "https://example.test" in message


def test_load_dotenv_reads_values_from_file(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text(
        "TELEGRAM_BOT_TOKEN=abc123\nTELEGRAM_CHAT_ID=456\n", encoding="utf-8"
    )

    os.environ.pop("TELEGRAM_BOT_TOKEN", None)
    os.environ.pop("TELEGRAM_CHAT_ID", None)
    load_dotenv(str(env_path))

    assert os.environ["TELEGRAM_BOT_TOKEN"] == "abc123"
    assert os.environ["TELEGRAM_CHAT_ID"] == "456"
