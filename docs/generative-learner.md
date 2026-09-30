# Generative Learner

The generative learner is the simulated world. It produces practice, knowledge change, and observed answers. Models under evaluation (BKT, PFA, HLR, and others) are fitted to or scored against that world. They do not define it.

## Design principles

- None of BKT, PFA, or HLR is used as the true data-generating model.
- The model under evaluation and the generative world stay independent.
- Robustness is assessed across multiple worlds, so a result is not an artifact of one learning assumption.

A world states its learning rule, forgetting rule, and whether time is explicit. Changing those assumptions is a change of world, not a hidden parameter of the model being scored.

## Worlds

### World A — Learning-only

Minimal baseline.

- learning is present
- forgetting is absent
- spacing effects are absent

World A checks whether a propagation pattern already appears when the only knowledge change is learning from practice.

### World B-E — Exponential Forgetting

Primary analysis candidate.

- diminishing learning
- exponential forgetting
- explicit time

Candidate forgetting update:

```text
K(t + Δ) = K(t) exp(-λ Δ)
```

This equation is a candidate form for the forgetting step. It is not a complete world specification. The learning step, the distribution of `Δ`, and the parameters remain to be fixed.

### World B-P — Power-law Forgetting

Primary analysis candidate.

- diminishing learning
- power-law forgetting
- explicit time

Candidate forgetting update:

```text
K(t + Δ) = K(t) (1 + λ Δ)^(-β)
```

World B-E and World B-P are alternatives, not a ranking of which forgetting curve is true of human memory. Running both asks whether a propagation result depends on the forgetting family.

### World C — Cognitive / Spacing Stress Test

Stress test, not a primary analysis world until its equation is chosen.

- dependence on practice history
- activation- or trace-based state
- a more explicit spacing effect
- informed by the Pavlik–Anderson and ACT-R line of spacing models

No equation is fixed for World C. Adopting a formula requires a separate design note that states the state variables, the activation or trace update, and how that state enters the answer model.

## Response model

Leading candidate, not a frozen specification.

Latent ability:

```text
a_u,c,t ∈ R
```

Competence, as a displayed probability scale:

```text
K = sigmoid(a)
```

Item difficulty:

```text
d_q
```

Probability of a correct response:

```text
P(correct) = G + (1 - G - S) * sigmoid(a - d)
```

where

- `G` is guess
- `S` is slip / lapse
- `d` is item difficulty

`K` and `a` are two views of the same latent competence in this candidate. Worlds that update `K` directly need a stated map back to `a` before this response equation can be used. Parameter values, priors, and whether `G` and `S` vary by item or learner are unset.

## Learning gain

Knowledge updates use a diminishing return. An unbounded additive gain is not the candidate.

Example:

```text
K+ = K + L (1 - K)
```

`L` is a learning-rate term in `(0, 1]` for this example. Its dependence on history, time, or the current item is world-specific and not yet fixed.

In the primary worlds, the learning gain is not taken directly from whether the response was correct or incorrect. The default causal story is:

```text
practice opportunity → learning
```

A practice opportunity updates knowledge. The observed correctness is an output of the response model, not the input that sets the gain.

The following are sensitivity analyses, kept separate from the primary worlds:

- successful retrieval bonus
- incorrect response plus feedback
- other correctness-dependent learning rules

A sensitivity world must say which of these modifiers it adds and must not be pooled with the primary estimate without a label.
