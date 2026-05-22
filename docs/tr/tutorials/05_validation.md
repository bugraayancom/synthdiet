# Yayınlanmış RKT'lere Karşı `synthdiet`'i Doğrulama

`synthdiet.validation` modülü, simülatörün tamamını yayınlanmış
klinik çalışma sonuçlarına karşı çalıştırır. Beklenen etkiler hakemli
makalelerden alınmış, atıfları ile birlikte belgelenmiştir.

## Pakete dahil hedefler

| Hedef | Atıf | Sonuç | Beklenen |
|-------|------|-------|----------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSKB (mmHg) | -11.5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6.0 |
| DiRECT | Lean Lancet 2018;391:541-51 | ΔKilo (kg) | -10.0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | ΔKilo (kg) | -7.9 |
| DPP | Knowler NEJM 2002;346:393-403 | ΔKilo (kg) | -5.5 |

> SKB = Sistolik Kan Basıncı.

Bu çalışmalar; düşük sodyumlu DASH diyetinden (kan basıncı için),
geleneksel Akdeniz diyetinden (LDL için), çok düşük kalorili sıvı
diyetlerden (DiRECT, DPP, Look AHEAD - kilo kaybı için) klinik
beslenmenin temel taşlarıdır.

## Tüm doğrulamaları çalıştırma

```python
from synthdiet.validation import (
    validate_dash_sodium, validate_predimed, validate_direct,
    validate_look_ahead, validate_dpp,
)

for validator in (
    validate_dash_sodium, validate_predimed, validate_direct,
    validate_look_ahead, validate_dpp,
):
    report = validator(n_patients=120, seed=42)
    print(report.pretty())
```

Her rapor şunları içerir:

- **Beklenen etki** (yayından)
- **Simüle edilen etki** (synthdiet'ten)
- **Tolerans aralığı**
- **PASS / FAIL** kararı

## CI'da kullanım

Doğrulama paketi, hızlı test çalıştırmalarını yavaşlatmamak için
pytest'te `slow` olarak işaretlenmiştir. Çalıştırmak için:

```bash
pytest -m slow tests/test_validation.py -v
```

## Hataların yorumlanması

Bir doğrulama **FAIL** ise, simülatör belgelenen toleransın dışında
bir değer üretmiştir. Tipik nedenler:

- Hastalığın tepki modelinde (`response_to_diet`) bir gerileme.
- Varsayılan diyet makro oranlarında biyobelirteç projeksiyonlarını
  aralık dışına taşıyan bir değişiklik.
- Yetersiz veya aşırı düzelten bir uyum/bırakma değişikliği.

Böyle bir durumda incelemeniz gereken yerler:

1. İlgili hastalığın `response_to_diet` kancası (örneğin `Hypertension`
   sınıfı).
2. Hall modelinin kalibrasyon sabitleri (`HallSimulationParameters`).
3. Diyet ön ayarının makro/mikro besin profili.

Yayınlanmış etkinin yanlış olduğuna karar vermeden önce bu üçünü
gözden geçirin.

## Kendi referans çalışmanızı ekleme

Yeni bir doğrulayıcı yazmak istiyorsanız tipik şablon şudur:

```python
from synthdiet.validation.base import ValidationTarget, run_validation

def validate_my_trial(n_patients: int = 120, seed: int = 0):
    target = ValidationTarget(
        name="MyTrial",
        citation="Author Journal 2024;1:1-10",
        outcome="ldl_mg_dl",
        expected_effect=-12.0,
        tolerance=4.0,
    )
    return run_validation(
        target,
        cohort_spec=...,        # ilgili hastalık prevalansları
        treatment_diet=...,     # çalışmadaki müdahale
        control_diet=...,       # çalışmadaki kontrol
        duration_weeks=12,
        n_patients=n_patients,
        seed=seed,
    )
```

Yeni doğrulayıcıyı paketin `validate_*` fonksiyonlarının yanına
yerleştirin ve `tests/test_validation.py` içine bir test ekleyin.
