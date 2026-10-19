# Back-up LIVE — 19-10-2026, vóór livegang lasergame-proefpagina's

Gemaakt door `regiopaginas/deploy_live.py`, direct vóór het overschrijven van elke pagina.

| Pagina | ID | Bestanden |
|---|---|---|
| /lasergame-huren/ | 49762 | `page-49762-lasergame-huren.*` |
| /lasergame-huren-drenthe/ | 49694 | `page-49694-lasergame-huren-drenthe.*` |
| /lasergame-huren-emmen/ | 49882 | `page-49882-lasergame-huren-emmen.*` |

Per pagina: `.json` (volledige page-JSON, context=edit), `.content.html` (post content),
`.elementor.json` (_elementor_data), `.yoast.json` (Yoast title/meta via bulk editor).

Terugzetten: `meta._elementor_data` uit `.json` terugschrijven via `POST /wp-json/wp/v2/pages/<id>`,
daarna `DELETE /wp-json/elementor/v1/cache`.
