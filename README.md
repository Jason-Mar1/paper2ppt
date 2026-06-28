<div align="center">

<img src="assets/icon.svg" alt="Paper PDF Brief" width="96" height="96" />

# Paper PDF Brief

**Turn research-paper PDFs into faithful spotlight briefings, review notes, and browser-ready reveal.js slide decks.**

[![Skill](https://img.shields.io/badge/type-AI%20skill-0B5EA8)](SKILL.md)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)](#requirements)
[![reveal.js](https://img.shields.io/badge/output-reveal.js-1f6feb)](https://revealjs.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<a href="https://github.com/Jason-Mar1/paper2ppt">github.com/Jason-Mar1/paper2ppt</a>

</div>

---

## Overview

Paper PDF Brief is an AI **skill** that reads an academic paper (uploaded PDF, arXiv/publisher link, or a paper from your file library) and produces a faithful, spotlight-style output:

- A polished **paper briefing** or **review note**
- A **presentation outline** with speaking notes
- A browser-ready **HTML / reveal.js slide deck** with a blue-white academic look

The guiding principle is **faithfulness**: every claim is grounded in the actual paper. The skill never invents results, baselines, datasets, equations, or limitations.

> The full behavior contract lives in [`SKILL.md`](SKILL.md). This README is the project entry point and quick-start guide.

## Using it as a skill

This repository is packaged as an **AI skill**, not a standalone app. The model reads [`SKILL.md`](SKILL.md) to learn when and how to act, and runs the helper scripts in [`scripts/`](scripts/) when it needs PDF text, figures, or an HTML deck.

To use it, install the skill into a compatible assistant (the interface metadata in [`agents/openai.yaml`](agents/openai.yaml) targets ChatGPT, Codex, the API, and Atlas), then simply ask:

- "Read this paper and give me a spotlight brief." (attach a PDF or paste an arXiv link)
- "Turn this paper into reveal.js slides." → the skill proposes an outline + style, then generates the HTML.
- "Just generate the deck directly, English-only, blue-white academic." → skips the checkpoint and builds it in one pass.

The skill triggers automatically when you ask to read, summarize, explain, review, present, or turn a research paper into slides.

> **Privacy:** the helper scripts run locally — your PDF is parsed on your machine and is not uploaded anywhere. The only external request is the generated deck loading reveal.js from a CDN, so internet access is needed when *viewing* the slides, not when creating them.

## Installation

This project follows the **Agent Skills** format: a folder containing a `SKILL.md` with `name` + `description` frontmatter. Install it by placing that folder where your assistant discovers skills. The skill name is **`paper-pdf-brief`**, so name the installed folder `paper-pdf-brief`.

First, get the files:

```bash
git clone https://github.com/Jason-Mar1/paper2ppt.git
```

### Option A — Claude Code

Copy the repo into a skills directory. Claude Code picks it up live (no restart needed).

- **User / global** (available in every project): `~/.claude/skills/paper-pdf-brief/`
- **Project-scoped** (shared with a repo): `.claude/skills/paper-pdf-brief/`

macOS / Linux:

```bash
mkdir -p ~/.claude/skills/paper-pdf-brief
cp -r paper2ppt/* ~/.claude/skills/paper-pdf-brief/
```

Windows (cmd):

```cmd
mkdir "%USERPROFILE%\.claude\skills\paper-pdf-brief"
xcopy /E /I paper2ppt "%USERPROFILE%\.claude\skills\paper-pdf-brief"
```

Verify by asking Claude to "turn a paper PDF into slides" — it should invoke the `paper-pdf-brief` skill. Make sure `SKILL.md` sits at the root of the installed folder.

### Option B — Claude.ai / Claude Desktop

1. Zip the repository contents so that `SKILL.md` is at the top level of the archive.
2. Enable **Skills** in Settings → Capabilities (and code execution, if prompted).
3. Upload the zip under the Skills section. Teams can upload it under Organization settings → Skills to share it across the workspace.

### Option C — Codex

The interface metadata in [`agents/openai.yaml`](agents/openai.yaml) targets ChatGPT, Codex, the API, and Atlas. For Codex, place the folder in a skills directory:

- **User**: `~/.codex/skills/paper-pdf-brief/`
- **Admin / managed**: `/etc/codex/skills/paper-pdf-brief/`

```bash
mkdir -p ~/.codex/skills/paper-pdf-brief
cp -r paper2ppt/* ~/.codex/skills/paper-pdf-brief/
```

### Install the Python dependencies

The helper scripts (PDF text/figure extraction) need a couple of packages. Run this once in the installed skill folder:

```bash
pip install -r requirements.txt
```

`generate_reveal_deck.py` itself has no third-party dependencies.

## Showcase

<!-- Replace this placeholder with a real screenshot of a generated deck, e.g. assets/demo-deck.png -->
<div align="center">

*A blue-white academic reveal.js deck generated from a paper PDF.*

<!-- ![Example generated deck](assets/demo-deck.png) -->
<sub>Add a screenshot at <code>assets/demo-deck.png</code> and uncomment the image line above.</sub>

</div>

## Features

- **Read-before-write** — distills title, motivation, key insight, method, and results straight from the source PDF.
- **Spotlight structure** — Title + one-line takeaway → Motivation → Key insight → Method → Results + takeaway.
- **Two-step deck workflow** — first confirm an outline and style, then generate the final HTML (or generate directly on request).
- **Blue-white academic styling** — navy headings, white cards, light-blue backgrounds; Times New Roman for body text and Comic Sans MS for handwritten-style callouts.
- **Real paper figures** — extract or render figures from the PDF and embed them in the deck.
- **English-first decks** — slide text defaults to English; switch to other languages on request.
- **Multiple output modes** — `brief`, `detailed teaching`, `review`, `presentation outline`, `reveal.js deck`, `visual html ppt`.

## Repository layout

```
paper2ppt/
├── SKILL.md                       # Skill definition and behavior contract
├── README.md                      # Project entry point (this file)
├── LICENSE                        # MIT license
├── requirements.txt               # Python dependencies for the scripts
├── .gitignore                     # Ignores generated decks, figures, caches
├── agents/
│   └── openai.yaml                # Agent interface + policy metadata
├── assets/
│   └── icon.svg                   # Skill icon
├── references/
│   ├── brief-template.md          # Reusable paper briefing template
│   ├── outline-checkpoint.md      # Step 1: outline/style confirmation pattern
│   └── reveal-template.md         # Step 2: reveal.js deck template
└── scripts/
    ├── extract_pdf_text.py        # Extract page-delimited text from a PDF
    ├── extract_pdf_figures.py     # Render pages / extract embedded figures
    └── generate_reveal_deck.py    # Convert markdown → standalone reveal.js HTML
```

Plus an [`examples/`](examples/) directory with a ready-to-run sample brief and its generated deck.

## Requirements

- Python 3.8+
- For PDF text extraction: [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`), with a fallback to [`pypdf`](https://pypdf.readthedocs.io/) / `PyPDF2`
- For figure extraction / page rendering: **PyMuPDF is required**
- Deck generation has **no runtime dependencies** — the generated HTML loads reveal.js from a CDN (internet access needed when viewing)

```bash
pip install -r requirements.txt
```

> `generate_reveal_deck.py` itself needs no third-party packages; the dependencies above are only for the PDF text/figure extraction scripts.

> To install the skill into Claude Code, Claude.ai, or Codex, see [Installation](#installation) above.

## Quick start

### 1. Extract paper text (optional starting point)

```bash
python scripts/extract_pdf_text.py input.pdf --out extracted_paper.md
```

| Argument | Default | Description |
|---|---|---|
| `pdf` | — | Input PDF path (required) |
| `--out` | `extracted_paper.md` | Output markdown text path |

### 2. Extract or render figures

```bash
python scripts/extract_pdf_figures.py input.pdf \
  --out paper_figures \
  --render-pages 1,3,4 \
  --extract-images
```

| Argument | Default | Description |
|---|---|---|
| `pdf` | — | Input PDF path (required) |
| `--out` | `paper_figures` | Output directory |
| `--render-pages` | `""` | Pages to render as PNG, e.g. `1,3,4` or `1-3` |
| `--dpi` | `180` | DPI for rendered pages |
| `--extract-images` | off | Extract embedded bitmap images |
| `--min-width` | `250` | Minimum embedded image width |
| `--min-height` | `180` | Minimum embedded image height |

### 3. Generate a reveal.js deck

Write a `paper_brief.md` using [`references/reveal-template.md`](references/reveal-template.md) (use `## Slide Title` headings and standard markdown for bullets, tables, blockquotes, and `![caption](path)` images), then:

```bash
python scripts/generate_reveal_deck.py paper_brief.md \
  --out paper_deck.html \
  --title "Paper Presentation" \
  --style blue-white-academic \
  --font-pair comic-times \
  --lang en
```

| Argument | Default | Description |
|---|---|---|
| `markdown` | — | Input markdown file (required) |
| `--out` | `paper_deck.html` | Output HTML file |
| `--title` | `Paper Presentation` | HTML document title |
| `--theme` | `white` | reveal.js theme name |
| `--style` | `blue-white-academic` | Visual preset: `default` or `blue-white-academic` |
| `--font-pair` | `comic-times` | Font preset: `default` or `comic-times` |
| `--lang` | `en` | HTML `lang` attribute |

Open the resulting `paper_deck.html` in any modern browser.

## How the slide workflow works

1. **Read the paper** and identify the exact title, problem, key insight, method, and main empirical claim.
2. **Step 1 — Outline checkpoint:** propose a 5–7 slide outline, a figure plan, and a default style, then ask one confirmation question. (See [`references/outline-checkpoint.md`](references/outline-checkpoint.md).)
3. **Step 2 — Generate:** after approval (or on a direct-generate request), extract figures, build `paper_brief.md`, and convert it to a standalone reveal.js HTML deck.

## Markdown supported by the deck generator

`generate_reveal_deck.py` is intentionally dependency-light and supports:

- `## Title` → a new slide; `---` → manual slide break
- `###` subheadings, `-`/`*`/`+` bullets, and numbered lists
- `**bold**`, `*italic*`, `` `code` ``, and `[links](url)`
- `![caption](path)` images rendered as captioned figure cards
- `> [visual] description` blockquote → dashed "Visual" placeholder card
- Standard pipe `| table | rows |`

## Examples

The [`examples/`](examples/) directory contains a complete, runnable sample:

- [`examples/sample_brief.md`](examples/sample_brief.md) — a `paper_brief.md`-style input (fictional paper, for format demonstration only).
- `examples/sample_deck.html` — the reveal.js deck generated from it.

Regenerate it from the repo root:

```bash
python scripts/generate_reveal_deck.py examples/sample_brief.md \
  --out examples/sample_deck.html \
  --title "Decoupling Geometry and Appearance" \
  --style blue-white-academic --font-pair comic-times --lang en
```

## License

Released under the [MIT License](LICENSE).

## Acknowledgements

- Slides are powered by [reveal.js](https://revealjs.com/).
- PDF parsing uses [PyMuPDF](https://pymupdf.readthedocs.io/) with a [`pypdf`](https://pypdf.readthedocs.io/) fallback.
