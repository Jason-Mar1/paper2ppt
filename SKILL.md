---
name: paper-pdf-brief
description: "read academic paper pdfs or paper pdf links and produce faithful spotlight-style paper briefings, review notes, presentation outlines, or browser-ready html/reveal.js paper ppt decks. use when the user asks to read, summarize, explain, review, present, or turn a research paper into slides. also use for html ppt, webpage slides, reveal.js, paper talk pages, visual academic decks, blue-white academic styling, paper figure extraction, english-only slides, or decks using times new roman and comic sans ms. for slide decks, guide a two-step workflow: first confirm the outline and style choices, then generate the final html; if the user explicitly asks to generate directly, proceed with sensible defaults. supports uploaded pdfs, arxiv or publisher pdf links, and file-library papers."
---

# Paper PDF Brief

## Core behavior

Read the paper before writing. Base every claim on the uploaded PDF, accessible PDF link, or cited paper content. Do not invent missing results, baselines, datasets, equations, limitations, or author claims.

For normal explanations, match the user's language. For paper slide decks, especially HTML PPT / reveal.js decks, prefer polished English unless the user explicitly asks for Chinese or bilingual slides. If the user says the deck should not contain Chinese, ensure every visible slide label, footer, caption, and note is English-only.

Default spotlight structure:

1. **Title + One-line Takeaway**
2. **Motivation / Problem**
3. **Key Insight**
4. **Method Overview**
5. **Results + Takeaway**

Use `references/brief-template.md` when the user wants a polished reusable briefing. Use `references/reveal-template.md` when the user asks for reveal.js, HTML slides, webpage PPT, browser-based presentation, a shareable paper talk page, or a visually styled academic deck.

## Input handling

- If the user provides an uploaded PDF, analyze that file.
- If the user provides an arXiv, OpenReview, publisher, or project URL, use web access to obtain the paper page or PDF when available.
- If the user refers to a previous upload or file name, search the file library before asking for the file again.
- If no paper source is available, ask the user to upload the PDF or provide a paper link.
- If the PDF appears scanned or extraction is incomplete, inspect rendered pages or screenshots before concluding that information is unavailable.

## Reading workflow

1. Identify the exact title, problem setting, task definition, abstract claim, method claim, and main empirical claim.
2. Read the abstract, introduction, method, experiments, conclusion, and figure/table captions.
3. Find the most important failure case, motivating example, or qualitative comparison. Use it for the Motivation / Problem slide when available.
4. Distill the key insight as an observation-to-solution pair: "Existing methods suffer from A; the paper observes B; therefore it proposes C."
5. Cross-check the method description against experiments: make sure each claimed contribution is evaluated or mark it as weakly supported.
6. Mark uncertainty explicitly when a result or detail is not visible in the provided paper.

## Two-step deck workflow

Use this workflow for HTML PPT, reveal.js decks, webpage slides, paper talk pages, and polished visual paper presentations. The default behavior is collaborative: first decide the story, then generate the artifact.

### Step 1: Outline and style checkpoint

After reading the paper, first return a concise proposed deck outline unless the user explicitly says to generate directly. Use `references/outline-checkpoint.md` as the response pattern.

The checkpoint must include:

- **Deck goal:** spotlight, full talk, rebuttal, teaching, review, or project page.
- **Slide outline:** 5-7 slides with one main message per slide.
- **Visual plan:** which paper figures/tables to use and where.
- **Style choices:** color palette, language, font pair, density, and whether to use paper figures or redrawn diagrams.
- **Default recommendation:** choose a complete default style so the user can simply say "generate".
- **One direct question:** ask the user to confirm or modify style/outline. Do not ask many questions.

When the user already expressed preferences, carry them forward instead of re-asking. For example, remember preferences such as blue-white academic style, English-only, Times New Roman, Comic Sans MS callouts, and actual paper figures.

### Step 2: Generate final HTML

Generate the HTML deck only after one of these is true:

- The user approves the outline/style checkpoint.
- The user asks for changes and then asks to generate.
- The initial request explicitly says to directly generate, skip questions, make it now, or similar.

If the user asks to directly generate, do not pause for the checkpoint. Use the skill defaults and produce the HTML artifact in one pass.

During generation:

1. Extract or select useful paper figures when available.
2. Build `paper_brief.md` from the approved outline.
3. Convert it into reveal.js HTML.
4. Return the `.html` file link and briefly state the chosen style.


For local PDF text extraction, optionally run:

```bash
python scripts/extract_pdf_text.py input.pdf --out extracted_paper.md
```

Use extracted text as a starting point, not as the only source. For tables, figures, diagrams, or failure cases, inspect the PDF visually when needed.

## Visual HTML PPT generation details

Use these implementation steps during Step 2.

1. Extract useful figures before drafting the deck when visuals would help. Prefer actual paper figures over generic placeholders.

```bash
python scripts/extract_pdf_figures.py input.pdf --out paper_figures --render-pages 1,3,4 --extract-images
```

2. Draft a `paper_brief.md` file using the approved Step 1 outline and `references/reveal-template.md`.
3. Include image lines for extracted figures using standard markdown syntax:

```markdown
![Figure 1: motivating domain gap](paper_figures/p01_img01.png)
```

4. Convert the markdown to a standalone reveal.js HTML deck. For the user's preferred style from iteration, use:

```bash
python scripts/generate_reveal_deck.py paper_brief.md --out paper_deck.html --title "Paper Presentation" --style blue-white-academic --font-pair comic-times --lang en
```

