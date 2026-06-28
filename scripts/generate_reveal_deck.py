#!/usr/bin/env python3
"""Generate a standalone reveal.js HTML deck from simple markdown.

The script is intentionally dependency-light. It supports headings, bullets,
blockquote visual placeholders, markdown images, and simple markdown tables.
The default reveal.js assets load from jsDelivr, so the generated HTML works
when opened with internet access.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Slide:
    title: str
    body_lines: List[str]


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def extract_deck_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def parse_slides(markdown: str) -> List[Slide]:
    slides: List[Slide] = []
    current_title: str | None = None
    current_body: List[str] = []

    def flush() -> None:
        nonlocal current_title, current_body
        if current_title is not None:
            slides.append(Slide(current_title, current_body))
        current_title = None
        current_body = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            flush()
            current_title = h2.group(1).strip()
            continue
        if re.match(r"^#\s+", line):
            continue
        if line.strip() == "---":
            flush()
            continue
        if current_title is None:
            if line.strip():
                current_title = "Overview"
                current_body.append(line)
            continue
        current_body.append(line)

    flush()
    return [slide for slide in slides if slide.title.strip() or any(x.strip() for x in slide.body_lines)]


def inline_markdown(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def render_markdown_table(lines: List[str]) -> str:
    rows: List[List[str]] = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells:
            rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:] if re.match(r"^\s*\|?\s*:?-{3,}:?", lines[1]) else rows[1:]
    th = "".join(f"<th>{inline_markdown(c)}</th>" for c in header)
    trs = [f"<tr>{th}</tr>"]
    for row in body:
        tds = "".join(f"<td>{inline_markdown(c)}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return '<div class="table-wrap"><table>' + "".join(trs) + "</table></div>"


def render_body(lines: Iterable[str]) -> str:
    source_lines = list(lines)
    blocks: List[str] = []
    para: List[str] = []
    list_items: List[str] = []
    ordered = False
    table_lines: List[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            blocks.append("<p>" + " ".join(inline_markdown(x.strip()) for x in para) + "</p>")
            para = []

    def flush_list() -> None:
        nonlocal list_items, ordered
        if list_items:
            tag = "ol" if ordered else "ul"
            blocks.append(f"<{tag}>" + "".join(list_items) + f"</{tag}>")
            list_items = []
            ordered = False

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            html_table = render_markdown_table(table_lines)
            if html_table:
                blocks.append(html_table)
            table_lines = []

    for raw in source_lines:
        line = raw.rstrip()
        is_table = line.strip().startswith("|") and line.strip().endswith("|")
        if is_table:
            flush_para()
            flush_list()
            table_lines.append(line)
            continue
        flush_table()

        if not line.strip():
            flush_para()
            flush_list()
            continue

        image = re.match(r"^\s*!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if image:
            flush_para()
            flush_list()
            alt = image.group(1).strip()
            src = html.escape(image.group(2).strip(), quote=True)
            caption = inline_markdown(alt) if alt else "Paper figure"
            blocks.append(
                '<figure class="image-card">'
                f'<img src="{src}" alt="{html.escape(alt, quote=True)}">'
                f'<figcaption>{caption}</figcaption>'
                '</figure>'
            )
            continue

        visual = re.match(r"^\s*>\s*\[visual\]\s*(.+)$", line, flags=re.IGNORECASE)
        if visual:
            flush_para()
            flush_list()
            blocks.append(
                '<div class="visual-card"><div class="visual-label">Visual</div>'
                f'<div class="visual-text">{inline_markdown(visual.group(1).strip())}</div></div>'
            )
            continue

        quote = re.match(r"^\s*>\s+(.+)$", line)
        if quote:
            flush_para()
            flush_list()
            blocks.append(f"<blockquote>{inline_markdown(quote.group(1).strip())}</blockquote>")
            continue

        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            flush_para()
            flush_list()
            blocks.append(f"<h3>{inline_markdown(h3.group(1).strip())}</h3>")
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        number = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or number:
            flush_para()
            is_ordered = bool(number)
            if list_items and ordered != is_ordered:
                flush_list()
            ordered = is_ordered
            item = (number or bullet).group(1).strip()  # type: ignore[union-attr]
            list_items.append(f"<li>{inline_markdown(item)}</li>")
            continue

        flush_list()
        para.append(line)

    flush_table()
    flush_para()
    flush_list()
    return "\n".join(blocks) if blocks else "<p></p>"


def render_slide(slide: Slide) -> str:
    title = inline_markdown(slide.title)
    body = render_body(slide.body_lines)
    return f"""<section>
  <h2>{title}</h2>
  {body}
