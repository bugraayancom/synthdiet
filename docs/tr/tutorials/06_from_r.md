# `synthdiet`'i R'dan `reticulate` ile Kullanma

Beslenme araştırmacılarının bir kısmı temel olarak R kullanır.
`synthdiet` ayrı bir R paketi sağlamaz, ancak `reticulate` üzerinden
sorunsuz çalışır.

## Bir defalık kurulum

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

Bu komutlar yerel bir Python sanal ortamı oluşturur, içine
`synthdiet`'i kurar ve R oturumunu o ortama bağlar. İstediğiniz
zaman `py_config()` ile hangi Python'un kullanıldığını
doğrulayabilirsiniz.

## Bir kohort üretmek

```r
synthdiet <- import("synthdiet")

spec <- synthdiet$CohortSpec(
  size = 100L,
  diseases = list(
    synthdiet$DiseaseSpec("type_2_diabetes", prevalence = 0.4),
    synthdiet$DiseaseSpec("hypertension",     prevalence = 0.4)
  )
)
cohort <- synthdiet$CohortGenerator(spec, seed = 42L)$generate()
```

> R'da tamsayıların sonuna `L` eklemeyi unutmayın; aksi halde
> Python tarafında `float` olarak görünürler ve Python'un `int`
> beklediği yerler hata verir.

## Paralel bir RKT çalıştırma

```r
trial <- synthdiet$trials$ParallelTrial(
  cohort = cohort,
  arms = list(
    "control"      = synthdiet$standard_diet(),
    "intervention" = synthdiet$mediterranean_diet()
  ),
  duration_weeks  = 12L,
  primary_outcome = "hba1c_pct"
)
result <- trial$run(seed = 1L)
itt <- result$intention_to_treat()
cat("ATE:", itt$diff,
    "(%95 GA", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## Sonucu R'a geri taşıma

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(ortalama_delta = mean(delta_hba1c_pct))
```

`result$outcomes` Python tarafında bir `pandas.DataFrame`'dir;
`py_to_r` çağrısıyla R'da tipik bir `data.frame`'e dönüştürülür.
Buradan sonra `dplyr`, `tidyr`, `lme4` gibi alıştığınız tüm R
araçları kullanılabilir.

## R'da grafik çizme

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Kol",
    y = "HbA1c değişimi (yp)",
    title = "12 haftalık sentetik klinik çalışma"
  )
```

## İpuçları ve sorun giderme

- **Performans**: `synthdiet` ana hesaplamaları Python'da yapar;
  R ile Python arasındaki köprü hafif yüktedir. Yine de büyük
  kohortlarda (>10.000 hasta) sonuçları toplu olarak Python tarafında
  hesaplayıp, sadece özet tabloyu R'a almak daha hızlıdır.
- **Bellek**: Birden fazla simülasyon yürütüyorsanız `gc()` ve
  `py_gc()` çağrılarını periyodik olarak ekleyin.
- **Sürüm sabitleme**: Yeniden üretilebilirlik için
  `virtualenv_install("synthdiet-env", packages = c("synthdiet==0.1.0"))`
  gibi sabit bir sürüm belirtin.

R kullanıcıları için tipik bir iş akışı: simülasyonu Python'da
çalıştır, çıktıyı `data.frame`'e çevir, R tarafında modelleme ve
görselleştirmeyi yap.
