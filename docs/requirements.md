# Adaptive Learning Simulation 要件定義書

## 1. 文書の目的

本書は、`adaptive-learning-simulation` の研究用シミュレーション基盤について、目的、対象範囲、機能要件、非機能要件、研究上の制約、再現性要件を定義する。

本システムは、ConceptBook本体とは独立した研究基盤として開発する。

研究上の中心課題は、

```text
予測
↓
問題順位付け
↓
問題選択
↓
学習効用
```

という伝播過程を評価し、

> 学習者モデルの予測性能差が、下流の教育的意思決定およびシミュレーション上の学習効用へどの程度伝播するか

を検証することである。

---

## 2. 研究目的

本システムは、BKT、PFA、HLR等の学習者モデルについて、単なる回答予測性能だけでなく、その予測を利用した問題順位付け・問題選択・学習効用まで含めて評価するために使用する。

特に以下を検証対象とする。

- 予測性能の差が問題順位へどの程度伝播するか
- 問題順位の差が実際の問題選択へどの程度伝播するか
- 問題選択の差が学習効用へどの程度伝播するか
- 予測性能を改善しても学習効用が改善しなくなる領域が存在するか
- 複雑な学習者モデルを用いた出題方策が、単純な履歴ベースヒューリスティックを上回るか
- 上記の結果が、生成学習者モデルの仮定を変更しても維持されるか

中心仮説は、

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

である。

これは研究上の結論ではなく、検証対象となる仮説である。

---

## 3. システムの位置付け

本システムは以下を目的としない。

- ConceptBook本体の実装
- 実際の学習者向けUI
- LMS
- 学習支援アプリ
- 人間の学習効果を直接予測する完成モデル

本システムは、

> 仮定した生成学習者環境の下で、学習者モデルおよび出題方策の挙動を比較するための研究用シミュレーション基盤

である。

---

## 4. 技術要件

### 4.1 言語

実装言語はJuliaとする。

現在の基準環境：

```text
Julia 1.11.7
```

### 4.2 パッケージ構成

Julia package名：

```text
AdaptiveLearningSimulation
```

依存関係は必要最小限とする。

現在利用するもの：

- StableRNGs.jl
- Distributions.jl
- DataFrames.jl
- CSV.jl

追加依存は必要性を確認してから導入する。

---

## 5. システム構成

最終的には以下の論理構造を持つ。

```text
生成学習者
    ↓
回答生成
    ↓
観測履歴
    ↓
学習者モデル
    ↓
予測・状態推定
    ↓
出題方策
    ↓
問題順位付け
    ↓
問題選択
    ↓
生成学習者の状態更新
    ↓
次の試行
```

評価処理は、この各段階の情報を記録する。

---

## 6. 生成学習者要件

### 6.1 基本原則

生成学習者モデルは、評価対象であるBKT / PFA / HLRとは独立して定義する。

BKT、PFA、HLRのいずれかを「真の学習者モデル」として使用してはならない。

目的は、特定の評価対象モデルに構造的に有利なシミュレーション環境を作らないことである。

### 6.2 潜在状態

生成学習者は、学習者ごと・概念ごとに潜在状態を持つ。

候補表現：

```text
a[u, c, t] ∈ R
```

および、

```text
K[u, c, t] = sigmoid(a[u, c, t])
```

潜在状態の正本を `a` とするか `K` とするかは実装前に確定する。

### 6.3 学習者差

最低限、以下の個人差を表現可能とする。

- 初期習熟度
- 学習速度
- 忘却速度
- Guess
- Slip / Lapse
- 概念間の初期知識差

固定的な「学習者タイプ」を定義するのではなく、連続パラメータ空間として扱う。

---

## 7. 問題要件

問題は最低限以下を持つ。

- 問題ID
- 対応する概念ID
- 問題難易度

問題難易度は、

```text
d[q]
```

として表現できる構造を持つ。

初回研究では以下は必須としない。

- 複数概念問題
- 前提概念
- 問題形式差
- 認識 / 再生差
- 問題文
- UI情報

---

## 8. 回答生成要件

回答生成では、潜在能力と問題難易度に加えてGuess / Slipを扱えること。

現在の有力候補：

```text
P(correct)
=
G + (1 - G - S) * sigmoid(a - d)
```

ここで、

- `G`: Guess
- `S`: Slip / Lapse
- `a`: 潜在能力
- `d`: 問題難易度

とする。

この式は現時点では有力候補であり、研究上の確定仕様ではない。

回答は指定されたRNGを利用して確率的に生成する。

---

## 9. 生成世界要件

複数の生成世界を同一インターフェースで交換可能とする。

### World A

Learning-only。

- 学習あり
- 忘却なし
- spacing効果なし

最小構成のベースラインとして使用する。

### World B-E

Exponential Forgetting。

- diminishing learning
- explicit time
- exponential forgetting

