# Back-up staging — 19-10-2026 (vóór herbouw lasergame-regiopagina's)

Bron: https://staging.dagpakketverhuur.nl (REST `wp/v2/pages?context=edit` + Yoast `get-post-seo-data`).

| Pagina | ID | Bestanden |
|---|---|---|
| /lasergame-huren/ (hub) | 49762 | `page-49762.json`, `page-49762.elementor.json`, `yoast-49762.json` |
| /lasergame-huren-drenthe/ | 49694 | `page-49694.json`, `page-49694.elementor.json`, `yoast-49694.json` |
| /lasergame-huren-emmen/ | 49882 | `page-49882.json`, `page-49882.elementor.json`, `yoast-49882.json` |
| / (homepage, alleen referentie) | 3883 | `page-3883-home.json`, `page-3883-home.elementor.json`, `yoast-3883.json` |

Terugzetten: `_elementor_data` uit `page-<id>.json` → `meta._elementor_data` terugschrijven via REST,
en `seo_title` / `meta_description` uit `yoast-<id>.json` via Yoast `update-post-seo-data`.
