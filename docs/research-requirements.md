# Adaptive Learning Simulation 研究要件定義書

## 1. 文書の目的

本書は、`adaptive-learning-simulation` を用いて実施する研究について、研究目的、研究課題、検証対象、実験条件、評価指標、分析要件、妥当性要件、再現性要件、および研究として主張可能な範囲を定義する。

本書はソフトウェアの実装要件ではなく、**研究として何を検証し、どの条件を満たせば結果を解釈できるか**を定めるものである。

---

# 2. 研究テーマ

本研究では、

> **学習者モデルの予測性能の差が、問題順位付け、問題選択、最終的な学習効用へどのように伝播するか**

をシミュレーションにより検証する。

研究対象となる伝播経路は以下とする。

```text
予測
↓
問題順位付け
↓
問題選択
↓
学習効用
```

Knowledge Tracingモデルの評価を、予測精度だけで完結させず、その予測が実際の教育的意思決定へどの程度影響するかまで評価する。

---

# 3. 研究背景

Knowledge Tracingでは、Brier Score、Log Loss、AUC等を用いた回答予測性能の評価が広く行われる。

しかし、教育システムにおいて学習者モデルは最終目的ではなく、

- 次に何を出題するか
- どの概念を復習させるか
- いつ学習済みと判断するか

といった意思決定のために使用される。

したがって、

> 予測性能が高いモデルほど、より良い教育的意思決定を行える

とは限らない。

本研究では、この関係を段階的に分解して検証する。

---

# 4. 研究目的

本研究の主要目的は、以下の4点である。

1. 学習者モデル間の予測性能差を定量化する
2. 予測性能差が問題順位付け・問題選択へどの程度伝播するかを測定する
3. 問題選択差がシミュレーション上の学習効用へどの程度影響するかを測定する
4. 上記の関係が生成学習者モデルの仮定によってどの程度変化するかを検証する

最終的には、

> **予測性能を改善することが、どの条件で教育的意思決定の改善につながるのか**

を明らかにすることを目指す。

---

# 5. 中心仮説

本研究の中心的な検証対象を以下とする。

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

すなわち、

> 学習者モデル間の予測性能差と、教育的効用の差は同一ではない

という仮説である。

これは研究開始時点の結論ではなく、検証対象である。

---

# 6. Research Questions

## RQ1：予測性能

> 学習者モデル間で、回答予測性能および潜在状態推定性能はどの程度異なるか。

比較対象候補：

- BKT
- PFA
- HLR

評価候補：

- Brier Score
- Log Loss
- AUC
- Calibration
- State RMSE
- State MAE

State RMSE / MAEは、真の潜在状態を参照可能なシミュレーション環境でのみ使用する。

---

## RQ2：問題順位付け

> 学習者モデル間の予測性能差は、次に学習すべき問題の順位をどの程度変化させるか。

評価候補：

- Spearman順位相関
- Kendall's tau
- Top-k overlap
- Rank displacement

同一時点・同一候補問題集合に対する順位を比較する。

---

## RQ3：問題選択

> 問題順位の差は、実際に選択される問題の差へどの程度伝播するか。

評価候補：

- Top-1 agreement
- Top-k Jaccard similarity
- Selection disagreement rate
- Selection Regret

単に異なる問題を選んだ回数だけでなく、その違いが教育的にどの程度重要だったかを評価する。

---

## RQ4：学習効用

> 問題選択の差は、シミュレーション上の学習効率・保持性能へどの程度影響するか。

主要評価指標候補：

- 習熟到達までの試行数（Trials to Mastery）

副次評価指標候補：

- Time to Mastery
- Retention
- Final Mastery
- Wasted Practice Ratio
- Neglected Concept Rate
- Cumulative Selection Regret

---

## RQ5：伝播

> 予測 → 問題順位付け → 問題選択 → 学習効用の各段階で、モデル間差はどの程度維持・増幅・減衰するか。

研究では最終成績だけでなく、各段階における差を追跡する。

---

## RQ6：飽和

> 予測性能を一定以上改善しても、問題選択や学習効用がほとんど改善しなくなる領域は存在するか。

必要に応じて、予測誤差を人工的に制御する実験を実施する。

---

# 7. 仮説

## H1

学習者モデル間の予測性能差は、問題順位の差へ完全には伝播しない。

## H2

問題順位の差は、実際の問題選択の差へ完全には伝播しない。

## H3

問題選択の差のすべてが、最終的な学習効用の差につながるわけではない。

## H4候補

