# Metrics

Metrics follow the four stages of the study. Each stage has its own quantities. A custom propagation rate is not defined. Propagation (RQ5) is examined by comparing differences across these stages, once the stage metrics themselves are specified precisely enough to support that comparison.

Definitions below name the quantity each metric is meant to capture. Estimators, tie handling, and the reference policy for regret are not frozen.

## Prediction Metrics

Scored from held-out responses, or from the true latent state when the generative world exposes it.

- **Brier Score** — mean squared error of predicted correctness probabilities.
- **Log Loss** — negative log likelihood of observed correctness under the predicted probabilities.
- **AUC** — ranking discrimination between correct and incorrect responses.
- **Calibration** — agreement between predicted probabilities and observed frequencies. The error summary (binning, ECE, or another calibration error) is not chosen yet.
- **RMSE / MAE** — error of a latent-state estimate against the generative state's competence, when that state is observable to the evaluator. These are state metrics, not response metrics.

State RMSE and State MAE are only defined for worlds and models that share a stated correspondence between the model state and the generative competence. That correspondence is not assumed to exist for every model.

## Ranking Metrics

Compared between two rankings of the same candidate set at the same decision point.

- **Spearman** — rank correlation of the two full orderings.
- **Kendall** — pairwise order agreement (Kendall's tau).
- **Top-k overlap** — size of the intersection of the two top-k sets, scaled in a way still to be fixed.
- **Rank displacement** — movement of items between the two rankings. The aggregation (mean absolute rank change, or another summary) is not chosen yet.

## Selection Metrics

Compared between the questions two policies actually select.

- **Top-1 agreement** — rate at which the two policies select the same question.
- **Jaccard** — Jaccard similarity of the selected sets when a policy selects more than one item, and of top-k sets when the comparison is defined on shortlists.
- **Disagreement rate** — rate at which selections differ.
- **Regret** — utility gap between the selected question and a reference selection. The reference (oracle, or another named policy) and the utility inside the gap are not chosen yet.

Weighted sampling, as in Current ConceptBook Weighting, makes selection stochastic. Agreement and regret for that policy need a declared treatment of random draws (shared random seed, expected selection, or a fixed number of replicates).

## Utility Metrics

Scored on completed simulated trajectories.

- **Trials to Mastery** — number of practice trials until the mastery criterion is met. Primary candidate for RQ4. The mastery criterion is not defined yet.
- **Time to Mastery** — simulated time until the same criterion, in worlds where time is explicit.
- **Retention** — competence at a later time, after a stated delay. The delay and the retention summary are not defined yet.
- **Final Mastery** — competence at the end of a fixed horizon, or at mastery, as declared by the experiment.
- **Wasted Practice** — practice delivered on material that the declared waste criterion counts as unproductive. The criterion is not defined yet.
- **Neglected Concept** — rate or count of concepts that receive too little practice under a declared neglect criterion. The criterion is not defined yet.
- **Cumulative Regret** — selection regret accumulated along a trajectory. It depends on the selection-regret reference above.

Utility metrics are properties of a policy inside a generative world. A higher utility in simulation is not a measurement of human learning.
