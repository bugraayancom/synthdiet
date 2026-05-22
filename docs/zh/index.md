# synthdiet 文档(中文)

`synthdiet` 是一个用于生成具有真实临床特征的合成患者并对其
模拟饮食干预的 Python 库。

> 其他语言: [English](../index.md) · [Türkçe](../tr/index.md) · [Español](../es/index.md) · [Français](../fr/index.md) · [Deutsch](../de/index.md) · [Português](../pt/index.md) · [Italiano](../it/index.md) · [日本語](../ja/index.md)
## 作者

**Buğra Ayan** —— 土耳其安卡拉

- 网站: <https://bugraayan.com>
- 邮箱: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

## 目录

### 教程

1. [快速上手](tutorials/01_quickstart.md) —— 生成患者、应用饮食并
   进行模拟。
2. [设计并执行 RCT](tutorials/02_rct.md) —— 使用 `synthdiet.trials`
   进行随机对照试验。
3. [因果推断](tutorials/03_causal.md) —— 反事实分析、ATE、CATE
   与混杂。
4. [临床案例与 OSCE](tutorials/04_case_studies.md) —— 使用
   `synthdiet.education` 的教学场景。
5. [对照已发表 RCT 的校验](tutorials/05_validation.md) —— 通过
   `synthdiet.validation` 进行校准。
6. [从 R 调用 synthdiet](tutorials/06_from_r.md) —— 通过
   `reticulate` 集成。

### 参考

- [API 参考](api.md)

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

## 许可证

MIT —— 详见仓库根目录的 `LICENSE`。
