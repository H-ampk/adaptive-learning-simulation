# Research Design

## Purpose

This repository studies how differences in knowledge-tracing prediction quality propagate through question ranking, question selection, and simulated learning utility.

```text
Prediction
    ↓
Ranking
    ↓
Selection
    ↓
Learning Utility
```

The study is separated from the ConceptBook application so the experimental specification can stay fixed while ConceptBook continues to change.

## Scope

The objects of comparison are learner models and the policies that consume their predictions or state estimates. Candidate models include BKT, PFA, and HLR. Current ConceptBook Weighting is a non-model baseline, reproduced from a frozen specification rather than imported from ConceptBook.

The generative learner that simulates practice and answers is a separate component. It is not identified with any model under evaluation. See [generative-learner.md](generative-learner.md).

Policies that turn a prediction or state estimate into a ranking and a selection are also separate from the learner model. That mapping is not yet specified. See [policies.md](policies.md).

Metrics are organized in four layers that match the propagation path. A single custom propagation rate is not defined. See [metrics.md](metrics.md).

## What a simulation result means

A run estimates quantities inside a declared generative world. Agreement across worlds is evidence that a pattern is robust to those assumptions. A result in one world is not a measurement of human learning, and it is not a claim that one knowledge-tracing model should replace another in ConceptBook.

## Research questions

### RQ1 — Prediction

How much do models such as BKT, PFA, and HLR differ in predictive accuracy and in the accuracy of their latent-state estimates?

Candidate metrics:

- Brier Score
- Log Loss
- AUC
- Calibration Error
- State RMSE
- State MAE

### RQ2 — Ranking

How far does a difference in prediction quality change the ranking of candidate questions?

Candidates:

- Spearman correlation
- Kendall's tau
- Top-k overlap
- Rank displacement

### RQ3 — Selection

How far does a ranking difference become a difference in the question that is actually selected?

Candidates:

- Top-1 agreement
- Top-k Jaccard similarity
- Selection disagreement rate
- Selection regret

### RQ4 — Learning Utility

How far does a selection difference become a difference in simulated learning efficiency?

Primary candidate:

- Trials to Mastery

Secondary candidates:

- Time to Mastery
- Retention
- Final Mastery
- Wasted Practice Ratio
- Neglected Concept Rate
- Cumulative Selection Regret

### RQ5 — Propagation

At each step from prediction to ranking, selection, and utility, how much of the upstream difference is preserved, amplified, or attenuated?

This question is answered by comparing the layer-wise metrics above. A separate propagation-rate formula is intentionally undefined until those comparisons show what summary would be interpretable.

### RQ6 — Saturation

Is there a region in which further improvement in prediction quality yields little or no improvement in pedagogical utility?

## Hypotheses

These are candidate hypotheses, not findings.

### H1

A difference in prediction does not propagate completely into a difference in ranking.

### H2

A difference in ranking does not propagate completely into a difference in selection.

### H3

Not every difference in selection becomes a difference in learning utility.

### Central hypothesis

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

This inequality is the claim under test. It is not a conclusion of the study, and it is not assumed when worlds, policies, or metrics are defined.

## Relationship to ConceptBook

```text
ConceptBook
    ↓
Current Weighting specification
    ↓
adaptive-learning-simulation
    ↓
independent reproduction
    ↓
comparison with other policies
```

ConceptBook contributes the current weighting specification that this repository will copy, freeze, and reimplement. The application is not a runtime dependency. Conformance tests, added when the reproduction exists, will check that the frozen copy matches the specification recorded for the paper.

The version evaluated in a paper stays fixed here. Later edits to ConceptBook do not change that version and cannot make the reported comparison unreproducible.

The recorded weighting rules are in [policies.md](policies.md). They are documentation only. The baseline is not implemented in this change.

## Components that must stay distinct

```text
Generative world
    simulated learning and answers

Learner model
    prediction and state estimate from observed history

Policy
    ranking and selection from that estimate, or from a non-model rule
```

Using one of BKT, PFA, or HLR as the data-generating process would couple the world to a model under test. The generative learner therefore follows its own assumptions, documented in [generative-learner.md](generative-learner.md).

## Out of scope for the current repository state

The following are not implemented:

- simulator
- generative learner
- BKT, PFA, HLR
- Oracle policy
- Current ConceptBook Weighting
- experiment runner
- metric calculation
- plotting
- language or package-manager setup
- CI
- database
- UI

## Design items left open

The documents name candidates. They do not freeze the following:

- mastery criterion and stopping rule used by Trials to Mastery and related utility metrics
- numeric thresholds inside Current ConceptBook Weighting that are only named qualitatively in the source notes (accuracy bands, high-accuracy cutoff)
- the map from a BKT, PFA, or HLR estimate to a question score
- the response model, which has a leading candidate but is not a frozen specification
- the equation for World C
- how explicit time and inter-trial gaps are generated in worlds that use time
- item pool, concept structure, and the horizon of a simulated session
- implementation language and package manager