</section>"""


def default_css() -> str:
    return """
    :root { --r-main-font-size: 30px; }
    .reveal h1, .reveal h2, .reveal h3 { text-transform: none; letter-spacing: -0.02em; }
    .reveal h2 { font-size: 1.55em; }
    .reveal h3 { font-size: 1.05em; opacity: 0.9; }
    .reveal p, .reveal li { line-height: 1.35; }
    .reveal ul, .reveal ol { width: 88%; }
    .reveal strong { color: inherit; }
    .reveal code { font-size: 0.85em; }
    .reveal blockquote { width: 86%; font-size: 0.82em; padding: 0.45em 0.8em; }
    .visual-card { width: 86%; margin: 0.8em auto 0; padding: 0.8em 0.9em; border: 2px dashed currentColor; border-radius: 18px; text-align: left; opacity: 0.92; }
    .visual-label { font-size: 0.55em; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.68; margin-bottom: 0.35em; }
    .visual-text { font-size: 0.78em; line-height: 1.32; }
    .image-card { margin: 0.7em auto 0; width: 86%; text-align: center; }
    .image-card img { max-width: 100%; max-height: 370px; object-fit: contain; border-radius: 14px; }
    .image-card figcaption { font-size: 0.48em; opacity: 0.72; margin-top: 0.35em; }
    .table-wrap { width: 92%; margin: 0.7em auto 0; }
    table { width: 100%; border-collapse: collapse; font-size: 0.58em; }
    th, td { border: 1px solid currentColor; padding: 0.35em 0.45em; }
    .footer { position: fixed; left: 24px; bottom: 14px; font-size: 13px; opacity: 0.55; z-index: 20; }
    """


def blue_white_css(font_pair: str) -> str:
    if font_pair == "comic-times":
        heading_font = '"Times New Roman", Times, serif'
        body_font = '"Times New Roman", Times, serif'
        accent_font = '"Comic Sans MS", "Comic Sans", cursive'
    else:
        heading_font = 'Georgia, "Times New Roman", serif'
        body_font = 'Arial, sans-serif'
        accent_font = 'Arial, sans-serif'

    return f"""
    :root {{
      --navy:#073763; --blue:#0b5ea8; --sky:#dceeff; --ice:#f5faff;
      --text:#102033; --muted:#617386; --line:#c6def7; --gold:#c49035;
      --r-main-font-size: 30px;
    }}
    body {{ background: linear-gradient(135deg,#f9fcff 0%,#e9f5ff 100%); }}
    .reveal {{ font-family: {body_font}; color: var(--text); }}
    .reveal .slides section {{ height: 100%; box-sizing: border-box; padding: 48px 64px; text-align: left; }}
    .reveal h1, .reveal h2 {{ font-family: {heading_font}; color: var(--navy); letter-spacing: -0.025em; text-transform: none; }}
    .reveal h2 {{ font-size: 1.34em; margin: 0 0 0.55em; border-bottom: 3px solid var(--line); padding-bottom: 0.25em; }}
    .reveal h3 {{ font-family: {accent_font}; color: var(--blue); font-size: 0.82em; margin: 0.45em 0 0.2em; text-transform: none; }}
    .reveal p, .reveal li {{ font-size: 0.72em; line-height: 1.28; color: var(--text); }}
    .reveal ul, .reveal ol {{ width: 88%; }}
    .reveal strong {{ color: var(--blue); font-weight: 900; }}
    .reveal code {{ font-size: 0.82em; color: var(--navy); }}
    .reveal blockquote {{ width: 86%; font-size: 0.72em; padding: 0.55em 0.8em; color: var(--navy); border-left: 8px solid var(--blue); background: white; box-shadow: 0 12px 34px rgba(14,76,129,.10); }}
    .visual-card {{ width: 86%; margin: 0.7em auto 0; padding: 0.75em 0.85em; border: 2px dashed var(--blue); border-radius: 18px; text-align: left; background: white; box-shadow: 0 12px 34px rgba(14,76,129,.10); }}
    .visual-label {{ font-family: {accent_font}; font-size: 0.48em; text-transform: uppercase; letter-spacing: 0.08em; color: var(--blue); margin-bottom: 0.3em; }}
    .visual-text {{ font-family: {accent_font}; font-size: 0.62em; line-height: 1.25; color: var(--navy); }}
    .image-card {{ margin: 0.55em auto 0; width: 90%; text-align: center; background: white; border: 1px solid var(--line); border-radius: 22px; padding: 0.45em; box-shadow: 0 12px 34px rgba(14,76,129,.11); }}
    .image-card img {{ max-width: 100%; max-height: 390px; object-fit: contain; border-radius: 12px; }}
    .image-card figcaption {{ font-family: {accent_font}; font-size: 0.42em; color: var(--muted); margin-top: 0.25em; }}
    .table-wrap {{ width: 92%; margin: 0.7em auto 0; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 12px 34px rgba(14,76,129,.10); }}
    th {{ background: var(--navy); color: white; font-family: {accent_font}; font-size: 0.55em; padding: 0.55em; }}
    td {{ font-size: 0.56em; padding: 0.55em; border-bottom: 1px solid var(--line); text-align: center; }}
    td:first-child {{ text-align: left; font-weight: 800; color: var(--navy); }}
    .footer {{ position: fixed; left: 24px; bottom: 14px; font-family: {accent_font}; font-size: 13px; color: var(--muted); z-index: 20; }}
    """


def build_html(title: str, slides: List[Slide], theme: str, style: str, font_pair: str, lang: str) -> str:
    rendered_slides = "\n".join(render_slide(slide) for slide in slides)
    safe_title = html.escape(title, quote=True)
    safe_theme = re.sub(r"[^a-zA-Z0-9_-]", "", theme) or "white"
    safe_lang = re.sub(r"[^a-zA-Z0-9_-]", "", lang) or "en"
    css = blue_white_css(font_pair) if style == "blue-white-academic" else default_css()
    return f"""<!doctype html>
<html lang="{safe_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/{safe_theme}.css" id="theme">
  <style>{css}</style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
{rendered_slides}
    </div>
  </div>
  <div class="footer">Generated with reveal.js</div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script>
    Reveal.initialize({{
      hash: true,
      slideNumber: true,
      controls: true,
      progress: true,
      center: true,
      transition: 'fade',
      width: 1280,
      height: 720,
      margin: 0.04
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="generate a reveal.js html deck from markdown")
    parser.add_argument("markdown", help="input markdown file")
    parser.add_argument("--out", default="paper_deck.html", help="output html file")
    parser.add_argument("--title", default="Paper Presentation", help="html document title")
    parser.add_argument("--theme", default="white", help="reveal.js theme name")
    parser.add_argument("--style", default="blue-white-academic", choices=["default", "blue-white-academic"], help="visual style preset")
    parser.add_argument("--font-pair", default="comic-times", choices=["default", "comic-times"], help="font preset")
    parser.add_argument("--lang", default="en", help="html lang attribute")
    args = parser.parse_args()

    in_path = pathlib.Path(args.markdown)
    if not in_path.exists():
        print(f"error: file not found: {in_path}", file=sys.stderr)
        return 2

    markdown = read_text(in_path)
    slides = parse_slides(markdown)
    if not slides:
        print("error: no slides found. use markdown headings like '## Slide Title'.", file=sys.stderr)
        return 3

    deck_title = args.title or extract_deck_title(markdown, "Paper Presentation")
    out_path = pathlib.Path(args.out)
    out_path.write_text(build_html(deck_title, slides, args.theme, args.style, args.font_pair, args.lang), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
