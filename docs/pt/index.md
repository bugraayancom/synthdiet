# Documentação do synthdiet (Português)

`synthdiet` é uma biblioteca Python para gerar pacientes sintéticos
com quadros clínicos realistas e simular intervenções dietéticas
sobre eles.

> Outros idiomas: [English](../index.md) · [Türkçe](../tr/index.md) · [Español](../es/index.md) · [Français](../fr/index.md) · [Deutsch](../de/index.md) · [Italiano](../it/index.md) · [中文](../zh/index.md) · [日本語](../ja/index.md)
## Autor

**Buğra Ayan** — Ancara / Turquia

- Site: <https://bugraayan.com>
- E-mail: <bugraayan.com@gmail.com>
- Google Scholar:
  <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

## Conteúdo

### Tutoriais

1. [Início rápido](tutorials/01_quickstart.md) — gerar paciente,
   aplicar dieta e simular.
2. [Projetar e executar um ECR](tutorials/02_rct.md) — ensaios
   randomizados com `synthdiet.trials`.
3. [Inferência causal](tutorials/03_causal.md) — análises
   contrafactuais, ATE, CATE e confundimento.
4. [Casos clínicos e OSCE](tutorials/04_case_studies.md) — cenários
   de ensino com `synthdiet.education`.
5. [Validação contra ECRs publicados](tutorials/05_validation.md) —
   calibração via `synthdiet.validation`.
6. [Usar synthdiet a partir do R](tutorials/06_from_r.md) —
   integração via `reticulate`.

### Referência

- [Referência da API](api.md)

## Citação

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Licença

MIT — veja `LICENSE` na raiz do repositório.
