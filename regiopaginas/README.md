# Regiopagina's — vaste SEO-architectuur (proef: Lasergame)

- `build.py` — generator: homepage-stijl (Shadow DOM), templates **A** (hub), **B** (provincie), **C** (stad),
  WhatsApp-tracking-bridge (gelijk aan header/footer/klantenservice), echte dpv-shop-productkaarten in de light DOM.
- `content_lasergame.py` — inhoud per pagina (hub, Drenthe, Emmen). Nieuwe regio = nieuw blok in een content-bestand.
- `cards/` — echte productkaarten (Compact 47238, XL 47235) van de categoriepagina; worden op de pagina live ververst.
- `out/` — gegenereerde HTML-widget per slug + `*.seo.json` (Yoast-title en meta).
- `deploy.py` — zet `out/<slug>.html` in de bestaande HTML-widget op **staging** (alleen `settings.html`).
- `preview/` — lokale screenshots (desktop 1440px, mobiel 390px).

Bouwen: `cd regiopaginas && python3 build.py`
