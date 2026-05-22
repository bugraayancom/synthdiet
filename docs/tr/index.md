# synthdiet dokümantasyonu (Türkçe)

`synthdiet`, gerçekçi klinik tablolara sahip sentetik hastalar üreten ve
bu hastalar üzerinde diyet müdahalelerini simüle eden bir Python
kütüphanesidir.

> Diğer diller: [English](../index.md) · [Español](../es/index.md) · [Français](../fr/index.md) · [Deutsch](../de/index.md) · [Português](../pt/index.md) · [Italiano](../it/index.md) · [中文](../zh/index.md) · [日本語](../ja/index.md)

## Yazar

**Buğra Ayan** — Ankara / Türkiye

- Web sitesi: <https://bugraayan.com>
- E-posta: <bugraayan.com@gmail.com>
- Google Scholar:
  <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

## İçindekiler

### Öğreticiler

1. [Hızlı Başlangıç](tutorials/01_quickstart.md) — sentetik hasta
   oluşturma, diyet uygulama ve simülasyon temelleri.
2. [Randomize Kontrollü Çalışma (RKT) Tasarımı](tutorials/02_rct.md) —
   `synthdiet.trials` ile sanal RKT yürütme.
3. [Nedensel Çıkarım](tutorials/03_causal.md) — karşı-olgusal
   analizler, ATE, CATE ve yanıltıcı (confounding) deneyleri.
4. [Klinik Vaka Çalışmaları ve OSCE](tutorials/04_case_studies.md) —
   `synthdiet.education` modülü ile öğretim senaryoları.
5. [Yayınlanmış RKT'lere Karşı Doğrulama](tutorials/05_validation.md) —
   `synthdiet.validation` ile referans çalışmalara karşı kalibrasyon.
6. [R'dan synthdiet kullanımı](tutorials/06_from_r.md) —
   `reticulate` aracılığıyla R entegrasyonu.

### Referans

- [API Referansı](api.md)

## Atıf

`synthdiet`'i akademik bir çalışmada kullanırsanız, lütfen depo kök
dizinindeki `CITATION.cff` dosyası üzerinden ya da aşağıdaki BibTeX
kaydı ile atıfta bulunun:

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Lisans

MIT — depo kök dizinindeki `LICENSE` dosyasına bakınız.
