# synthdiet

[![PyPI sürümü](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python sürümleri](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Diğer diller: [English](README.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md)

Gerçekçi klinik tablolara sahip **sentetik hastalar** üreten ve bu hastalar
üzerinde **diyet müdahalelerini simüle eden** bir Python kütüphanesi.

`synthdiet`; diyetisyenler, klinik beslenme araştırmacıları ve eğitimciler
için tasarlanmıştır. Diyet protokollerini prototiplemek, sanal klinik
çalışmalar yürütmek ve beslenme önerilerini kliniğe taşımadan önce
yüzlerce/binlerce sentetik hasta üzerinde stres testine tabi tutmak için
kullanılabilir.

> Yasal uyarı: `synthdiet` bir araştırma ve eğitim aracıdır. Ürettiği
> sayılar **klinik öneri değildir** ve sentetik hastalar **gerçek hasta
> değildir**. Hasta bakımı için her zaman yetkili bir kayıtlı diyetisyene
> başvurun.

---

## Yazar

**Buğra Ayan** — Ankara / Türkiye
- Web sitesi: <https://bugraayan.com>
- E-posta: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Özellikler

### Temel alan modeli
- Demografik bilgileri, antropometriyi, yaşam tarzını, laboratuvar
  biyobelirteçlerini, tanıları ve mevcut ilaçları bir araya getiren
  tipli bir `Patient` (Hasta) sınıfı.
- Endokrin, kardiyovasküler, renal, hepatik, gastrointestinal,
  metabolik, kas-iskelet, onkolojik, psikiyatrik ve alerji
  kategorilerini kapsayan **25+ hastalık** kayıt defteri.
- **19 klinik açıdan önemli ilaç-besin etkileşimi** (metformin → B12,
  statinler → greyfurt, varfarin → K vitamini, levotiroksin alım
  zamanlaması, MAOI tiramin krizi vb.) kayıt defteri.
- 5 sentetik hasta üreteci (rastgele, dağılım tabanlı, kopula, kohort,
  Markov ilerlemesi).
- Makro/mikro besin dökümlü 45 öğelik bir besin veritabanı ve
  8 hazır diyet ön ayarı (Akdeniz, DASH, ketojenik, düşük FODMAP,
  düşük sodyumlu renal, diyabetik, vegan, standart).

### Yöntemsel derinlik (v0.1 genişlemesi)
- **Hall 2011 vücut kompozisyonu modeli** opsiyonel olarak
  (`DietSimulator(engine="hall_2011")`); Forbes denklemi ile
  yağ kütlesi/yağsız kütle ayrımı ve adaptif termogenez.
- **Uyum (adherence) ve bırakma (dropout) dinamikleri**: sabit,
  azalan, Weibull bırakma, stokastik atlama, algılanan yük modelleri.
- **RKT motoru** (`synthdiet.trials`): paralel kollu, çapraz (crossover)
  ve 2×2 faktöriyel tasarımları, tabakalı/blok/minimizasyon
  randomizasyonunu, bırakma modellemesini ve ITT/PP/AT analizlerini
  destekler.
- **Nedensel çıkarım** (`synthdiet.causal`): karşı-olgusal simülasyon,
  ATE/CATE tahmincileri, IPTW ve g-formülü düzeltmesi içeren
  yanıltıcı (confounding) deneyleri, hafif DAG araçları.
- **Diyet kalitesi indeksleri** (`synthdiet.indices`): HEI-2020,
  AHEI-2010, MEDAS, DASH skoru, PHDI, DII.
- **İstatistiksel yardımcılar** (`synthdiet.stats`): sürekli ve
  ikili sonuçlar için güç analizi, bootstrap güven aralıkları,
  permütasyon testleri, Benjamini-Hochberg + Holm-Bonferroni
  düzeltmeleri, başlangıç düzeyine göre ayarlanmış ANCOVA.
- **Ölçüm hatası ve eksik veri enjeksiyonu** (`synthdiet.noise`):
  test başına CV%, öz-bildirim yanlılığı, MCAR/MAR/MNAR örüntüleri.
- **15 klinik vaka çalışması + OSCE tarzı puanlama**
  (`synthdiet.education`).
- **5 dönüm noktası RKT'sine karşı doğrulama paketi**
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Görselleştirme** (`synthdiet.viz`, opsiyonel): CONSORT diyagramı,
  forest plot, trajektör şeridi, Tablo 1.

---

## Kurulum

```bash
pip install synthdiet
```

Opsiyonel ekstralar:

```bash
pip install "synthdiet[viz]"     # matplotlib görselleştirmeleri
pip install "synthdiet[causal]"  # networkx DAG dışa aktarımı
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` Python 3.9+ gerektirir; `numpy`, `pandas` ve `scipy`
bağımlılıklarını kullanır.

---

## 60 saniyelik tur

```python
from synthdiet import (
    CohortGenerator, CohortSpec, DiseaseSpec,
    DietSimulator, mediterranean_diet,
    evaluate_simulation, format_evaluation_report,
)

spec = CohortSpec(
    size=100,
    diseases=[
        DiseaseSpec("type_2_diabetes", prevalence=0.40),
        DiseaseSpec("hypertension",     prevalence=0.45),
    ],
)
cohort = CohortGenerator(spec, seed=42).generate()

simulator = DietSimulator(adherence=0.8)
diet = mediterranean_diet(daily_energy_kcal=1800)

for patient in cohort[:3]:
    result = simulator.run(patient, diet, duration_weeks=12)
    evaluation = evaluate_simulation(result)
    print(format_evaluation_report(evaluation))
    print("-" * 60)
```

Daha fazla uçtan uca örnek için [`examples/`](examples/) klasörüne
bakabilirsiniz.

---

## Proje düzeni

```
src/synthdiet/
├── patients/          # Demografi, antropometri, biyobelirteçler, yaşam tarzı
├── diseases/          # 25+ hastalık sınıfı + kayıt defteri
├── interactions/      # İlaç kataloğu + ilaç-besin etkileşimi kaydı
├── nutrition/         # Besinler, besin öğeleri, DRI'lar
├── diets/             # DietPlan + 8 hazır diyet
├── generators/        # 5 sentetik hasta üreteci
├── simulation/        # Diyet simülatörü (basit + Hall 2011 vücut kompozisyonu)
├── behavior/          # Uyum + Weibull bırakma modelleri
├── trials/            # RKT motoru (paralel/çapraz/faktöriyel + ITT/PP)
├── causal/            # Karşı-olgusal + ATE/CATE + IPTW + DAG
├── indices/           # HEI-2020, AHEI-2010, MEDAS, DASH, PHDI, DII
├── stats/             # Güç analizi, bootstrap, ANCOVA, FDR/Holm
├── noise/             # Lab CV% + MCAR/MAR/MNAR eksik veri enjeksiyonu
├── validation/        # DASH-Sodium / PREDIMED / DiRECT / Look AHEAD / DPP
├── education/         # 15 vaka çalışması + OSCE rubriği + Markdown/HTML
├── viz/               # CONSORT, trajektörler, forest, Tablo 1 (matplotlib)
├── evaluation/        # Sonuç metrikleri + raporlar
└── utils/             # Sabitler, doğrulayıcılar, rastgele durum yardımcıları
```

Türkçe öğreticiler [`docs/tr/tutorials/`](docs/tr/tutorials/) dizininde,
İngilizce öğreticiler ise [`docs/tutorials/`](docs/tutorials/) dizininde
yer alır. JOSS makale taslağı için [`paper/`](paper/) klasörüne bakın.

---

## `synthdiet`'i genişletme

Yeni bir hastalık eklemek için `Disease` sınıfını alt sınıflayın ve
kayıt defterine kaydedin:

```python
from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register


@register
class FattyLiverGradeII(Disease):
    name = "fatty_liver_grade_ii"
    icd10 = "K76.0"
    category = "hepatic"

    def nutritional_constraints(self, patient):
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.45),
            added_sugar_pct_max=0.05,
            fiber_g_min=30,
        )
```

İçe aktarıldıktan sonra, sınıf otomatik olarak
`get_disease("fatty_liver_grade_ii")` ile erişilebilir hale gelir ve
`DiseaseSpec` içinde seçilebilir.

---

## Atıf

`synthdiet`'i akademik bir çalışmada kullanırsanız, lütfen
[`CITATION.cff`](CITATION.cff) dosyası üzerinden ya da aşağıdaki
BibTeX kaydı ile atıfta bulunun:

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

---

## Lisans

MIT — bkz. [`LICENSE`](LICENSE).
