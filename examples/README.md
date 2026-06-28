# Examples

A minimal, end-to-end example of the deck workflow.

> **Note:** [`sample_brief.md`](sample_brief.md) summarizes a **fictional** paper. It exists only to
> demonstrate the markdown format and the generator script. When the skill runs for real, every
> slide is grounded in the actual source PDF.

## Files

| File | What it is |
|---|---|
| [`sample_brief.md`](sample_brief.md) | A `paper_brief.md`-style input following `references/reveal-template.md` |
| `sample_deck.html` | The reveal.js deck generated from `sample_brief.md` (open in a browser) |

## Regenerate the deck

From the repository root:

```bash
python scripts/generate_reveal_deck.py examples/sample_brief.md \
  --out examples/sample_deck.html \
  --title "Decoupling Geometry and Appearance" \
  --style blue-white-academic \
  --font-pair comic-times \
  --lang en
```

Then open `examples/sample_deck.html` in any modern browser. It loads reveal.js from a CDN, so
internet access is needed when viewing.

## What this demonstrates

- The 6-slide spotlight structure: title → motivation → key insight → method → (formula) → results.
- Markdown features supported by the generator: `## Slide` headings, bullets, `**bold**`, inline
  `` `code` ``, `> [visual] ...` placeholder cards, and pipe tables.
- The default blue-white academic style with the Times New Roman + Comic Sans MS font pair.
