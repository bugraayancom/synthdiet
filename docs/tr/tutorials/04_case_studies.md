# Klinik Vaka Çalışmalarını Eğitimde Kullanma

`synthdiet.education` modülü, doğrudan derste kullanılabilecek
**15 hazır klinik senaryo** ile birlikte gelir. Vakalar, gerçek
beslenme polikliniği başvurularını yansıtacak şekilde hazırlanmıştır:
metabolik sendrom, KOAH'lı yaşlı hasta, gebelik diyabeti, kronik
böbrek hastalığı, çölyak hastalığı, anoreksiya, dispepsi, kanser
kaşeksisi vb.

## Mevcut vakaları listeleme

```python
from synthdiet.education import list_cases
print(list_cases())
```

Çıktı, vaka tanımlayıcılarının (örn. `t2dm_ht_dyslipidemia`) bir
listesidir. Bu kimlikler `get_case` fonksiyonunda anahtar olarak
kullanılır.

## Bir vakayı Markdown olarak görüntüleme

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

Markdown çıktısı şunları içerir:

- Başvuru şikayeti ve hikaye,
- Hasta profili (demografi, BKİ, tanılar, ilaçlar),
- Laboratuvar değerleri,
- Öğrenme hedefleri.

Bu çıktıyı doğrudan ders notlarına veya uzaktan öğretim
platformlarına yapıştırabilirsiniz.

## Referans çözümü inceleme

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("beklenen:", outcome)
```

Referans çözüm; uzman bir diyetisyenin bu hasta için makul kabul
ettiği diyet planını ve 12-24 hafta sonra beklenen biyobelirteç
değişimlerini içerir.

## OSCE tarzı puanlama

Öğrencilerden bir diyet planı tasarlamalarını isteyin, ardından
yerleşik rubrikle puanlayın:

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

Varsayılan rubrik 5 kriter için 4'er puan (toplam 20) verir:

1. **Enerji uygunluğu**: hesaplanan ihtiyaçtan ±%15 sapma içinde.
2. **Yasaklı yiyecek yok**: hastalığa özel yasaklı listelerde
   bir öğe yer almıyor.
3. **Protein yeterliliği**: yaşa, hastalığa ve hedefe göre
   minimum protein karşılanıyor.
4. **Sodyum sınırı**: hastalığa özel sodyum tavanını aşmıyor.
5. **Eklenmiş şeker**: toplam enerjinin ≤ %10'u.

## Rubriği özelleştirme

Lif, doymuş yağ veya lif/kalori oranı gibi ek kriterler ekleyebilirsiniz:

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Lif >= 30 g/gün",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Bir sınıf için toplu çalışma kağıdı oluşturma

Tüm 15 vakayı tek bir HTML dosyasına dökerek öğrencilerinize
verebilirsiniz:

```python
from synthdiet.education import built_in_cases

with open("calisma_kagidi.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```

`as_html()` çıktısı yalın bir HTML olduğundan, üzerine kendi CSS
stilinizi uygulayabilir veya PDF'e dönüştürebilirsiniz.

## Eğitimde tipik bir oturum akışı

1. Öğretmen, sınıfa belirli bir vakayı projeksiyonla gösterir
   (`case.as_markdown()`).
2. Öğrenciler 20-30 dakika içinde bir diyet planı hazırlar.
3. Öğrenci planları, `OSCEStation.grade(student_diet)` ile
   otomatik olarak puanlanır.
4. Daha sonra `synthdiet.DietSimulator` ile öğrencinin planı 12 hafta
   simüle edilir; sonuçlar, vakanın referans çözümünün beklenen
   sonuçlarıyla karşılaştırılır.
5. Sınıf, hangi planın en iyi sonuca yol açtığını ve nedenini
   tartışır.

Bu akış, hem klinik karar verme becerisini hem de simülasyona dayalı
nicel düşünme becerisini birlikte geliştirir.
