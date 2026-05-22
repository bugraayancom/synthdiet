# API リファレンス

このページは `synthdiet` の公開 API を日本語の短い説明とともに
列挙します。Sphinx で生成される完全なドキュメントは英語ですが、
本ページは概観の早見表として使えます。

## 患者モデル

| シンボル | 説明 |
|---------|------|
| `synthdiet.Patient` | 人口統計、人体計測、バイオマーカー、生活習慣、診断、薬剤を集約するメインオブジェクト。 |
| `synthdiet.Demographics` | 年齢、性別、国 など。 |
| `synthdiet.Anthropometrics` | 身長、体重、ウエスト周囲長。 |
| `synthdiet.Biomarkers` | 検査値(HbA1c、LDL、血圧 …)。 |
| `synthdiet.Lifestyle` | 身体活動、喫煙、飲酒。 |

## 疾患

| シンボル | 説明 |
|---------|------|
| `synthdiet.Disease` | すべての疾患の基底クラス。 |
| `synthdiet.NutritionalConstraints` | 疾患特異的な栄養制約。 |
| `synthdiet.available_diseases()` | 登録済み疾患の一覧。 |
| `synthdiet.get_disease(name)` | 名前から疾患クラスを返す。 |

## 食事プラン

| シンボル | 説明 |
|---------|------|
| `synthdiet.DietPlan` | 食事プランの構造化表現。 |
| `synthdiet.mediterranean_diet()` | 地中海食。 |
| `synthdiet.dash_diet()` | DASH。 |
| `synthdiet.keto_diet()` | ケトジェニック。 |
| `synthdiet.low_fodmap_diet()` | 低 FODMAP。 |
| `synthdiet.low_sodium_renal_diet()` | 低ナトリウム腎臓食。 |
| `synthdiet.diabetic_diet()` | 糖尿病食。 |
| `synthdiet.vegan_diet()` | ビーガン食。 |
| `synthdiet.standard_diet()` | 標準食(対照)。 |

## ジェネレータ

| シンボル | 説明 |
|---------|------|
| `synthdiet.RandomPatientGenerator` | ランダム生成。 |
| `synthdiet.DistributionPatientGenerator` | 分布から生成。 |
| `synthdiet.CopulaPatientGenerator` | コピュラ(相関のある特徴)。 |
| `synthdiet.CohortGenerator` | 仕様からコホートを生成。 |
| `synthdiet.CohortSpec` | コホート設定。 |
| `synthdiet.DiseaseSpec` | コホート内の疾患分布。 |
| `synthdiet.MarkovProgressionGenerator` | マルコフ進行。 |

## シミュレーション

| シンボル | 説明 |
|---------|------|
| `synthdiet.DietSimulator` | メインシミュレータ(simple + Hall 2011)。 |
| `synthdiet.SimulationResult` | バイオマーカー軌跡を含む結果。 |
| `synthdiet.HallSimulation` | Hall 2011 モデルの実装。 |
| `synthdiet.HallSimulationParameters` | 調整可能パラメータ。 |

## 臨床試験

| シンボル | 説明 |
|---------|------|
| `synthdiet.trials.ParallelTrial` | 並行群 RCT。 |
| `synthdiet.trials.CrossoverTrial` | クロスオーバー。 |
| `synthdiet.trials.FactorialTrial` | 2×2 要因。 |
| `synthdiet.trials.intention_to_treat` | ITT 解析。 |
| `synthdiet.trials.per_protocol` | Per-protocol 解析。 |

## 食事品質指標

| シンボル | 説明 |
|---------|------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020。 |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010。 |
| `synthdiet.indices.MEDAS` | 地中海食アドヒアランス。 |
| `synthdiet.indices.DASHScore` | DASH アドヒアランス。 |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index。 |
| `synthdiet.indices.DII` | Dietary Inflammatory Index。 |

## 因果推論

| シンボル | 説明 |
|---------|------|
| `synthdiet.causal.counterfactual_run` | 同一患者の 2 食事下での反事実シミュレーション。 |
| `synthdiet.causal.ATEEstimator` | ATE 推定器。 |
| `synthdiet.causal.cate_by_subgroup` | サブグループ別 CATE。 |
| `synthdiet.causal.ConfoundingExperiment` | 交絡 + IPTW + g-公式。 |
| `synthdiet.causal.DietDAG` | 軽量 DAG ユーティリティ。 |

## 教育

| シンボル | 説明 |
|---------|------|
| `synthdiet.education.CaseStudy` | 単一の臨床ケース。 |
| `synthdiet.education.OSCEStation` | OSCE 形式の評価ステーション。 |
| `synthdiet.education.built_in_cases()` | 内蔵 15 ケース。 |

## 統計とノイズ

| シンボル | 説明 |
|---------|------|
| `synthdiet.stats.sample_size_continuous` | 連続アウトカムのサンプルサイズ。 |
| `synthdiet.stats.sample_size_binary` | 二値アウトカムのサンプルサイズ。 |
| `synthdiet.stats.bootstrap_ci` | ブートストラップ CI。 |
| `synthdiet.stats.permutation_test` | 並べ替え検定。 |
| `synthdiet.stats.fdr_bh` | Benjamini-Hochberg FDR。 |
| `synthdiet.stats.ancova_baseline_adjusted` | ベースライン調整 ANCOVA。 |
| `synthdiet.noise.add_lab_measurement_error` | 検査値への測定誤差。 |
| `synthdiet.noise.inject_mcar_missing` | MCAR 欠測。 |
| `synthdiet.noise.inject_mar_missing` | MAR 欠測。 |
| `synthdiet.noise.inject_mnar_missing` | MNAR 欠測。 |
