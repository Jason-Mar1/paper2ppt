#!/usr/bin/env python3
"""Extract useful figure assets from an academic PDF.

This helper has two modes:
1. Render selected pages as high-resolution PNGs for quick visual slide assets.
2. Extract embedded bitmap images from each page when the PDF stores figures as images.

It intentionally does not try to infer figure captions perfectly. Inspect outputs and
choose the most useful assets for the deck.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable, List


def parse_pages(spec: str | None, max_pages: int) -> List[int]:
    if not spec:
        return []
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            for p in range(start, end + 1):
                if 1 <= p <= max_pages:
                    pages.add(p)
        else:
            p = int(part)
            if 1 <= p <= max_pages:
                pages.add(p)
    return sorted(pages)


def safe_ext(ext: str) -> str:
    ext = re.sub(r"[^a-zA-Z0-9]", "", ext.lower())
    if ext in {"jpg", "jpeg", "png", "webp"}:
        return "jpg" if ext == "jpeg" else ext
    return "png"


def render_pages(doc, out_dir: pathlib.Path, pages: Iterable[int], dpi: int) -> None:
    import fitz  # type: ignore

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    for page_no in pages:
        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = out_dir / f"page_{page_no:02d}.png"
        pix.save(str(out))
        print(out)


def extract_images(doc, out_dir: pathlib.Path, min_width: int, min_height: int) -> None:
    seen: set[int] = set()
    for page_index in range(len(doc)):
        page_no = page_index + 1
        page = doc[page_index]
        count = 0
        for img in page.get_images(full=True):
            xref = img[0]
            width, height = int(img[2]), int(img[3])
            if xref in seen or width < min_width or height < min_height:
                continue
            seen.add(xref)
            count += 1
            info = doc.extract_image(xref)
            ext = safe_ext(info.get("ext", "png"))
            image_bytes = info["image"]
            out = out_dir / f"p{page_no:02d}_img{count:02d}.{ext}"
            out.write_bytes(image_bytes)
            print(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="extract page renders and embedded images from a paper PDF")
    parser.add_argument("pdf", help="input pdf path")
    parser.add_argument("--out", default="paper_figures", help="output directory")
    parser.add_argument("--render-pages", default="", help="pages to render, e.g. '1,3,4' or '1-3'")
    parser.add_argument("--dpi", type=int, default=180, help="dpi for rendered pages")
    parser.add_argument("--extract-images", action="store_true", help="extract embedded bitmap images")
    parser.add_argument("--min-width", type=int, default=250, help="minimum embedded image width")
    parser.add_argument("--min-height", type=int, default=180, help="minimum embedded image height")
    args = parser.parse_args()

    pdf_path = pathlib.Path(args.pdf)
    if not pdf_path.exists():
        print(f"error: file not found: {pdf_path}", file=sys.stderr)
        return 2

    try:
        import fitz  # type: ignore
    except Exception as exc:
        print("error: PyMuPDF/fitz is required for figure extraction", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 3

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    pages = parse_pages(args.render_pages, len(doc))
    if pages:
        render_pages(doc, out_dir, pages, args.dpi)
    if args.extract_images:
        extract_images(doc, out_dir, args.min_width, args.min_height)
    if not pages and not args.extract_images:
        print("nothing requested: pass --render-pages and/or --extract-images", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