候補：

```text
K(t + Δ) = K(t) exp(-λΔ)
```

主分析条件の一つとする。

### World B-P

Power-law Forgetting。

- diminishing learning
- explicit time
- power-law forgetting

候補：

```text
K(t + Δ)
=
K(t)(1 + λΔ)^(-β)
```

主分析条件の一つとする。

### World C

認知モデル・spacingを強く反映したstress test。

候補：

- practice history
- activation
- memory trace
- spacing effect

Pavlik-Anderson / ACT-R系研究を参考とする。

具体式は別途設計する。

---

## 10. 学習更新要件

practice後の潜在状態更新をWorldごとに定義可能とする。

有力候補：

```text
K+ = K + L(1 - K)
```

これにより、高習熟状態ほど追加practiceによる伸びを小さくする。

初回の主分析では、learning gainを回答の正誤へ直接依存させない。

以下は感度分析候補とする。

- 正解時のretrieval bonus
- 不正解後のfeedback学習
- 正誤別learning gain

---

## 11. 学習者モデル要件

以下の学習者モデルを比較可能にする。

- BKT
- PFA
- HLR

学習者モデルは生成学習者の真の内部状態へアクセスしてはならない。

入力として利用可能なのは、実際の学習システムでも観測可能と想定される情報のみとする。

例：

- 回答履歴
- 正誤
- 問題
- 概念
- 時刻

モデルの推定値と出題方策は分離する。

---

## 12. 出題方策要件

以下の出題方策を比較可能にする。

### ベースライン

- Random
- Sequential
- 現行ConceptBook重み付け

### モデルベース

- BKT-based Policy
- PFA-based Policy
- HLR-based Policy

### 上限参照

- Oracle Policy

学習者モデルと出題方策は別の構成要素として実装する。

```text
学習者モデル
↓
予測・状態推定
↓
出題方策
↓
問題スコア
↓
問題順位
↓
問題選択
```

---

## 13. 現行ConceptBook重み付け

研究用ベースラインとして、評価対象時点のConceptBook仕様を固定して再実装する。

現在記録されている要素：

- 未回答 `+10`
- 誤答回数 `incorrect × 3`
- 正答率による `+6 / +3`
- 7日経過 `+5`
- 30日経過 `+8`
- 1日以内 `-4`
- 直前正答 `-2`
- 高正答率 `-3`
- minimum weight `1`
- weighted sampling without replacement

ConceptBook本体から直接importしない。

研究時点の仕様を独立して固定し、再現可能にする。

---

## 14. 評価指標要件

評価指標は4層に分離する。

### 14.1 予測

- Brier Score
- Log Loss
- AUC
- Calibration
- State RMSE
- State MAE

### 14.2 問題順位付け

- Spearman correlation
- Kendall's tau
- Top-k overlap
- Rank displacement

### 14.3 問題選択

- Top-1 agreement
- Top-k Jaccard similarity
- Selection disagreement rate
- Selection Regret

### 14.4 学習効用

Primary候補：

- 習熟到達までの試行数（Trials to Mastery）

Secondary候補：

- Time to Mastery
- Retention
- Final Mastery
- Wasted Practice Ratio
- Neglected Concept Rate
- Cumulative Selection Regret

---

## 15. ログ要件

各interactionについて、研究上必要な中間状態を保存可能とする。

最低限の候補：

- experiment ID
- learner ID
- trial
- time
- true latent state
- question ID
- concept ID
- item difficulty
- response probability
- actual response
- model prediction
- model state estimate
- candidate questions
- question scores
- ranking
- selected question
- Oracle selection
- immediate utility
- cumulative utility
- updated latent state

ただし、大規模実験での保存容量を考慮し、詳細ログと集計ログを分離可能とする。

---

## 16. 実験設定要件

実験条件はソースコードへ直接埋め込まず、設定として管理可能とする。

最低限：

- seed
- World
- learner count
- concept count
- question count
- maximum trials
- learner parameter distributions
- question difficulty distribution
- policy
- learner model
- mastery threshold
- time configuration

実験設定から同じ実験を再実行可能であること。

---

## 17. 再現性要件

研究の再現性は最重要の非機能要件とする。

以下を満たすこと。

- 乱数seedを明示する
- default RNGへ依存しない
- RNGオブジェクトを明示的に渡す
- StableRNGsを利用可能とする
- `Project.toml` を管理する
- `Manifest.toml` を管理する
- 実験設定を保存する
- 使用したcommit SHAを記録可能にする
- 同一seed・同一設定・同一コードで同一結果を再生成可能とする

---

## 18. 公平性・研究妥当性要件

以下を設計上の必須制約とする。

### 18.1 モデルリーク防止

評価対象モデルは生成学習者の真の潜在状態を参照してはならない。

Oracleのみ例外とする。

### 18.2 Generative Model Favoritismの抑制

