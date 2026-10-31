# Free Energy Mapping Printables

Seven printable planning sheets built around a simple, kind premise:
plan around your **real energy**, not around an imagined version of your
motivation. Plain HTML/CSS sources print to unbranded PDFs through one
local build script. No signups, no accounts, no tracking, no network
calls — the build only drives a local copy of headless Chrome.

By [Asdale Dynamics, LLC](https://dylanasdale.github.io).

## The sheets

| # | Sheet | Use it when |
|---|-------|-------------|
| 1 | Weekly Energy Map (blank) | You want an honest weather report of your week, in words |
| 2 | Five-Level Task Matcher | Your to-do list exists but none of it matches today's energy |
| 3 | Low-Battery Day Menu | The tank is low and decisions are too expensive |
| 4 | Realistic Hours-Per-Day Tracker | You want your real capacity number, colored honestly |
| 5 | Drain-Day Recovery Card | Something heavy emptied the tank; recovery, not productivity |
| 6 | People & Meetings Drain Sorter | 4 p.m. keeps arriving mysteriously empty |
| 7 | Sunday Gentle Review | Fifteen warm minutes to connect the week, once, kindly |

Every PDF opens with one kind intro page explaining the sheet in plain
English — no jargon, no condescension, no branding on the print pages.

This pack is distinct from the *gentle-productivity-manual* (the long-form
guide) and the *free-daily-docket-pack* (single-day pages). These are the
week-level and energy-level pages between them.

## How to build

Requirements: Python 3.8+ and Chrome, Chromium, or Edge installed locally.

```sh
python3 build.py                 # build all 7 sheets into printables/
python3 build.py 03              # build sheets matching a number/pattern
CHROME=/path/to/chrome python3 build.py   # nonstandard browser path
```

Unbranded PDFs appear in `printables/`. Print them at 100% scale on
Letter paper; sources are in `src/`.

## How to test

```sh
python3 -m unittest discover -s tests -v
```

Tests verify every physical sheet builds a valid PDF (header, trailer,
size, declared pages) and guard the repo basics: seven sheets present,
kind intro page in every source, MIT license with the exact copyright
line, and README credit.

## Privacy & license

- No secrets, API keys, or personal data anywhere in this repo.
- Nothing is uploaded; the PDF build is entirely local.
- MIT License. Copyright (c) 2026 Asdale Dynamics, LLC — print, copy,
  share, and adapt freely.
