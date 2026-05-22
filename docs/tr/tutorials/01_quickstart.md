# Hızlı Başlangıç

Bu öğretici tipik bir `synthdiet` iş akışını adım adım gösterir:

1. sentetik bir hasta üretmek,
2. bir hastalık eklemek,
3. bir diyet uygulamak,
4. 12 hafta simüle etmek,
5. sonucu değerlendirmek.

## Kurulum

```bash
pip install synthdiet
```

## Tek bir hasta oluşturma

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="TR"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

`patient.summary()`; demografik bilgileri, BKİ'yi, tanıları ve mevcut
biyobelirteçleri özetleyen okunabilir bir metin döner.

## Hazır bir diyet seçme

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

`synthdiet`, 8 hazır diyet ön ayarı sağlar: Akdeniz, DASH, ketojenik,
düşük FODMAP, düşük sodyumlu renal, diyabetik, vegan ve standart.

## Simülatörü çalıştırma

Varsayılan simülatör basit bir "7700 kcal/kg" enerji dengesi kuralını
kullanır. Daha gerçekçi uzun vadeli projeksiyonlar için
`engine="hall_2011"` parametresini geçerek Hall vücut kompozisyonu
modelini etkinleştirebilirsiniz.

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"24 haftalık kilo değişimi: {result.weight_change_kg:+.2f} kg")
```

`adherence=0.85` parametresi, hastanın diyete %85 uyum gösterdiğini
ifade eder. Daha karmaşık uyum modelleri için
`synthdiet.behavior.DecayingAdherence` veya `WeibullDropout` gibi
sınıflar kullanılabilir.

## Sonucu değerlendirme

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

Değerlendirme raporu:

- başlangıçtan sona biyobelirteç değişimlerini,
- hedef aralığa göre durumu (iyileşti, kötüleşti, sabit),
- diyet kısıtı uyarılarını (varsa),
- ve genel klinik anlamlılık özetini içerir.

## Diyet kısıtlarını önceden kontrol etme

Hastanın hastalıkları diyet üzerinde sıkı kısıtlar getirebilir
(örneğin renal hastada düşük sodyum, fenilketonüride düşük protein).
Simülasyonu çalıştırmadan önce kısıtları kontrol edebilirsiniz:

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Uyarı:", w)
```

## Sonraki adımlar

- [02_rct](02_rct.md) — bir kohort üzerinde çok kollu randomize bir
  klinik çalışma yürütme.
- [03_causal](03_causal.md) — karşı-olgusal analizler ve
  ATE tahmini.
- [04_case_studies](04_case_studies.md) — yerleşik klinik
  vakaları öğretimde kullanma.
