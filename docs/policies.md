# Policies

A policy chooses the next question. A learner model supplies a prediction or a state estimate. The policy is the map from that estimate, or from a rule that does not use a model, to a ranking and then a selection.

```text
Learner Model
    ↓
Prediction / State Estimate
    ↓
Policy
    ↓
Ranking
    ↓
Selection
```

BKT, PFA, and HLR are learner models. They are not policies. The map from each model's estimate to "which question is chosen" is not yet defined. Until that map is written down, a named model-based policy is a placeholder for a family, not an algorithm.

Non-model baselines enter at the policy step. They do not produce a latent-state estimate.

## Baselines

- **Random** — select from the eligible pool without using history or a model.
- **Sequential** — select in a fixed item order.
- **Current ConceptBook Weighting** — select by the frozen weighting specification below.

The sampling rule for Current ConceptBook Weighting, as recorded, is weighted sampling without replacement. It is not "always take the unique maximum." Comparisons that need a deterministic top-1 must state how ties and weighted draws are resolved.

## Model-based policies

- **BKT-based Policy** — ranking and selection from a BKT prediction or state estimate. The score that ranks items is unspecified.
- **PFA-based Policy** — ranking and selection from a PFA prediction or state estimate. The score that ranks items is unspecified.
- **HLR-based Policy** — ranking and selection from an HLR prediction or state estimate. The score that ranks items is unspecified.

Each of these needs an explicit scoring function before an experiment can attribute a selection difference to the learner model rather than to an unstated ranking rule.

## Upper bound

- **Oracle Policy** — selection that may use privileged information from the generative world, such as the true latent state. The information set and the objective the oracle optimizes are not yet defined.

The oracle is an upper reference for utility under a stated objective. It is not a learner model and it is not a fair competitor on prediction metrics, because those metrics assume the model sees only the observation history.

## Current ConceptBook Weighting

This is the baseline specification to copy into this repository and keep unchanged for a paper. It is documentation of the current ConceptBook rule. It is not an implementation, and this repository does not import ConceptBook.

Recorded adjustments:

| Condition | Adjustment |
| --- | --- |
| Unanswered | `+10` |
| Incorrect-answer count | `incorrect × 3` |
| Accuracy | `+6` / `+3` |
| Elapsed time of 7 days | `+5` |
| Elapsed time of 30 days | `+8` |
| Elapsed time within 1 day | `-4` |
| Correct on the immediately previous attempt | a further `-2` |
| High accuracy | `-3` |
| Minimum weight | `1` |

Selection uses weighted sampling without replacement.

The purpose of copying this table is to freeze the version that a paper evaluates. Later changes in ConceptBook must not move the baseline out from under a reported result. When the rule is reimplemented, conformance tests should compare this repository's copy with the specification that was current at the time of the freeze.

Two boundaries are named but not numeric in this record: which accuracy values receive `+6` versus `+3`, and which accuracy value counts as high accuracy for the `-3` adjustment. Those cutoffs are part of the freeze. They are to be copied from ConceptBook when the reproduction is specified, and then left unchanged for the paper. They are not invented here.

How overlapping time adjustments combine (7 days and 30 days, or a within-1-day penalty together with a later bonus) is also part of that freeze and is not resolved in this note.
