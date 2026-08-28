"""Command-line interface for the offline portfolio demo."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from .core import analyze_html


def _load_previous_fingerprint(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = payload.get("fingerprint")
    return value if isinstance(value, str) else None


def _save_state(path: Path, fingerprint: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"fingerprint": fingerprint}, indent=2) + "\n"
    # Write beside the target first, then replace it atomically. This avoids a
    # half-written state file if the process is interrupted during the write.
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        temporary.write(payload)
        temporary_path = Path(temporary.name)
    temporary_path.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a local demo HTML fixture for appointment availability."
    )
    parser.add_argument("html", type=Path, help="Path to a local HTML fixture")
    parser.add_argument(
        "--state",
        type=Path,
        default=Path("state.json"),
        help="Local state file (ignored by Git)",
    )
    parser.add_argument(
        "--cutoff",
        type=datetime.fromisoformat,
        help="Optional ISO-8601 cutoff, for example 2026-09-30T23:59:00",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    html = args.html.read_text(encoding="utf-8")
    previous = _load_previous_fingerprint(args.state)
    report = analyze_html(
        html,
        previous_fingerprint=previous,
        cutoff=args.cutoff,
    )

    print(f"Available slots: {len(report.slots)}")
    for slot in report.slots:
        print(f"- {slot.starts_at.isoformat()} | {slot.label}")
    print(f"Changed since last run: {'yes' if report.changed else 'no'}")

    _save_state(args.state, report.fingerprint)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