予測性能と学習効用の関係には、一定以上の予測性能向上が学習効用向上へほとんど寄与しなくなる飽和領域が存在する。

H4はControlled Prediction Quality Experimentを実施する場合のみ正式仮説とする。

---

# 8. 比較対象

## 8.1 ベースライン出題方策

最低限以下を比較する。

- Random
- Sequential
- 現行ConceptBook重み付け

---

## 8.2 モデルベース出題方策

候補：

- BKT-based Policy
- PFA-based Policy
- HLR-based Policy

ただし、

```text
学習者モデル
↓
状態推定・予測
↓
出題方策
↓
問題順位付け
↓
問題選択
```

を明確に分離する。

学習者モデルそのものと、モデル出力を問題選択へ変換する規則を混同してはならない。

---

## 8.3 Oracle

シミュレーション上の真の潜在状態を参照できるOracle方策を、上限比較の候補として用いる。

Oracleは実際の教育システムで利用可能な方策ではなく、シミュレーション上の参照基準とする。

Oracleが最大化するUtilityは、実験開始前に明示的に定義する。

---

# 9. 現行ConceptBook重み付けの位置付け

現行ConceptBookの出題アルゴリズムは、Knowledge Tracingを直接利用しない履歴ベースヒューリスティックとして扱う。

研究上の問いの一つを、

> 複雑な学習者モデルを利用した出題方策は、単純な履歴ベースヒューリスティックを上回る教育的価値を持つか

とする。

研究対象となるConceptBook重み付けは、評価時点の仕様を固定する。

ConceptBook本体の将来変更によって実験結果が変化しないよう、研究用リポジトリ内で独立した仕様として管理する。

---

# 10. 生成学習者モデルの要件

## 10.1 独立性

生成学習者モデルは、

- BKT
- PFA
- HLR

のいずれかと同一の生成過程にしてはならない。

評価対象モデルと真の生成過程を分離する。

---

## 10.2 複数世界

単一の生成モデルだけで結論を出さず、複数の生成世界を使用する。

### World A

Learning-only。

- 学習あり
- 忘却なし
- spacingなし

最小ベースラインとして使用する。

### World B-E

Exponential Forgetting。

- diminishing learning
- 明示的な時間
- exponential forgetting

主分析条件の一つ。

### World B-P

Power-law Forgetting。

- diminishing learning
- 明示的な時間
- power-law forgetting

主分析条件の一つ。

### World C

より認知モデル寄りのstress test。

候補：

- memory trace
- activation
- practice history
- spacing effect

World Cは初回研究では補助分析として扱うことができる。

---

# 11. 回答生成

回答生成は、学習者の潜在能力と問題難易度を区別できる必要がある。

有力候補：

```text
P(correct)
=
G + (1 - G - S) * sigmoid(a - d)
```

ここで、

- `a`：潜在能力
- `d`：問題難易度
- `G`：Guess
- `S`：Slip / Lapse

とする。

回答生成モデルは実験開始前に確定し、結果を見た後に都合よく変更してはならない。

---

# 12. 個人差

生成学習者は最低限以下の異質性を持てる必要がある。

- 初期習熟度
- 学習速度
- 忘却速度
- Guess
- Slip
- 概念間の知識差

これらは固定的な「学習者タイプ」として扱わず、連続パラメータ空間として扱う。

「Fast Learner」「Forgetful Learner」等の名称を使用する場合は、分析上の代表領域を示すラベルとする。

---

# 13. 問題モデル

問題は最低限、

- 問題ID
- 概念ID
- 問題難易度

を持つ。

初回研究では、1問題につき1概念を基本とする。

以下は初回研究の必須要件としない。

- 複数概念問題
- 前提概念
- Concept Graph
- 認識 / 再生差
- 問題形式差

---

# 14. 時間モデル

World B-E / B-Pでは、時間経過を明示的に扱う。

最低限、

- 問題間の時間
- セッション間隔
- 最終practiceからの経過時間

を表現可能とする。

具体的な時間生成方法は実験開始前に確定する。

実際の時間分布を模倣する場合は、その根拠を明示する。

---

# 15. 学習更新

practiceによる学習増分は、無制限な線形加算を避ける。

有力候補：

```text
K+ = K + L(1 - K)
```

主分析では、practiceを行ったこと自体によって学習が発生する単純な構造を基本候補とする。

正誤による学習量差は、初回から必須とせず感度分析候補とする。

---

# 16. 実験単位

最低限、以下の階層を区別する。

```text
実験条件
↓
Monte Carlo反復
↓
仮想学習者
↓
trial / interaction
```