5. Return the generated `.html` file. Mention that it opens directly in a browser and uses reveal.js from a CDN by default.

### Visual deck defaults learned from iteration

When the user asks for a polished HTML PPT and does not specify otherwise:

- Use a blue-white academic palette: navy headings, white cards, light-blue backgrounds, thin blue borders.
- Use **Times New Roman** for paper-like academic titles and most body text.
- Use **Comic Sans MS** sparingly for handwritten-style labels, tags, short callouts, arrows, and informal annotations. Do not use it for dense paragraphs.
- Do not bundle or share font files. Use CSS font-family declarations only.
- Prefer an English-only deck for academic presentation pages unless the user asks for Chinese.
- Include 4-7 slides for a spotlight talk: title, motivation, insight, method/framework, core modules or formula, results, final takeaway/limitation.
- Add actual paper figures when available: Figure 1 for motivation, framework diagram for method, module diagrams for core module slides, and table-derived compact results for evidence.
- Keep each slide focused: one idea, 3-5 bullets, concise captions, and paper-specific evidence.
- Avoid screenshot-heavy slides unless the figure is central. Crop or choose the most relevant figures when possible.

## Reveal.js slide defaults

- Slide 1: exact title plus one-line takeaway. Do not overload the slide with authors, affiliations, or venue information unless the user asks.
- Slide 2: motivation/problem. Explain why the problem matters, why current methods fail, and include one failure-case visual placeholder or figure when possible.
- Slide 3: key insight. This is the most important slide. Present the observation-to-solution logic before any network architecture.
- Slide 4: method overview. Show only the main framework: input, core module 1, core module 2, output/loss. Include at most one key formula and explain what it optimizes.
- Slide 5: results plus takeaway. Summarize datasets, metrics, main improvements, ablations, and the final message.

If the user asks for a `.pptx`, use the presentation artifact workflow instead of only generating HTML. If they explicitly request reveal.js or HTML, prioritize HTML reveal.js output.

## Section guidance

### Title + One-line Takeaway

Explain the whole paper in one sentence using this pattern whenever possible:

> We solve X problem by Y idea, achieving Z improvement.

Rules:

- Use the exact paper title when visible.
- Do not spend much space on authors, affiliations, or conference metadata.
- The takeaway must state the problem, core idea, and benefit.
- Avoid vague phrases such as "this paper proposes a novel method" unless followed by the actual idea.

### Motivation / Problem

Make the audience agree that the problem is real before introducing the method.

Answer:

- Why is this problem worth solving?
- What pain point do current methods have?
- Why is that pain point serious in realistic settings?
- What failure case best demonstrates the problem?

Preferred structure:

1. Current methods suffer from a specific limitation.
2. The limitation becomes severe in real-world use, deployment shift, scale, annotation cost, ambiguity, or robustness.
3. A failure case or qualitative example shows the gap.

Use one figure or visual placeholder when possible. The slide should build consensus, not advertise the proposed method too early.

### Key Insight

This is the most important slide. Do not start with a complex network diagram.

Present the logic as:

- **Observation A:** what the paper notices about the task, data, failure mode, or prior methods.
- **Insight B:** the simple principle that follows from that observation.
- **Proposed direction C:** how the method operationalizes that principle.

Example style:

> Existing methods mix geometry and appearance, causing poor cross-domain generalization. The key insight is to decouple geometry from appearance so that transferable structure and domain-specific style can be modeled separately.

Use a simple conceptual diagram or visual placeholder to express the idea.

### Method Overview

Only explain the main framework. Do not list every module or implementation detail.

Recommended structure:

- **Input:** what enters the system.
- **Core module 1:** first essential mechanism and why it exists.
- **Core module 2:** second essential mechanism and why it exists.
- **Output / loss:** what the system predicts or optimizes.

If formulas are needed, include only one key formula. Explain the formula in plain language: what variables mean and what the objective encourages.

### Results + Takeaway

Summarize evidence rather than listing every number.

Cover:

- Datasets and settings.
- Baselines or comparison methods.
- Metrics.
- Main quantitative result and the most important improvement.
- Ablation or qualitative evidence that supports the key insight.
- Any obvious weakness, missing baseline, limited setting, or weak experimental design.

End with one final takeaway sentence that tells the audience what to remember.

## Quality rules

- Prefer concise, high-signal summaries over paragraph-by-paragraph retelling.
- Use bullets for readability, but keep each bullet substantive.
- Preserve technical terms, dataset names, metric names, module names, and table numbers exactly when visible.
- Cite page numbers, section names, table numbers, or figure numbers when possible.
- Never claim experiments exist unless they are actually in the paper.
- When using extracted figures, caption them with the original figure number when visible.
- When the user asks for a review, include quality, clarity, originality, and significance, but still ground comments in the paper.
- When generating reveal.js slides, do not paste full paragraphs from the paper; synthesize short slide bullets.
- For spotlight-style presentations, prioritize story flow: problem consensus -> insight -> framework -> evidence.

## Output modes

Use the default spotlight structure unless the user asks for one of these modes:

- **brief:** 1-2 bullets per slide/section.
- **detailed teaching:** add background, formulas, and step-by-step explanation.
- **review:** emphasize strengths, weaknesses, questions for authors, and score rationale.
- **presentation outline:** convert each section into slide titles and speaking notes.
- **reveal.js deck:** generate a browser-ready HTML slide deck with `scripts/generate_reveal_deck.py`.
- **visual html ppt:** use the two-step outline-then-html workflow; extract figures, use blue-white academic styling by default, and generate a browser-ready reveal.js deck after approval or direct-generation instruction.
