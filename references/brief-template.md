# Paper Spotlight Brief Template

Use this template when the user asks for the fixed paper briefing format.

## 1. Title + One-line Takeaway

**Title:** <exact paper title>

**One-line Takeaway:** We solve <X problem> by <Y idea>, achieving <Z improvement/evidence>.

Notes:
- Keep author, unit, and venue metadata minimal unless the user asks.
- The one-line takeaway must contain the problem, idea, and benefit.

## 2. Motivation / Problem

**Why this problem matters:** <why the task is worth solving>

**Pain point of current methods:** <specific limitation in prior methods>

**Why it is serious in practice:** <deployment, scale, domain shift, cost, safety, robustness, ambiguity, or other real setting>

**Failure case / motivating example:** <figure/table/page reference if available; otherwise describe a simple visual to create>

Takeaway for this section: <one sentence that makes the audience agree the problem exists>

## 3. Key Insight

**Observation:** <what the paper observes about prior methods, data, task structure, or failure cases>

**Insight:** <the simple principle behind the paper>

**Proposed direction:** <how the method turns the insight into an approach>

**Simple diagram idea:** <one conceptual diagram, not a complex architecture>

Example phrasing:

> Existing methods suffer from <A>. The paper observes <B>. Therefore, it proposes <C>.

## 4. Method Overview

**Input:** <input data / model input>

**Core module 1:** <name and role>

**Core module 2:** <name and role>

**Output / loss:** <prediction, training objective, or optimization target>

**One key formula, if necessary:** <only one formula; explain what it optimizes>

**Why this design follows the insight:** <link the framework back to Section 3>

## 5. Results + Takeaway

**Datasets/settings:** <datasets and protocols>

**Baselines:** <main compared methods>

**Metrics:** <metrics>

**Main result:** <best-supported quantitative finding with table/figure reference>

**Ablation / qualitative support:** <evidence that validates the key insight>

**Concern or limitation:** <missing comparisons, limited settings, weak evidence, unclear reproducibility>

**Final takeaway:** <what the audience should remember>

## Optional Reviewer-style Add-on

**Pros:**
- <pro 1>
- <pro 2>

**Cons:**
- <con 1>
- <con 2>

**Questions for authors:**
1. <question>
2. <question>
3. <question>

## Optional Visual HTML PPT Add-on

Use this add-on when the user asks for a styled HTML PPT or browser presentation.

**Visual style:** blue-white academic palette.

**Font pair:** Times New Roman for academic text; Comic Sans MS only for handwritten-style callouts, tags, arrows, and short annotations.

**Figure plan:**
- Slide 1 or 2: motivating figure / failure case.
- Slide 4: framework diagram.
- Slide 5: module diagram or one key formula.
- Results slide: compact table recreated from the paper, not a raw oversized screenshot unless necessary.

**Language rule:** use English-only slide text if the user says no Chinese, asks for an English deck, or requests a conference-style paper talk.
