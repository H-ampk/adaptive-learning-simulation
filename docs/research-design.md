# 研究設計

## 目的

このリポジトリは、Knowledge Tracing の予測性能の差が、問題順位付け、問題選択、シミュレーション上の学習効用へどのように伝播するかを調べます。

```text
予測（Prediction）
    ↓
問題順位付け（Ranking）
    ↓
問題選択（Selection）
    ↓
学習効用（Learning Utility）
```

実験仕様を固定したまま ConceptBook 本体の変更を続けられるよう、この研究は ConceptBook アプリケーションから分けています。

## 範囲

比較の対象は、学習者モデル（Learner Model）と、その予測または状態推定を使う出題方策（Policy）です。候補モデルには BKT、PFA、HLR があります。現行ConceptBook重み付け（Current ConceptBook Weighting）はモデルを使わないベースライン（Baseline）であり、ConceptBook から import するのではなく、固定した仕様から再現します。

練習と回答をシミュレートする生成学習者モデル（Generative Learner）は、別の構成要素です。評価対象のどのモデルとも同一視しません。詳細は [generative-learner.md](generative-learner.md) を参照してください。

予測または状態推定を、問題順位付けと問題選択へ変える出題方策も、学習者モデルとは別です。その対応はまだ仕様になっていません。詳細は [policies.md](policies.md) を参照してください。

指標は、伝播の経路に対応する4層に分けます。独自の伝播率は定義しません。詳細は [metrics.md](metrics.md) を参照してください。

## シミュレーション結果が意味すること

1回の実行は、宣言された生成世界の中の量を推定します。複数の世界で一致することは、そのパターンがそれらの仮定に対して頑健であることの証拠です。一つの世界での結果は、人間の学習の測定ではありません。また、ある Knowledge Tracing モデルを ConceptBook 上の別のモデルと置き換えるべきだ、という主張でもありません。

## 研究上の問い

### RQ1 — 予測（Prediction）

BKT、PFA、HLR などのモデルのあいだで、予測の正確さと潜在状態の推定の正確さはどの程度違うか。

候補指標：

- Brier Score
- Log Loss
- AUC
- キャリブレーション誤差（Calibration Error）
- 状態の RMSE（State RMSE）
- 状態の MAE（State MAE）

### RQ2 — 問題順位付け（Ranking）

予測性能の差は、候補問題の順位をどの程度変えるか。

候補：

- スピアマン順位相関（Spearman correlation）
- ケンドールの順位相関（Kendall's tau）
- 上位k件の重なり（Top-k overlap）
- 順位の変位（Rank displacement）

### RQ3 — 問題選択（Selection）

順位の差は、実際に選ばれる問題の差へどの程度なるか。

候補：

- 第1位の一致率（Top-1 agreement）
- 上位k件のジャカード類似度（Top-k Jaccard similarity）
- 選択不一致率（Selection disagreement rate）
- 選択後悔値（Selection Regret）

### RQ4 — 学習効用（Learning Utility）

選択の差は、シミュレーション上の学習効率の差へどの程度なるか。

主候補：

- 習熟到達までの試行数（Trials to Mastery）

副次候補：

- 習熟到達までの時間（Time to Mastery）
- 保持（Retention）
- 最終習熟度（Final Mastery）
- 無駄な練習の割合（Wasted Practice Ratio）
- 練習不足の概念の割合（Neglected Concept Rate）
- 累積選択後悔値（Cumulative Selection Regret）

### RQ5 — 伝播（Propagation）

予測から問題順位付け、問題選択、学習効用までの各段階で、上流の差はどの程度維持され、増幅され、減衰するか。

この問いは、上に挙げた層ごとの指標を比較して答えます。その比較から、解釈できる要約が何であるかが見えるまで、別個の伝播率の式は意図的に定義しません。

### RQ6 — 飽和（Saturation）

予測性能をさらに改善しても、教育的効用（Pedagogical Utility）がほとんど、あるいはまったく改善しない領域があるか。

## 仮説

これらは仮説の候補であり、知見ではありません。

### H1

予測の差は、問題順位付けの差へ完全には伝播しない。

### H2

問題順位付けの差は、問題選択の差へ完全には伝播しない。

### H3

問題選択の差のすべてが、学習効用の差になるわけではない。

### 中心仮説

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

この不等式は検証対象の主張です。研究の結論ではありません。世界、出題方策、指標を定義するときに、この不等式を前提にもしません。

## ConceptBook との関係

```text
ConceptBook
    ↓
現行の重み付け仕様（Current Weighting specification）
    ↓
adaptive-learning-simulation
    ↓
独立した再実装（independent reproduction）
    ↓
他の出題方策との比較（comparison with other policies）
```

ConceptBook が渡すのは、このリポジトリが写し、固定し、再実装する現行の重み付け仕様です。アプリケーションは実行時の依存関係ではありません。再実装ができてから追加する一致テストで、固定した写しが論文用に記録した仕様と一致するかを確認します。

論文で評価した版は、ここに固定したままにします。ConceptBook への後からの編集は、その版を変えません。報告した比較を再現不能にもしません。

記録した重み付け規則は [policies.md](policies.md) にあります。文書のみです。この変更ではベースラインを実装していません。

## 分けたままにする構成要素

```text
生成世界（Generative world）
    シミュレーション上の学習と回答

学習者モデル（Learner model）
    観測履歴からの予測と状態推定

出題方策（Policy）
    その推定、またはモデルを使わない規則からの問題順位付けと問題選択
```

BKT、PFA、HLR のいずれかをデータ生成過程に使うと、世界と評価対象モデルが結びつきます。そのため生成学習者モデルは、独自の仮定に従います。仮定は [generative-learner.md](generative-learner.md) に書いてあります。

## 現在のリポジトリ状態では対象外

次は未実装です。

- シミュレーター
- 生成学習者モデル
- BKT、PFA、HLR
- オラクル方策（Oracle Policy）
- 現行ConceptBook重み付け
- 実験実行系
- 指標の計算
- 図の作成
- 言語またはパッケージ管理の設定
- CI
- データベース
- UI

## 未確定の設計事項

文書が名前を挙げているのは候補です。次は固定していません。

- 習熟到達までの試行数、および関連する効用指標が使う習熟基準と停止規則
- 現行ConceptBook重み付けのうち、元メモでは定性的にしか書かれていない数値の境界（正答率の区分、高正答率のカットオフ）
- BKT、PFA、HLR の推定から問題スコアへの対応
- 回答モデル。有力候補はあるが、固定した仕様ではない
- World C の式
- 時間を使う世界で、明示的な時間と試行間隔をどう生成するか
- 問題集合、概念構造、シミュレーションするセッションの期間
- 実装言語とパッケージ管理
