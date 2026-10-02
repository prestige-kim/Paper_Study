# Cross-Paper Comparison and Literature Synthesis

Use this workflow for two or more papers. Comparison starts only after resolving the exact versions and extracting evidence from each paper.

## Normalize before comparing

For each paper, capture the applicable fields below. For theory, normalize assumptions and conclusion scope; for qualitative work, sampling, context, and analysis; for reviews, selection criteria and coverage. Omit irrelevant computational or experimental fields.

- research problem and scope;
- task definition and supervision;
- datasets, splits, preprocessing, and data scale;
- backbone or core method;
- training objective and inference procedure;
- parameter count, FLOPs, latency, hardware, or training compute when reported;
- metrics, their direction, and evaluation protocol;
- central result and exact locator;
- author-stated limitations and analyst critique.

Use `not reported` instead of estimating missing applicable values after inspecting the relevant material. Use `not verifiable from the available source` when access is incomplete, and `not applicable` for unrelated fields. Do not compare a full-text paper with an abstract-only source as though coverage were equal.

## Comparability rules

- Directly rank quantitative results only when dataset, split, metric, protocol, and relevant model scale match.
- When settings differ, describe the result as contextual evidence rather than a leaderboard.
- Separate architectural improvement from gains caused by additional data, pretraining, augmentation, search, ensembling, or compute.
- Do not treat publication chronology as proof of conceptual influence; use citations or explicit statements for lineage claims.
- Distinguish contemporary baselines available to the authors from later retrospective comparisons.

## Recommended synthesis

1. **Scope statement:** What question the comparison can and cannot answer.
2. **Evolution map:** Predecessor → limitation → new idea → remaining limitation.
3. **Normalized comparison table:** Method, data, supervision, objective, evaluation, efficiency, and evidence.
4. **Result table:** Only directly comparable results; place non-comparable findings in a separate contextual table.
5. **Trade-off analysis:** Accuracy, data needs, compute, latency, robustness, interpretability, and reproduction burden as relevant.
6. **Scenario-based conclusion:** Which method fits which use case and why; avoid declaring a universal winner without evidence.
7. **Study sequence:** Prerequisites and the most efficient reading order.
8. **Open research questions:** Gaps exposed by the comparison.

Attach source locators to every central quantitative comparison and important lineage claim.
