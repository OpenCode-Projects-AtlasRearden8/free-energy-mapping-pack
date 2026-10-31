#!/usr/bin/env python3
"""Build the Free Energy Mapping printables as PDFs from HTML sources.

Uses headless Chrome (--print-to-pdf) so the toolchain stays local and
dependency-free. Output PDFs land in printables/ and are unbranded.

Usage:
    python3 build.py            # build every sheet
    python3 build.py 03 07      # build only sheets whose filename matches
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_HTML = ROOT / "src" / "sheets"
SRC_CSS = ROOT / "src" / "styles.css"
OUT_DIR = ROOT / "printables"

INTRO_MARK = "page intro-page"

# Candidate Chrome-family executables, most-specific first.
CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "microsoft-edge",
]


def find_chrome() -> str:
    """Locate a Chrome-family binary: env CHROME first, then PATH candidates."""
    env = os.environ.get("CHROME")
    if env and shutil.which(env):
        return shutil.which(env)
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError(
        "No Chrome-family browser found. Install Google Chrome/Chromium, "
        "or set the CHROME environment variable to its path. "
        "The build only drives Chrome locally; nothing is uploaded."
    )


def chrome_cmd(out_pdf: Path, html_file: Path) -> list:
    return [
        find_chrome(),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + str(out_pdf),
        "--virtual-time-budget=4000",
        html_file.resolve().as_uri(),
    ]


def build_sheet(html_file: Path, out_pdf: Path) -> None:
    text = html_file.read_text(encoding="utf-8")
    if INTRO_MARK not in text:
        raise ValueError(f"{html_file.name}: missing intro page ({INTRO_MARK!r})")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    cmd = chrome_cmd(out_pdf, html_file)
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"{html_file.name}: chrome exited {proc.returncode}\n{proc.stderr[-2000:]}"
        )
    if not out_pdf.exists() or out_pdf.stat().st_size < 1000:
        raise RuntimeError(f"{html_file.name}: PDF missing or suspiciously small")


def sheet_pdfs() -> list:
    """(html, pdf) filename pairs sorted by sheet number."""
    pdfs = []
    for html in sorted(SRC_HTML.glob("*.html")):
        pdfs.append((html, OUT_DIR / (html.stem + ".pdf")))
    return pdfs


def build_all(only: str = "") -> list:
    if not SRC_HTML.is_dir():
        raise RuntimeError(f"missing {SRC_HTML}")
    if not SRC_CSS.is_file():
        raise RuntimeError(f"missing {SRC_CSS}")
    built = []
    for html, pdf in sheet_pdfs():
        if only and not re.search(only, html.name):
            continue
        build_sheet(html, pdf)
        built.append((html, pdf))
    return built


def main(argv: list) -> int:
    only = "".join(a for a in argv[1:] if a.strip())
    try:
        built = build_all(only)
    except Exception as exc:  # noqa: BLE001 - single entry point reports it
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    for html, pdf in built:
        print(f"  ok  printables/{pdf.name}  <- {html.name}")
    print(f"Built {len(built)} PDF(s) in {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
