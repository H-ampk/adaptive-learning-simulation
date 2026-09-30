# Related Work

This note groups research lines that the study design draws on. It is a map for later reading, not a finished review. Bibliographic details should be checked and completed before any paper cites them. No BibTeX file or reference manager is part of this repository yet.

Entries are labeled as representative works to confirm. The short gloss says why the line matters here. It does not summarize a paper's results as established fact.

## Simulated students in knowledge-tracing evaluation

Knowledge-tracing models are often scored on log data, and sometimes also on data from a simulated student whose learning rule is known.

Representative works to confirm:

- Corbett and Anderson's knowledge tracing work, which introduced the BKT family inside a mastery-learning tutor.
- Piech and colleagues' Deep Knowledge Tracing, which reported both real and simulated settings in the evaluation of a neural tracer.
- Khajah, Lindsey, and Mozer's comparison of deep knowledge tracing with extended BKT, including simulated data, under a title of the form "How deep is knowledge tracing?"

Use in this repository: simulated students make the latent state available, so prediction metrics and state-error metrics can be reported together. The generating rule must stay independent of the models being scored.

## Knowledge tracing in a mastery-learning context

A large part of the BKT literature evaluates models by how they behave inside mastery practice, not only by next-step accuracy.

Representative works to confirm:

- The cognitive-tutor / knowledge-tracing line associated with Corbett and Anderson, where a mastery criterion stops practice.
- Lee and Brunskill's educational-data-mining paper on individualizing student models and the number of practice opportunities a student would receive.

Use in this repository: Trials to Mastery is the primary utility candidate because mastery learning is the decision context, not only next-item classification.

## Adaptive practice scheduling

Scheduling policies choose what to practice next, often with an explicit memory or half-life model.

Representative works to confirm:

- Settles and Meeder's trainable spaced-repetition model (half-life regression) for language learning.
- Lindsey, Shroyer, Pashler, and Mozer on personalized review and long-term retention.
- Pavlik and Anderson on computing a practice schedule from an activation-based memory model.

Use in this repository: HLR-based and spacing-aware policies belong to this line. The policy that turns a half-life or activation into a ranking still has to be specified; the model paper does not fix that map for this study.

## Prediction accuracy and pedagogical decision quality

Next-step metrics (AUC, log loss, Brier score) and the quality of an instructional decision are related but are not the same measurement.

Representative concern, with citations still to be pinned down:

- Work in the educational-data-mining and intelligent-tutoring literature that tracks how a change in the student model changes downstream practice, including the individualization study named above.
- Broader arguments that a model can improve predictive fit without changing the decision a tutor would make, or the reverse.

Use in this repository: RQ2 through RQ6 exist because a gain on RQ1 is not assumed to appear as a gain in selection or utility. The central hypothesis is the thing to be measured across those layers.

This note does not treat any single paper as having settled that hypothesis.

## Exponential forgetting

One standard family writes retention as an exponential decay in the time since practice.

Representative anchors to confirm:

- Exponential decay as used in memory models and in BKT variants that add a forgetting transition.
- Discussions that contrast this form with power-law forgetting, including the papers listed in the next section.

Use in this repository: World B-E adopts exponential forgetting as a declared assumption, through the candidate update `K(t + Δ) = K(t) exp(-λ Δ)`. It is one analysis world, not a claim that human forgetting is exponential.

## Power-law forgetting

Another standard family writes retention as a power function of time or of a lag term.

Representative works to confirm:

- Wixted and Ebbesen, "On the form of forgetting," arguing at the time for a power function over an exponential on aggregate forgetting curves.
- Anderson and Schooler, "Reflections of the environment in memory," connecting a power law of forgetting to environmental statistics and to the ACT-R activation tradition.
- Later methodological work asking whether an apparent power law can arise from averaging heterogeneous exponential curves. Exact citations are still to be added.

Use in this repository: World B-P adopts power-law forgetting as a second declared assumption, through the candidate update `K(t + Δ) = K(t) (1 + λ Δ)^(-β)`. B-E and B-P are both primary candidates so a result can be checked for dependence on the forgetting family.

## ACT-R and Pavlik–Anderson spacing models

Activation-based models explain spacing by the history of practice traces, not by a single lag applied to a scalar competence.

Representative works to confirm:

- Pavlik and Anderson's activation-based model of practice and forgetting in vocabulary, and the spacing effect.
- Pavlik and Anderson's later use of that model to compute a practice schedule.
- The ACT-R base-level learning and activation equations those models draw on (Anderson and Lebiere, and related ACT-R statements). Exact edition and equation numbers are to be fixed when World C is specified.

Use in this repository: World C is a stress test in this family. Its equation is deliberately unset until the state, the trace decay, and the link to the response probability are written down.

## Synthetic learners in adaptive-learning evaluation

When a live student experiment is too costly for every policy variant, studies evaluate schedulers against a synthetic learner and treat the outcome as conditional on that learner.

Representative practice to confirm with specific citations:

- Policy comparisons inside simulated tutors, where the simulator is published along with the policy.
- Evaluations that report both predictive fit and a teaching outcome (practice count, delayed recall, or a mastery proxy).

Use in this repository: the synthetic learner is useful because the latent state and the counterfactual selection are observable. The corresponding limit is part of the study design: utility is a property of the named world, and a simulation result is not reported as a human learning effect.

## What this file is not

- It is not a claim that the central hypothesis has already been shown.
- It is not a complete or citable bibliography.
- It does not fix World C, the response model, or any policy scoring rule. Those remain in the design documents as open specifications.
