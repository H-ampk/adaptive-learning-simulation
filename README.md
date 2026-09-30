# Adaptive Learning Simulation

学習者モデルの予測性能の差が、問題順位付け、問題選択、最終的な学習効用へどのように伝播するかを検証するためのシミュレーション研究用リポジトリです。

研究の中心：

```text
予測（Prediction）
    ↓
問題順位付け（Ranking）
    ↓
問題選択（Selection）
    ↓
学習効用（Learning Utility）
```

このリポジトリは、ConceptBook 本体とは独立した研究用リポジトリです。ConceptBook 側がその後どう変わっても、シミュレーション研究を再現できるように分けています。

## 研究上の問い

この研究が問うのは、予測性能（Prediction Quality）の差が、問題順位付け、問題選択、シミュレーション上の学習効用へどのように移るかです。作業仮説は次のとおりです。

```text
Δ Prediction ≠ Δ Pedagogical Utility
```

これは、予測性能の差と教育的効用（Pedagogical Utility）の差が同じではない、という検証対象の主張です。このリポジトリの結論ではありません。

## 比較の予定

- 比較候補の学習者モデル（Learner Model）には、BKT、PFA、HLR がある。
- 現行ConceptBook重み付け（Current ConceptBook Weighting）は、このリポジトリ内で固定した仕様から再現するベースライン（Baseline）である。
- 模擬の回答と学習を生み出す生成学習者モデル（Generative Learner）は、評価対象の Knowledge Tracing モデルから独立させる。
- 結論を単一の学習仮定に縛らないため、複数の生成世界を用いる。

シミュレーション結果は、それらの生成世界についての記述です。それだけでは、人間の学習者における学習効果の証拠にはなりません。

再現性は要件です。文書化した仮定、固定した出題方策（Policy）の仕様、保存した設定があれば、研究を再実行できる状態にします。

このリポジトリでは、研究の再現性を重視し、Julia の `Project.toml` / `Manifest.toml` と明示的な乱数 seed を使用する。

## 技術構成

- Julia
- StableRNGs.jl
- Distributions.jl
- DataFrames.jl
- CSV.jl

## ConceptBook との関係

ConceptBook は、現行の重み付け仕様を通じた比較対象の一つです。

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

このリポジトリは ConceptBook をライブラリとして import しません。論文で使う仕様はここに写し、一致テストで照合します。これにより、ConceptBook 側の後からの変更で、その研究が再現できなくなることを防ぎます。

## ディレクトリ構成

| パス | 役割 |
| --- | --- |
| `docs/` | 要件定義（`docs/requirements.md`）、研究設計、生成学習者モデル、出題方策、指標、関連研究 |
| `configs/` | 実験設定（空） |
| `src/` | Julia パッケージ `AdaptiveLearningSimulation`（研究ロジックは未実装） |
| `test/` | Julia の package test |
| `results/` | 実験出力。`results/raw/` と `results/tmp/` は Git の対象外 |

## 現状

Julia の package 環境は初期化済みです。シミュレーター、生成学習者モデル、学習者モデル、出題方策、指標、実験実行系、図の作成は未実装です。
