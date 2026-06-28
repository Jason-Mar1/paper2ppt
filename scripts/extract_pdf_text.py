#!/usr/bin/env python3
"""Extract readable markdown-like text from an academic PDF.

This helper is intentionally lightweight. It tries PyMuPDF first because it
usually preserves page text well; if unavailable, it falls back to pypdf or
PyPDF2. It writes page-delimited text that can be used for paper briefing.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable, Tuple


def extract_with_pymupdf(path: pathlib.Path) -> Iterable[Tuple[int, str]]:
    import fitz  # type: ignore

    doc = fitz.open(str(path))
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text") or ""
        yield i, text


def extract_with_pypdf(path: pathlib.Path) -> Iterable[Tuple[int, str]]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        from PyPDF2 import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # keep extraction moving across pages
            text = f"[text extraction failed on page {i}: {exc}]"
        yield i, text


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = []
    blank = False
    for line in lines:
        if not line.strip():
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False
    return "\n".join(cleaned).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="extract text from a paper pdf")
    parser.add_argument("pdf", help="input pdf path")
    parser.add_argument("--out", default="extracted_paper.md", help="output markdown text path")
    args = parser.parse_args()

    pdf_path = pathlib.Path(args.pdf)
    if not pdf_path.exists():
        print(f"error: file not found: {pdf_path}", file=sys.stderr)
        return 2

    try:
        pages = list(extract_with_pymupdf(pdf_path))
        engine = "pymupdf"
    except Exception:
        pages = list(extract_with_pypdf(pdf_path))
        engine = "pypdf"

    out_path = pathlib.Path(args.out)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Extracted Paper Text\n\nsource: {pdf_path.name}\nengine: {engine}\n\n")
        for page_no, text in pages:
            f.write(f"\n\n## Page {page_no}\n\n")
            f.write(normalize_text(text))
            f.write("\n")

    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
