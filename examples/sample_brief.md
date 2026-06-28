# Decoupling Geometry and Appearance for Robust Cross-Domain Recognition

> NOTE: This is a fictional, illustrative example used only to demonstrate the deck
> format and the generator script. It does not summarize any real paper. When the
> skill runs for real, every slide is grounded in the actual source PDF.

## Title + One-line Takeaway

**Title:** Decoupling Geometry and Appearance for Robust Cross-Domain Recognition

**One-line Takeaway:** We solve *cross-domain generalization failure* by *separating transferable geometric structure from domain-specific appearance*, achieving *+8.4 mIoU over the strongest baseline on unseen domains*.

> [visual] Teaser: same object, three domains (sim, day, night) — geometry stays stable while appearance shifts dramatically.

## Motivation / Problem

- **Why worth doing:** recognition models must work in deployment domains never seen during training.
- **Pain point:** current methods entangle geometry and appearance, so a change in lighting or style collapses accuracy.
- **Why serious:** in real deployment, domain shift is the norm, not the exception — retraining per domain is costly.
- **Failure case:** a model trained on daytime imagery misclassifies the same scene at night despite identical geometry.

> [visual] Failure case: prediction map degrades from clean (day) to fragmented (night).

## Key Insight

- **Observation:** geometry transfers across domains; appearance does not.
- **Insight:** if the two are modeled separately, the transferable part can be reused while the domain-specific part is re-estimated cheaply.
- **Proposed direction:** factor the representation into a geometry stream and an appearance stream with a consistency constraint.
- **Message:** decouple what transfers from what does not.

> [visual] Insight diagram: entangled features -> split into [geometry | appearance] -> robust transfer.

## Method Overview

- **Input:** a single RGB image.
- **Core module 1 — Geometry encoder:** extracts domain-invariant structural features.
- **Core module 2 — Appearance adapter:** lightweight, re-estimated per target domain.
- **Output / loss:** segmentation prediction supervised by a cross-domain consistency objective.

### Key formula

`L = L_task + λ · L_consistency(G(x_s), G(x_t))`

Explain in one sentence: the consistency term encourages the geometry encoder `G` to produce matching structure across source and target domains.

## Results + Takeaway

- **Setup:** trained on Sim, evaluated on Day / Night / Rain unseen domains.
- **Main result:** +8.4 mIoU over the strongest prior method on the hardest (Night) split.
- **Ablation:** removing the consistency loss drops gains by ~5 mIoU, supporting the decoupling insight.
- **Limitation:** appearance adapter still needs a small unlabeled target set.
- **Final takeaway:** separating geometry from appearance is a simple, strong recipe for cross-domain robustness.

| Setting | Method | mIoU | Takeaway |
|---|---|---|---|
| Sim → Night | Baseline | 41.2 | entangled features fail |
| Sim → Night | Ours | 49.6 | +8.4 from decoupling |
| Sim → Night | Ours (no consistency) | 44.5 | ablation confirms the insight |
