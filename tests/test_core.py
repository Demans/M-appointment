from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from appointment_monitor.core import analyze_html, fingerprint_slots, parse_slots


FIXTURES = Path(__file__).parent / "fixtures"


class AvailabilityMonitorTests(unittest.TestCase):
    def test_extracts_only_enabled_slots_in_chronological_order(self) -> None:
        html = (FIXTURES / "available.html").read_text(encoding="utf-8")
        slots = parse_slots(html)

        self.assertEqual(2, len(slots))
        self.assertEqual("2026-09-14T13:00:00", slots[0].starts_at.isoformat())
        self.assertEqual("14 Sep, 13:00", slots[0].label)

    def test_unavailable_page_has_stable_empty_fingerprint(self) -> None:
        html = (FIXTURES / "unavailable.html").read_text(encoding="utf-8")
        report = analyze_html(html)

        self.assertEqual((), report.slots)
        self.assertEqual(fingerprint_slots(()), report.fingerprint)

    def test_cutoff_filters_later_slots(self) -> None:
        html = (FIXTURES / "available.html").read_text(encoding="utf-8")
        report = analyze_html(html, cutoff=datetime.fromisoformat("2026-09-30T23:59:00"))

        self.assertEqual(1, len(report.slots))
        self.assertEqual("2026-09-14T13:00:00", report.slots[0].starts_at.isoformat())

    def test_change_is_reported_only_when_prior_state_exists(self) -> None:
        html = (FIXTURES / "available.html").read_text(encoding="utf-8")
        first = analyze_html(html)
        repeated = analyze_html(html, previous_fingerprint=first.fingerprint)
        changed = analyze_html(html, previous_fingerprint="different")

        self.assertFalse(first.changed)
        self.assertFalse(repeated.changed)
        self.assertTrue(changed.changed)


if __name__ == "__main__":
    unittest.main()

