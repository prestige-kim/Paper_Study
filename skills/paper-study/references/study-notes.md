# Study Notes and Critical Review

Use this schema flexibly and apply the paper-type guidance in SKILL.md. Retain sections that help answer the user's request; omit irrelevant sections rather than filling them with generic text. A theoretical paper needs assumptions and proofs, a qualitative paper needs observations and analysis, and a review needs selection and synthesis; none requires an invented training pipeline.

## Standard study-note structure

### 1. Paper identity

- Full title, authors, venue/repository, year, DOI or arXiv ID, version date when relevant
- Paper type and primary task
- Source path or URL

### 2. One-minute brief

- Research problem
- One-sentence core idea
- Most important evidence or result with locator; include dataset, split, metric, and comparator when applicable
- Why the paper matters

### 3. Problem framing and contribution

- Background and specific gap
- Research question or hypothesis when explicit
- Contributions, separated into conceptual, methodological, empirical, and resource contributions
- A `claim → evidence` table for the paper's central claims

Recommended columns:

| Claim | Evidence type | Paper locator | Assessment |
|---|---|---|---|

Do not infer a formal hypothesis when the paper does not state one.

### 4. Method

Explain the applicable elements in dependency order:

1. Inputs, outputs, and task definition
2. Model components or analytical procedure
3. Data flow through training and inference
4. Objective functions and optimization
5. Design choices that differ from prior work

For theory, replace this flow with definitions → assumptions → statements → proof strategy → scope. For qualitative work, use sampling → collection → analysis → interpretation. For reviews, use search/selection → synthesis → conclusions. Do not force missing machine-learning fields into these papers.

For equations:

- reproduce only the minimum notation needed;
- define every symbol used in the explanation;
- explain the operational meaning and role in the method;
- distinguish the paper's derivation from an analyst-added supplementary derivation.

Use pseudocode or a flow diagram only when it makes a multi-stage process materially clearer.

### 5. Evidence

Use the experimental table below for empirical results. For theory, check what each conclusion follows from and which assumptions it needs; for qualitative work, connect themes to observations and methodological context; for reviews, distinguish the authors' synthesis from the cited studies' findings. Disclose when only a proof sketch, excerpt, or subset of the underlying evidence could be inspected.

Record enough context to interpret the result:

| Dataset/split | Task | Metric and direction | Baseline/comparator | Proposed result | Locator |
|---|---|---|---|---|---|

Then explain:

- preprocessing and data augmentation;
- training configuration and compute, when reported;
- baseline fairness and whether settings are comparable;
- main results, ablations, robustness, and error analysis;
- statistical uncertainty or repeated runs, when reported.

Never compare values from different datasets, splits, evaluation protocols, or model scales as if they were directly comparable.

### 6. Figures and tables that matter

For each central figure or table, state:

- what is encoded or compared;
- the pattern visible in the artifact;
- the conclusion the authors draw;
- whether the artifact supports that conclusion and what it does not establish.

Group repetitive artifacts. If visual inspection was unavailable, say so and limit the explanation to accessible captions or text.

### 7. Critical evaluation

Separate the following:

- **Author-stated limitations** with locators
- **Analyst critique** covering only relevant dimensions: assumptions, confounders, data leakage, baseline choice, evaluation coverage, statistical rigor, generalization, compute cost, reproducibility, fairness, privacy, or environmental impact
- **Open questions** that follow from the evidence

Criticism must identify the evidence or missing test that motivates it. Avoid generic statements such as “more experiments are needed.”

### 8. Reproduction checklist

For applicable items, use `reported`, `partially reported`, or `not reported` after checking the relevant material. Use `not verifiable from the available source` when that material is inaccessible; omit irrelevant items or mark them `not applicable` in a requested checklist.

For an empirical or computational study, check:

- dataset source, licensing, and exact split
- preprocessing and augmentation
- architecture and initialization
- objective and regularization
- optimizer, schedule, batch size, and epochs/steps
- random seeds and repeated runs
- hardware, training time, and memory/compute
- evaluation code and protocol
- code, checkpoints, and dependency versions

For theory, check definitions, assumptions, proof availability, and any computational verification. For qualitative work, check sampling, collection protocol, analysis/coding, and access restrictions. For reviews, check search date, sources, inclusion criteria, selection, and synthesis procedure. Respect participant confidentiality and source access restrictions.

Conclude with the largest reproduction risks and a practical first implementation plan when requested.

### 9. Research lineage and application

- Essential prerequisite works only
- What this paper changes relative to the closest baseline
- Which later directions it plausibly enables; use external sources only when requested or needed, and label them
- Suitable and unsuitable application scenarios

### 10. Learning aids

Choose aids proportional to the paper:

- a compact glossary of genuinely nontrivial terms;
- a hierarchical concept map or method flow;
- the smallest useful set of self-test questions that covers the relevant learning goals among mechanism, evidence, comparison, critique, and transfer;
- concise answers placed after the questions so the learner can self-test first;
- an “explain it without jargon” or “design an ablation” prompt when it adds a learning dimension not already tested.

Questions should require understanding of why the method works and what the experiments establish, not memorization of headings or isolated numbers.
