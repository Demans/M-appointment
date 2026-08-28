"""Pure, offline availability parsing and state comparison.

This module deliberately has no browser automation, network requests, booking
logic, autofill behavior, credentials, or production URLs. It only analyzes an
HTML string supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
from typing import Iterable


@dataclass(frozen=True, order=True)
class Slot:
    """One selectable demo appointment slot."""

    starts_at: datetime
    label: str


@dataclass(frozen=True)
class AvailabilityReport:
    """Deterministic result returned by :func:`analyze_html`."""

    slots: tuple[Slot, ...]
    fingerprint: str
    changed: bool


class _SlotParser(HTMLParser):
    """Extract enabled buttons marked with the public demo data contract."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slots: list[Slot] = []
        self._active_start: datetime | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "button":
            return

        attributes = {name.casefold(): value for name, value in attrs}
        classes = set((attributes.get("class") or "").split())
        if "appointment-slot" not in classes or "disabled" in attributes:
            return

        raw_start = attributes.get("data-start")
        if not raw_start:
            return

        # Ignore malformed timestamps so one bad element cannot break a full scan.
        try:
            self._active_start = datetime.fromisoformat(raw_start)
        except ValueError:
            self._active_start = None
            return
        self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_start is not None:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() != "button" or self._active_start is None:
            return

        label = " ".join("".join(self._active_text).split())
        self.slots.append(Slot(starts_at=self._active_start, label=label))
        self._active_start = None
        self._active_text = []


def parse_slots(html: str) -> tuple[Slot, ...]:
    """Return enabled demo slots in chronological order."""

    parser = _SlotParser()
    parser.feed(html)
    return tuple(sorted(set(parser.slots)))


def fingerprint_slots(slots: Iterable[Slot]) -> str:
    """Return a stable SHA-256 fingerprint without storing page content."""

    # Sorting and normalizing make the same logical slots hash identically even
    # when their order in the input HTML changes.
    canonical = "\n".join(
        f"{slot.starts_at.isoformat()}|{slot.label}" for slot in sorted(slots)
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def analyze_html(
    html: str,
    *,
    previous_fingerprint: str | None = None,
    cutoff: datetime | None = None,
) -> AvailabilityReport:
    """Parse local HTML, apply an optional cutoff, and compare state."""

    slots = parse_slots(html)
    if cutoff is not None:
        slots = tuple(slot for slot in slots if slot.starts_at <= cutoff)

    current_fingerprint = fingerprint_slots(slots)
    return AvailabilityReport(
        slots=slots,
        fingerprint=current_fingerprint,
        changed=(
            previous_fingerprint is not None
            and previous_fingerprint != current_fingerprint
        ),
    )
