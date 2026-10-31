# STATUS.md — free-energy-mapping-pack

Last updated: 2026-10-31

## What was built

Printable planning sheets built around real energy instead of imagined
motivation — plain, warm, ADHD-friendly, unbranded:

1. **Weekly Energy Map (blank)** — Mon–Sun × morning/midday/afternoon/evening
   grid with a 1–5 energy tint legend, plus honest-notes boxes.
2. **Five-Level Task Matcher** — mind-dump table with tasks sorted by the
   energy (1–5) each actually requires; level-1 and rewritten-task boxes.
3. **Low-Battery Day Menu** — four battery bands (0–25% survival floor →
   75–100% regular power) with checkbox menus and fill-in-your-own lines.
4. **Realistic Hours-Per-Day Tracker** — 7-day × 8-hour coloring grid with
   honest coloring instructions (only actual hours get color; x marks
   drain days; the planned-vs-colored gap is data, not failure).
5. **Drain-Day Recovery Card** — pause-first, personal floor, body/mind
   recovery menu, drain-day "no list," and tiny tomorrow-me hand-offs.
6. **People & Meetings Drain Sorter** — Energize/Neutral/Drain columns with
   one-word whys and one tiny dosage change per drain.
7. **Sunday Gentle Review** — six brief prompts (weather check, planned vs.
   actual, quiet wins, cost vs. gave, more-of-the-feeling, one carry-forward)
   plus Monday forecast boxes.

Every PDF opens with a one-page kind intro explaining the sheet in plain
English. Print pages carry no branding, no site name, no calls to action.

## Layout

```
build.py              local PDF build script (headless Chrome, no deps)
src/styles.css        shared print stylesheet (Letter, unbranded)
src/sheets/*.html     7 sheet sources, each with its intro page
printables/*.pdf      built, unbranded PDFs (committed)
tests/test_build.py   unittest suite (12 tests)
LICENSE               MIT — Copyright (c) 2026 Asdale Dynamics, LLC
README.md             usage + credit to Asdale Dynamics, LLC
```

## How to run

```sh
python3 build.py        # builds all 7 PDFs into printables/
python3 -m unittest discover -s tests -v
```

Requirements: Python 3.8+ and a local Chrome-family browser (Google
Chrome 156 was used here). `build.py` auto-detects chrome/chromium/edge;
override with `CHROME=/path/to/browser`. Fully local — no network
access during build or tests.

## Verification results

- `python3 build.py` — all 7 sheets build; PDFs are 53–75 KB each.
- `python3 -m unittest discover -s tests -v` — **12/12 tests pass**
  (runs a full temp-dir rebuild and validates every PDF header/trailer/size).
- Build script verifies each PDF exists, is non-trivial, and each source
  contains its kind intro page (a failed sheet fails the build).

## Known gaps

- No automated visual regression check; PDF text/layout was verified
  structurally (page objects, sizes), not pixel-by-pixel. Worth one
  manual print pass on Letter paper.
- Sheets are Letter-size only; no A4 variant yet (print at "fit to page"
  works fine as a workaround).
- The test that compares declared page divs to PDF page objects is
  intentionally loose; a future improvement could count pages robustly
  with a tiny PDF parser.
- No Spanish/translated versions, no editable-fill (interactive form)
  PDFs — everything is print-and-handwrite by design.
