# Adaptive Learning Simulation

A simulation framework for evaluating how differences in learner-model prediction quality propagate through question ranking, selection, and simulated learning utility.

```text
Prediction
    ↓
Ranking
    ↓
Selection
    ↓
Learning Utility
```

This repository is a research project, separate from the ConceptBook application. It exists so simulation studies can be reproduced without depending on later changes to ConceptBook itself.

## Question

The study asks how a difference in prediction quality moves through ranking, selection, and simulated learning utility. The working hypothesis is:

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

That statement is a claim to be tested. It is not a result of this repository.

## Planned comparisons

- Learner models such as BKT, PFA, and HLR are candidates for comparison.
- Current ConceptBook Weighting is a baseline to be reproduced from a specification frozen in this repository.
- The generative learner that produces simulated answers and learning is kept independent of the knowledge-tracing models under evaluation.
- Several generative worlds are used so conclusions are not tied to a single learning assumption.

Simulation results describe those generative worlds. They are not, by themselves, evidence about learning effects in human learners.

Reproducibility is a requirement: documented assumptions, frozen policy specifications, and saved configurations should be enough to rerun a study.

## Relationship to ConceptBook

ConceptBook is one object of comparison, through its current weighting specification:

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

This repository does not import ConceptBook as a library. The specification used in a paper will be copied here and checked with conformance tests, so a later change in ConceptBook cannot make that study unreproducible.

## Layout

| Path | Role |
| --- | --- |
| `docs/` | Research design, generative learner, policies, metrics, related work |
| `configs/` | Experiment configurations (empty) |
| `src/` | Simulation code (not implemented) |
| `tests/` | Tests (not implemented) |
| `results/` | Experiment outputs; `results/raw/` and `results/tmp/` are ignored |

## Status

Research documents only. The simulator, generative learner, learner models, policies, metrics, experiment runner, and plots are not implemented.