同一の仮想学習者条件に複数Policyを適用する場合、比較可能性を確保するための乱数設計を事前に定義する。

---

# 17. 主要独立変数

候補：

- 学習者モデル
- 出題方策
- 生成世界
- 初期習熟度
- 学習速度
- 忘却速度
- Guess
- Slip
- 問題難易度分布
- 時間条件
- mastery threshold

全要因を一度にfactorial化する必要はない。

主要研究と感度分析を分離する。

---

# 18. 主要従属変数

## 予測層

- Brier Score
- Log Loss
- AUC
- Calibration Error
- State RMSE / MAE

## 順位層

- Spearman correlation
- Kendall's tau
- Top-k overlap
- Rank displacement

## 選択層

- Agreement
- Disagreement
- Jaccard similarity
- Regret

## Utility層

- Trials to Mastery
- Time to Mastery
- Retention
- Final Mastery
- Wasted Practice Ratio
- Neglected Concept Rate

---

# 19. 主要アウトカム

初回研究のPrimary Outcomeは原則として、

> **習熟到達までの試行数（Trials to Mastery）**

を第一候補とする。

ただし、masteryの定義および終了条件は実験開始前に確定する。

副次指標をPrimaryへ変更する場合は、結果確認前に研究文書を更新する。

---

# 20. Mastery定義

以下を実験前に確定する。

- 潜在状態の閾値
- すべての概念を習熟済みとする必要があるか
- 一定割合でよいか
- 一時的に閾値を超えればよいか
- 一定期間保持している必要があるか

Masteryの定義はTrials to Masteryへ直接影響するため、重要な研究条件として扱う。

---

# 21. 分析要件

最終的なUtility比較だけでは不十分とする。

各段階について、

```text
Prediction Error
↓
Ranking Difference
↓
Selection Difference
↓
Utility Difference
```

を追跡可能にする。

分析では、

- 効果量
- 相関
- rank correlation
- agreement
- regret
- 必要に応じて回帰分析

等を利用する。

独自指標を新規定義する場合は、既存指標では表現できない理由を明示する。

---

# 22. Controlled Prediction Quality Experiment

RQ6を検証する場合、実モデルだけでなく予測品質を人工的に操作する。

概念例：

```text
p_hat = p_true + ε
```

ノイズ量を変化させ、

```text
予測性能
↓
問題順位
↓
問題選択
↓
学習効用
```

の関係を連続的に観察する。

ノイズ分布、clip方法、calibrationへの影響は実験前に確定する。

---

# 23. 感度分析

最低限、主要結論について以下への依存性を検討する。

- exponential / power-law forgetting
- forgetting parameter
- learning rate
- mastery threshold
- Guess / Slip
- 初期知識分布
- 問題難易度
- 時間分布
- learner heterogeneity
- model → policy変換方法

主要分析と感度分析を明確に区別する。

---

# 24. バイアス防止要件

## 24.1 Generative Model Favoritism

評価対象モデルと同一の生成構造だけを使用しない。

## 24.2 Oracle Favoritism

OracleのUtility定義が特定Policyと同義にならないよう注意する。

## 24.3 Post-hoc Tuning

結果を確認した後に、特定モデルが有利になるようパラメータ範囲や評価指標を変更しない。

## 24.4 Metric Shopping

複数指標のうち都合の良いものだけを主要結果として報告しない。

Primary / Secondaryを事前に区別する。

---

# 25. 再現性要件

すべての正式実験について、最低限以下を保存する。

- Git commit SHA
- Julia version
- `Project.toml`
- `Manifest.toml`
- experiment configuration
- random seed
- World
- learner parameters
- model configuration
- policy configuration
- metric configuration

同一コード・同一設定・同一seedから同一結果を再生成できることを要求する。

---

# 26. 乱数要件

default RNGへ暗黙的に依存しない。

seedから生成したRNGを明示的にsimulationへ渡す。

正式実験では、乱数生成方法を記録する。

Policy間比較において共通乱数を使用するか独立乱数を使用するかは事前に決定し、文書化する。

---

# 27. ログ要件

各trialで必要に応じて以下を記録する。

- learner
- world
- trial
- time
- latent state
- question
- item difficulty
- response probability
- response
- model prediction
- model state
- question scores
- ranking
- selected question
- Oracle selection
- immediate utility
- cumulative utility
- post-update state

大規模Monte Carloでは、すべての詳細ログを保存する必要はなく、検証用詳細ログと本番集計ログを分離する。

---

