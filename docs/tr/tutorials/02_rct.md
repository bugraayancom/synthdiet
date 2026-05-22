# Randomize Kontrollü Çalışma (RKT) Tasarımı ve Yürütülmesi

Bu öğretici, `synthdiet.trials` motorunu kullanarak paralel kollu bir
randomize kontrollü çalışmayı (RKT) simüle eder.

> Terminoloji: Bu dokümanda **RKT** (Randomize Kontrollü Çalışma)
> İngilizce karşılığı **RCT** (Randomised Controlled Trial) ile aynı
> anlamda kullanılır.

## Kohort üretimi

```python
from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec

spec = CohortSpec(
    size=200,
    diseases=[
        DiseaseSpec("hypertension", prevalence=0.40,
                    severity_weights={"mild": 4, "moderate": 4, "severe": 2}),
        DiseaseSpec("type_2_diabetes", prevalence=0.30),
    ],
)
cohort = CohortGenerator(spec, seed=2026).generate()
```

Burada 200 hastalık bir kohort üretilir; %40'ı hipertansif (şiddet
dağılımı 4:4:2), %30'u tip 2 diyabetlidir. Tekrar üretilebilirlik için
`seed=2026` sabitlenmiştir.

## Güç (power) analizi

Çalışmaya başlamadan önce, hedef etkiyi belirleyebilmek için kaç
hastaya ihtiyacınız olduğunu hesaplayın:

```python
from synthdiet.stats import sample_size_continuous

n = sample_size_continuous(effect_size=2.0, sd=8.0, alpha=0.05, power=0.80)
print(f"Kol başına {n} hasta gerekli (2 kg fark, %80 güç).")
```

## Çalışmayı tanımlama ve çalıştırma

```python
from synthdiet.diets import dash_diet, standard_diet
from synthdiet.trials import ParallelTrial, WeibullDropout
from synthdiet.behavior import DecayingAdherence

trial = ParallelTrial(
    cohort=cohort,
    arms={"control": standard_diet(), "dash": dash_diet()},
    duration_weeks=24,
    primary_outcome="systolic_bp_mmhg",
    secondary_outcomes=["weight_kg", "ldl_mg_dl"],
    randomization="stratified",
    strata=[lambda p: p.demographics.sex.value,
            lambda p: p.has_disease("type_2_diabetes")],
    adherence=DecayingAdherence(initial=0.90, floor=0.45, rate=0.02),
    dropout=WeibullDropout(shape=1.5, scale_weeks=40, seed=7),
    engine="hall_2011",
)
result = trial.run(seed=42)
```

Önemli parametreler:

- `arms`: Kol adı → diyet planı eşlemesi.
- `randomization`: `"simple"`, `"stratified"`, `"block"` veya
  `"minimization"`.
- `strata`: Tabakalı randomizasyon için hasta üzerinden tanımlanan
  fonksiyonların listesi (cinsiyet, diyabet durumu vb.).
- `adherence`: Uyum modeli. `DecayingAdherence` zamanla azalan uyumu
  modeller.
- `dropout`: Hastaların çalışmadan ayrılma örüntüsü. Weibull
  dağılımı klinik çalışmalarda yaygın olarak kullanılır.

## ITT ve PP analizleri

```python
itt = result.intention_to_treat(method="ancova")
pp = result.per_protocol(adherence_threshold=0.80)
print(itt.pretty())
print(pp.pretty())
```

- **ITT (Intention-to-Treat)**: Hastayı atandığı kola göre analiz
  eder; bırakanlar dahil. Klinik etkinliğin (effectiveness)
  ölçüsüdür.
- **PP (Per-Protocol)**: Yalnızca uyum eşiğini geçen hastaları
  analiz eder. Biyolojik etkinin (efficacy) ölçüsüdür.

## CONSORT diyagramı

```python
from synthdiet.viz import consort_diagram

ax = consort_diagram(result, title="Sentetik DASH çalışması")
ax.figure.savefig("consort.png", dpi=150, bbox_inches="tight")
```

CONSORT diyagramı, randomize edilen, atanan, uyumlu olan ve
analiz edilen hasta sayılarını klinik araştırma raporlarındaki
standart akış şemasına uygun şekilde görselleştirir.

## Başlangıç düzeyine göre ayarlanmış ANCOVA

Diyet çalışmalarında başlangıçtaki kan basıncı veya kilo değeri,
sonuçtaki değişimi büyük ölçüde belirler. ANCOVA, başlangıç
değerini kovaryant olarak kullanarak istatistiksel gücü artırır:

```python
from synthdiet.stats import ancova_baseline_adjusted

ancova = ancova_baseline_adjusted(
    result.outcomes,
    outcome="delta_systolic_bp_mmhg",
    baseline="baseline_systolic_bp_mmhg",
    treatment="arm",
)
print(ancova.pretty())
```

## Çapraz (crossover) ve faktöriyel tasarımlar

`ParallelTrial`'a alternatif olarak `CrossoverTrial` (her hasta
sırayla iki diyet de alır) ve `FactorialTrial` (örn. diyet × egzersiz
2×2 tasarım) sınıfları da mevcuttur.

```python
from synthdiet.trials import CrossoverTrial, FactorialTrial
```

Her iki sınıf da aynı `arms`, `duration_weeks`, `primary_outcome`
arayüzünü paylaşır; ayrıntılar için API referansına bakınız.
