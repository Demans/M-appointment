# Appointment Availability Monitor — Portfolio-Safe Demo

A small, testable Python project that demonstrates the reusable engineering
ideas behind an appointment-monitoring workflow: parsing structured HTML,
normalizing available slots, applying a date cutoff, generating deterministic
state fingerprints, and reporting whether availability changed.

This repository is intentionally **offline-only**. It analyzes local synthetic
HTML fixtures and never connects to a real appointment service.

## Why this version is safe to publish

The private working project contains personal workflow details that do not
belong in a public portfolio. This clean-room demo therefore excludes:

- Real or private service URLs
- Booking, reservation, and autofill code
- Personal form data and booking profiles
- API keys, bot tokens, chat IDs, cookies, and credentials
- Live HTML captures, state files, logs, screenshots, caches, and ZIP archives
- Automatic browser actions and network requests

The included HTML files are fictional test fixtures.

## What it demonstrates

- Python data modeling with immutable dataclasses
- Defensive HTML parsing with the standard library
- Deterministic SHA-256 state fingerprints
- Optional date-cutoff filtering
- Atomic local state updates
- Command-line interface design
- Unit tests and a least-privilege GitHub Actions workflow
- Privacy-by-design separation between a real workflow and a public demo

## Run it

Requires Python 3.11 or newer.

```bash
python -m pip install --no-deps -e .
appointment-monitor-demo tests/fixtures/available.html --state state.json
python -m unittest discover -s tests -v
```

Example output:

```text
Available slots: 2
- 2026-09-14T13:00:00 | 14 Sep, 13:00
- 2026-10-02T09:30:00 | 2 Oct, 09:30
Changed since last run: no
```

## Project background and attribution

This portfolio demo represents lessons learned while substantially extending a
forked appointment-monitoring workflow in collaboration with a friend. The
working process was AI-assisted: AI tools helped with research, debugging,
implementation ideas, and automated development setup; changes were reviewed
and tested by the project collaborators.

The original upstream concept came from
[`macbrina/appointment`](https://github.com/macbrina/appointment). This public
demo is a deliberately reduced, privacy-safe implementation and does not claim
the upstream project as original work.

## Privacy boundary

Do not add a real page URL, browser automation, notifications, personal booking
data, or autofill behavior to this repository. Keep the operational version in
a separate private location and follow [SECURITY.md](SECURITY.md).