# 28. シミュレーション規模

初期実装確認では小規模条件を利用する。

例：

- learner数：少数
- concept数：10程度
- trial数：100程度

研究結果生成時はMonte Carlo反復を増やす。

正式なサンプルサイズは、分散・計算コスト・推定精度を確認して決定する。

単純に「10,000人なら十分」と固定しない。

---

# 29. 統計的報告要件

シミュレーション結果では、平均値だけでなく分布を報告する。

可能な限り、

- 平均
- 中央値
- 標準偏差
- 分位点
- 信頼区間またはMonte Carlo uncertainty
- 効果量

を報告する。

大量simulationにより極小の差が統計的に明確になっても、実質的な差があるとは限らないため、**effect sizeを重視する**。

---

# 30. 成功・失敗の定義

研究成功を、

> BKT/PFA/HLRのいずれかが他より優れる結果になること

とは定義しない。

以下はいずれも有効な研究結果とする。

- 予測性能差がUtility差まで伝播する
- 途中で差が消失する
- 小さな予測差が大きなUtility差へ増幅される
- 生成世界によってモデル順位が反転する
- 単純なConceptBookヒューリスティックが複雑なモデルと同等になる
- 特定のモデルが常に優位ではない

研究の目的は勝者を決めることではなく、**差がどのような条件で下流へ伝播するかを明らかにすること**である。

---

# 31. 主張可能な範囲

本研究のみから、

- 人間の学習者でも同じ結果になる
- 特定モデルが現実の教育で最善である
- ConceptBookが他システムより教育的に優れている
- 特定の認知理論が正しい

とは主張しない。

主張可能なのは、

> 定義した生成学習者モデル・パラメータ条件・出題方策の下で、予測性能差が問題順位・問題選択・学習効用へどのように伝播したか

までとする。

---

# 32. 外的妥当性

シミュレーション結果の外的妥当性は別途検証する。

将来的には、

```text
人間データ
↓
生成学習者モデルの妥当性確認
↓
シミュレーション再調整
↓
最小限の人間実験
```

という循環を検討する。

ただし初回研究では、人間実験を必須としない。

---

# 33. 初回研究の対象外

初回研究では、原則として以下を除外する。

- UI / UX
- motivation
- fatigue
- emotion
- misconception
- concept間transfer
- prerequisite graph
- recognition / recall差
- feedback形式
- 複数概念問題
- Deep Knowledge Tracing
- reinforcement learning
- neural policy
- 実際のConceptBook利用者データによる効果検証

---

# 34. 研究文書管理

研究上重要な仮定はコードだけに記述せず、必ず文書へ残す。

最低限、

- Research Questions
- 仮説
- 生成世界
- パラメータ
- Primary Outcome
- 終了条件
- 分析方法
- 感度分析条件

を研究文書から確認できる状態にする。

---

# 35. 実験開始前の確定事項

正式な実験を開始する前に、最低限以下を確定する。

1. 潜在状態の正本
2. 状態更新を `a` / `K` のどちらの空間で行うか
3. 初期知識分布
4. learning rate分布
5. forgetting parameter分布
6. Guess / Slip分布
7. item difficulty分布
8. 時間生成方法
9. model → policy写像
10. mastery threshold
11. Trials to Mastery終了条件
12. Oracle Utility
13. Selection Regret
14. Primary / Secondary Outcome
15. Monte Carlo反復数
16. 感度分析条件

これらは結果を確認してから決定してはならない。

---

# 36. 研究完了条件

初回シミュレーション研究は、以下を満たした時点で完了とする。

- 独立した生成学習者モデルが実装されている
- 複数Worldで実験可能
- BKT / PFA / HLRを同一条件で比較可能
- ベースラインPolicyとモデルベースPolicyを比較可能
- 予測・順位・選択・Utilityの各層を記録可能
- Primary Outcomeを評価可能
- 主要Sensitivity Analysisを実施済み
- 再現可能なexperiment configurationが保存されている
- 結果が生成世界に依存するか分析済み
- 研究上の限界を明示できる

---

# 37. 現時点の研究上の未確定事項

現時点では以下を未確定とする。

- `a` / `K` の状態表現
- World B-E / B-Pの具体的パラメータ
- World Cの具体式
- 仮想時間モデル
- 正誤依存learningを感度分析へ入れる範囲
- model-based Policyの具体式
- Oracle Utility
- mastery定義
- Selection Regret
- RQ6を初回論文へ含めるか
- 正式なMonte Carlo規模

これらはそれぞれ独立した設計課題として決定する。