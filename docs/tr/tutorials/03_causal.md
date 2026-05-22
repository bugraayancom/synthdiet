# Sentetik Hastalarla Nedensel Çıkarım

`synthdiet` tamamen sentetik hastalar ürettiği için, her hastanın
her diyet altındaki **gerçek karşı-olgusal sonucu** hesaplanabilir.
Bu durum, kütüphaneyi nedensel çıkarımı öğretmek için benzersiz
biçimde uygun kılar.

> Gerçek dünyada bir hastanın "Akdeniz diyeti uygularsa ne olur?"
> ve "Standart diyet uygularsa ne olur?" sorularının ikisini birden
> gözlemleyemezsiniz. Sentetik hastada bu mümkündür ve gerçek ATE
> (Ortalama Tedavi Etkisi) bilinebilir; bu da farklı tahmincileri
> kıyaslamak için altın bir referans sağlar.

## Karşı-olgusal karşılaştırmalar

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
    mediterranean_diet, standard_diet,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.causal import counterfactual_run

patient = Patient(
    demographics=Demographics(age=58, sex=Sex.MALE),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98),
    lifestyle=Lifestyle(),
)
patient.add_disease(Type2Diabetes(severity="moderate"))

pair = counterfactual_run(patient, mediterranean_diet(), standard_diet(),
                          duration_weeks=12)
ite = pair.individual_effect("hba1c_pct")
print(f"HbA1c üzerindeki bireysel tedavi etkisi: {ite:+.2f} pp")
```

`pair` nesnesi hem tedavi hem kontrol kolu altındaki simülasyon
sonuçlarını içerir. `individual_effect` fonksiyonu, herhangi bir
biyobelirteç için bireysel tedavi etkisini (ITE) döner.

## Kohort üzerinde ATE

Ortalama Tedavi Etkisi (ATE), bir popülasyondaki ortalama nedensel
etkiyi temsil eder:

```python
from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec
from synthdiet.causal import ATEEstimator

cohort = CohortGenerator(
    CohortSpec(size=80, diseases=[DiseaseSpec("type_2_diabetes", 1.0)]),
    seed=1,
).generate()

est = ATEEstimator(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    duration_weeks=12,
)
result = est.estimate(cohort, outcome="hba1c_pct")
print(result.pretty())
```

## Heterojen etkiler (CATE)

Tüm hastalar aynı ölçüde fayda görmez. Koşullu Ortalama Tedavi
Etkisi (CATE), alt gruplara göre etkinin nasıl değiştiğini
gösterir:

```python
from synthdiet.causal import cate_by_subgroup

cate = cate_by_subgroup(
    cohort=cohort,
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    subgroup_fn=lambda p: "obez" if p.bmi >= 30 else "obez_degil",
    outcome="hba1c_pct",
)
for group, ate in cate.items():
    print(group, ate.pretty())
```

Tipik sonuçlar: obez tip 2 diyabet hastalarında etki, obez olmayanlara
göre genellikle daha büyüktür.

## Yanıltıcılar (confounding) ve düzeltme

Gözlemsel verilerde tedavi ataması rastgele olmayabilir; örneğin
daha hasta olanlar daha yoğun müdahale alır. `ConfoundingExperiment`,
bu durumu simüle ederek farklı tahmincilerin yanıltıcı etkiyi nasıl
düzelttiğini karşılaştırır:

```python
from synthdiet.causal import ConfoundingExperiment

exp = ConfoundingExperiment(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    # Daha hasta olanlar daha yoğun müdahale alıyor (yanıltıcı atama)
    propensity=lambda p: min(0.9, max(0.1, (p.bmi - 22) / 25.0)),
    duration_weeks=12,
)
report = exp.run(cohort, outcome="hba1c_pct", seed=42)
print(report)
```

Çıktı şunları içerir:

- **Gerçek ATE**: sentetik hastalar olduğu için bilinebilir.
- **Naif karşılaştırma**: yanıltıcılar nedeniyle sapmalı.
- **IPTW** (Inverse Probability of Treatment Weighting): eğilim
  skoru ağırlıklarıyla düzeltilmiş tahmin.
- **g-formülü**: koşullu ortalamaların standardize edilmesiyle
  düzeltilmiş tahmin.

## Bir DAG'ı görselleştirme

```python
from synthdiet.causal.dag import default_diet_dag

dag = default_diet_dag()
print(dag.to_mermaid())
```

Mermaid çıktısını bir Markdown görüntüleyiciye veya GitHub
README'sine yapıştırarak DAG'ı grafik olarak görebilirsiniz.

## Pratik öneri

Sentetik veriler üzerinde çeşitli nedensel tahmincileri sınamak,
gerçek veride seçeceğiniz yöntemin ne kadar güvenilir olduğunu
anlamanıza yardımcı olur. `synthdiet` ile tipik bir alıştırma:

1. Bilinen yanıltıcı yapı altında sentetik veri üret.
2. Naif, IPTW ve g-formülü tahminlerini hesapla.
3. Hangisinin gerçek ATE'ye en yakın olduğunu raporla.
4. Aynı yöntemi gerçek (gözlemsel) veri kümenize uygulamadan önce
   sentetik veride hata büyüklüğünü belgele.
