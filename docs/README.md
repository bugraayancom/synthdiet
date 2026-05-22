# synthdiet documentation index

`synthdiet` documentation is available in 9 languages. Pick yours:

| Language | Index | Tutorials | API |
|----------|-------|-----------|-----|
| English | [index](index.md) | [tutorials/](tutorials/) | [api](api.md) |
| Türkçe | [index](tr/index.md) | [tutorials/](tr/tutorials/) | [api](tr/api.md) |
| Español | [index](es/index.md) | [tutorials/](es/tutorials/) | [api](es/api.md) |
| Français | [index](fr/index.md) | [tutorials/](fr/tutorials/) | [api](fr/api.md) |
| Deutsch | [index](de/index.md) | [tutorials/](de/tutorials/) | [api](de/api.md) |
| Português | [index](pt/index.md) | [tutorials/](pt/tutorials/) | [api](pt/api.md) |
| Italiano | [index](it/index.md) | [tutorials/](it/tutorials/) | [api](it/api.md) |
| 中文 (简体) | [index](zh/index.md) | [tutorials/](zh/tutorials/) | [api](zh/api.md) |
| 日本語 | [index](ja/index.md) | [tutorials/](ja/tutorials/) | [api](ja/api.md) |

Each language folder mirrors the same structure:

```
docs/<lang>/
├── index.md
├── api.md
└── tutorials/
    ├── 01_quickstart.md
    ├── 02_rct.md
    ├── 03_causal.md
    ├── 04_case_studies.md
    ├── 05_validation.md
    └── 06_from_r.md
```

The English documentation under `docs/` (root) is also the canonical
source built by Sphinx (`docs/conf.py`). Translations are
human-curated companion documents and are not yet wired into the
Sphinx build.

## Contributing translations

Want to add another language? Create a new sibling folder
`docs/<iso-code>/` mirroring the structure above, and add a
`README.<iso-code>.md` at the repository root. Please keep:

- Code blocks (Python, R, bash) in their original form so the API
  contract stays identical across languages.
- File names (`01_quickstart.md` etc.) consistent with the English
  version for easier cross-referencing.
- The language switcher row at the top of every `index.md` and root
  `README.<lang>.md` updated to include the new language.
