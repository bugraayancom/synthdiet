# synthdiet ドキュメント(日本語)

`synthdiet` は、現実的な臨床像を持つ合成患者を生成し、それらに
食事介入をシミュレーションするための Python ライブラリです。

> 他言語: [English](../index.md) · [Türkçe](../tr/index.md) · [Español](../es/index.md) · [Français](../fr/index.md) · [Deutsch](../de/index.md) · [Português](../pt/index.md) · [Italiano](../it/index.md) · [中文](../zh/index.md)
## 著者

**Buğra Ayan** —— トルコ・アンカラ

- ウェブサイト: <https://bugraayan.com>
- メール: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

## 目次

### チュートリアル

1. [クイックスタート](tutorials/01_quickstart.md) —— 患者の生成、
   食事の適用、シミュレーションの基本。
2. [RCT の設計と実行](tutorials/02_rct.md) —— `synthdiet.trials` での
   ランダム化試験。
3. [因果推論](tutorials/03_causal.md) —— 反事実解析、ATE、CATE、
   交絡実験。
4. [臨床ケースと OSCE](tutorials/04_case_studies.md) ——
   `synthdiet.education` を使った教材。
5. [既発表 RCT に対するバリデーション](tutorials/05_validation.md) ——
   `synthdiet.validation` でのキャリブレーション。
6. [R から synthdiet を使う](tutorials/06_from_r.md) —— `reticulate`
   を介した連携。

### リファレンス

- [API リファレンス](api.md)

## 引用

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## ライセンス

MIT —— リポジトリルートの `LICENSE` を参照。
