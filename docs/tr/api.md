# API Referansı

Bu sayfa, `synthdiet` kütüphanesinin halka açık API yüzeyini Türkçe
açıklamalarla listeler. Tam Sphinx tarafından üretilen otomatik
dokümantasyon İngilizce sürümdedir; bu liste, sınıf ve fonksiyonları
hızlıca taramanıza yardımcı olmak için bir çeviri özetidir.

## Hasta modeli

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.Patient` | Demografi, antropometri, biyobelirteçler, yaşam tarzı, tanılar ve ilaçları bir arada tutan ana hasta nesnesi. |
| `synthdiet.Demographics` | Yaş, cinsiyet, ülke gibi demografik alanlar. |
| `synthdiet.Anthropometrics` | Boy, kilo, bel çevresi gibi antropometrik ölçümler. |
| `synthdiet.Biomarkers` | Laboratuvar değerleri (HbA1c, LDL, kan basıncı vb.). |
| `synthdiet.Lifestyle` | Fiziksel aktivite, sigara, alkol gibi yaşam tarzı bilgileri. |

## Hastalıklar

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.Disease` | Tüm hastalıklar için temel sınıf. |
| `synthdiet.NutritionalConstraints` | Hastalığa özel beslenme kısıtları. |
| `synthdiet.available_diseases()` | Kayıtlı tüm hastalıkların listesini döner. |
| `synthdiet.get_disease(name)` | İsme göre hastalık sınıfını döner. |

## Diyet planları

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.DietPlan` | Bir diyet planının yapısal temsili. |
| `synthdiet.mediterranean_diet()` | Akdeniz diyeti ön ayarı. |
| `synthdiet.dash_diet()` | DASH diyeti ön ayarı. |
| `synthdiet.keto_diet()` | Ketojenik diyet ön ayarı. |
| `synthdiet.low_fodmap_diet()` | Düşük FODMAP diyeti ön ayarı. |
| `synthdiet.low_sodium_renal_diet()` | Düşük sodyumlu renal diyet ön ayarı. |
| `synthdiet.diabetic_diet()` | Diyabetik diyet ön ayarı. |
| `synthdiet.vegan_diet()` | Vegan diyet ön ayarı. |
| `synthdiet.standard_diet()` | Standart referans diyet (kontrol kolu için). |

## Üreteçler (Generators)

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.RandomPatientGenerator` | Sıfırdan rastgele hasta üreteci. |
| `synthdiet.DistributionPatientGenerator` | Dağılım parametrelerinden hasta üreteci. |
| `synthdiet.CopulaPatientGenerator` | Kopula tabanlı, korele özelliklerle hasta üreteci. |
| `synthdiet.CohortGenerator` | Bir kohort spesifikasyonundan hasta listesi üretir. |
| `synthdiet.CohortSpec` | Kohort yapılandırması (boyut, prevalanslar). |
| `synthdiet.DiseaseSpec` | Bir hastalığın kohorttaki dağılımının tanımı. |
| `synthdiet.MarkovProgressionGenerator` | Hastalık ilerlemesi için Markov tabanlı üreteç. |

## Simülasyon

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.DietSimulator` | Ana diyet simülatörü (basit + Hall 2011 motoru). |
| `synthdiet.SimulationResult` | Simülasyon sonucu (sıralı biyobelirteç gidişatı). |
| `synthdiet.HallSimulation` | Hall 2011 vücut kompozisyonu modelinin uygulaması. |
| `synthdiet.HallSimulationParameters` | Hall modeli için ayarlanabilir parametreler. |

## Klinik çalışmalar (Trials)

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.trials.ParallelTrial` | Paralel kollu RKT motoru. |
| `synthdiet.trials.CrossoverTrial` | Çapraz tasarım (crossover) RKT'leri. |
| `synthdiet.trials.FactorialTrial` | 2×2 faktöriyel tasarım RKT'leri. |
| `synthdiet.trials.intention_to_treat` | Tedavi niyetine göre (ITT) analiz. |
| `synthdiet.trials.per_protocol` | Protokol başına (PP) analiz. |

## Diyet kalitesi indeksleri

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate Healthy Eating Index 2010. |
| `synthdiet.indices.MEDAS` | Akdeniz diyetine bağlılık ölçeği. |
| `synthdiet.indices.DASHScore` | DASH diyeti uyum skoru. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Nedensel çıkarım

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.causal.counterfactual_run` | Aynı hastayı iki diyet altında karşı-olgusal olarak simüle eder. |
| `synthdiet.causal.ATEEstimator` | Ortalama Tedavi Etkisi (ATE) tahmincisi. |
| `synthdiet.causal.cate_by_subgroup` | Alt gruplara göre koşullu ATE (CATE) hesaplar. |
| `synthdiet.causal.ConfoundingExperiment` | IPTW ve g-formülü ile yanıltıcı düzeltmeli deney. |
| `synthdiet.causal.DietDAG` | Hafif bir Yönlü Asiklik Graf (DAG) yardımcı sınıfı. |

## Eğitim

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.education.CaseStudy` | Tek bir klinik vaka çalışmasını temsil eder. |
| `synthdiet.education.OSCEStation` | OSCE tarzı puanlama istasyonu. |
| `synthdiet.education.built_in_cases()` | Yerleşik 15 vakanın tam listesini döner. |

## İstatistikler ve gürültü

| Sembol | Açıklama |
|--------|----------|
| `synthdiet.stats.sample_size_continuous` | Sürekli sonuçlar için örneklem büyüklüğü. |
| `synthdiet.stats.sample_size_binary` | İkili (binary) sonuçlar için örneklem büyüklüğü. |
| `synthdiet.stats.bootstrap_ci` | Bootstrap güven aralığı. |
| `synthdiet.stats.permutation_test` | Permütasyon testi. |
| `synthdiet.stats.fdr_bh` | Benjamini-Hochberg FDR düzeltmesi. |
| `synthdiet.stats.ancova_baseline_adjusted` | Başlangıç düzeyine göre ayarlanmış ANCOVA. |
| `synthdiet.noise.add_lab_measurement_error` | Laboratuvar değerlerine ölçüm hatası ekler. |
| `synthdiet.noise.inject_mcar_missing` | Tamamen rastgele eksik veri (MCAR). |
| `synthdiet.noise.inject_mar_missing` | Rastgeleye yakın eksik veri (MAR). |
| `synthdiet.noise.inject_mnar_missing` | Rastgele olmayan eksik veri (MNAR). |