特定のモデルと同一の生成過程のみで評価しない。

複数の生成世界を使用する。

### 18.3 PolicyとModelの分離

予測モデルそのものの能力と、予測値をどう出題へ利用するかを分離する。

### 18.4 Sensitivity Analysis

主要結論について、

- forgetting equation
- parameter range
- mastery threshold
- learner heterogeneity
- noise
- policy mapping

等への依存性を確認可能とする。

---

## 19. 性能要件

初期段階では正確性・再現性を性能より優先する。

ただし最終的には、

- 数千〜数万の仮想学習者
- 複数World
- 複数Policy
- 複数parameter condition
- Monte Carlo simulation

を現実的に実行できる構造を目指す。

並列化は初期必須要件とはしない。

正しいsingle-thread実装を先に確立する。

---

## 20. テスト要件

最低限、以下を自動テスト可能とする。

### 基盤

- package load
- 型の生成
- RNG再現性

### 回答生成

- 確率が `[0,1]` 内
- difficulty増加で正答確率が低下
- ability増加で正答確率が上昇
- Guess / Slipの影響

### World

- World Aで忘却が発生しない
- World B-Eで時間経過により状態が低下
- World B-Pで時間経過により状態が低下
- 同一条件で期待される単調性を満たす

### Simulation

- 同一seedで同一結果
- 異なるPolicyで状態を共有しない
- Oracle以外が真の状態へアクセスしない

数値誤差を考慮し、浮動小数点値について不適切な完全一致を要求しない。

---

## 21. 出力要件

研究結果は機械処理可能な形式で保存する。

候補：

- CSV
- Julia serialization
- 将来的にはArrow等

初期段階ではCSVを基本候補とする。

生データと集計結果を区別する。

```text
results/
├─ raw/
├─ processed/
└─ summary/
```

具体形式は実験runner設計時に確定する。

---

## 22. 文書要件

人が読む文書は原則日本語で作成する。

以下は必要に応じて英語表記を維持する。

- コード識別子
- モデル名
- 指標名
- ライブラリ名
- 数式記号
- 論文名

研究上の重要語は必要に応じて、

```text
日本語（English）
```

で併記する。

---

## 23. 初回研究で扱わないもの

初回研究のスコープから以下を除外する。

- 人間を対象とした実験
- UI / UX評価
- motivation
- fatigue
- misconception
- concept間transfer
- prerequisite graph
- recognition / recall差
- feedback形式差
- 複数KCを同時に含む問題
- IRTの本格導入
- Deep Knowledge Tracingの実装
- neural network
- reinforcement learningによるPolicy最適化

これらは将来研究候補とする。

---

## 24. 開発単位

実装はGitHub Issue単位で行う。

原則として、

```text
要件
↓
設計
↓
実装
↓
テスト
↓
研究文書更新
```

の順序を守る。

一つのIssueで複数の研究上重要な仮定を同時に確定しない。

---

## 25. 初期Issue候補

実装順は以下を基本とする。

1. 生成学習者モデルの共通型・基盤
2. 回答生成モデル
3. World A
4. World B-E
5. World B-P
6. 仮想時間モデル
7. Simulation runnerの最小版
8. Random / Sequential Policy
9. 現行ConceptBook Weighting
10. BKT
11. PFA
12. HLR
13. Model-based Policy
14. Oracle
15. Prediction metrics
16. Ranking metrics
17. Selection metrics
18. Utility metrics
19. Monte Carlo runner
20. 感度分析
21. Controlled Prediction Quality Experiment

順序は依存関係に応じて変更可能とする。

---

## 26. 現時点の未確定事項

以下は本要件定義時点では未確定とする。

- 潜在状態の正本を `a` / `K` のどちらにするか
- 初期知識分布の具体値
- learning rate分布
- forgetting parameter分布
- Guess / Slip分布
- item difficulty分布
- 仮想時間 `Δ` の生成方法
- World Cの具体式
- mastery threshold
- Trials to Masteryの厳密な終了条件
- learner model → policyの写像
- Oracle Utility
- Selection Regretの厳密な定義
- Controlled Prediction Quality Experimentを初回論文に含めるか

これらは結果を確認してから後付けで調整するのではなく、各実験の実施前に研究文書で確定する。

---

## 27. 完了条件

本研究基盤の初期完成は、少なくとも以下を満たした状態とする。

- 複数の生成世界を切替可能
- 仮想学習者をseed付きで生成可能
- 問題回答系列を生成可能
- BKT / PFA / HLRを同じ観測データへ適用可能
- 複数出題方策を交換可能
- Prediction / Ranking / Selection / Utilityを記録可能
- 同一条件の再実行が可能
- Monte Carlo simulationが可能
- 実験設定と結果を保存可能
- 全主要ロジックに自動テストが存在
- 研究文書から実装上の仮定を追跡可能
