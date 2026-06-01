
# DagPakketVerhuur Dashboard — Master Blueprint voor Claude

Dit document is bedoeld als 1-op-1 brief aan Claude. Bevat alle keuzes die zijn gemaakt, zodat Claude alleen nog hoeft te coderen.

## 0. Tech stack & host (vastgelegd)

- React 19 + TanStack Start v1 + Vite 7 + Tailwind v4 (template draait al)
- Supabase project `snjkmikrlkyalvjaadia` (bestaand, blijft)
- Host: `dashboard.dagpakketverhuur.nl` (custom domain via Lovable publish)
- WooCommerce site `dagpakketverhuur.nl` blijft de bron van boekingen
- **n8n wordt uitgefaseerd** — Supabase ↔ Woo wordt directe REST koppeling + webhook
- Boekhouding: **Moneybird** koppeling (facturen pushen)
- Betalingen: alleen in-dashboard registratie, geen Mollie nu
- WhatsApp: alleen via `wa.me` deeplink-knop, geen API
- Mail: Lovable Emails (geen externe provider)
- Klantportaal: **nee**, niet nu
- Auth: 1 admin + 1–2 medewerkers, simpele rol (admin / medewerker)

---

## 1. Modules in scope (alles in v1)

1. Boekingen + Klanten + Statistieken
2. Offertes + Facturen (Moneybird sync)
3. Magazijn: paklijsten, barcode/QR scan, beschikbaarheidskalender, schadefoto's
4. Communicatie: email triggers + WhatsApp deeplinks

Geen klantportaal, geen Mollie, geen Twilio.

---

## 2. Datamodel (volledige tabellenlijst)

Bestaand (NIET aanraken): `bookings`, `booking_items`, `products`.

Nieuw / uit te breiden:

| Tabel | Doel |
|---|---|
| `customers` | Auto-aggregatie uit bookings (email = key) |
| `customer_notes` | Vrije notities, pinned-flag |
| `customer_tags` | Labels (VIP, slechte betaler, etc.) |
| `user_roles` | enum: `admin`, `medewerker` |
| `audit_log` | Wie deed wat, wanneer |
| `product_stats` | View: aantal verhuurd + omzet per product |
| `quotes` | Offertes (status: nieuw → verstuurd → akkoord/afgewezen) |
| `quote_items` | Regels op offerte |
| `invoices` | Facturen + Moneybird-id |
| `invoice_items` | Regels op factuur |
| `payments` | Handmatige betaalregistratie |
| `deposits` | Borg per boeking + schadekosten |
| `contracts` | Digitale handtekening (PNG + PDF) |
| `availability_calendar` | Per product per dag (afgeleid uit booking_items) |
| `damage_reports` | Schadefoto's bij uitgifte/retour |
| `scan_events` | Barcode/QR scans (inpak/uit/retour) |
| `cleaning_status` | Schoonmaak-checklist na retour |
| `email_log` | Welke mail naar wie, wanneer, template |
| `whatsapp_log` | Welke deeplink gegenereerd (niet verzonden) |

Alle nieuwe tabellen krijgen RLS: admin = alles, medewerker = lezen + status-updates, geen delete.

---

## 3. WooCommerce koppeling (vervangt n8n)

### Inkomend (Woo → Dashboard)
- Webhook endpoint `src/routes/api/public/woo/order.ts`
- Triggers: `order.created`, `order.updated`
- HMAC signature check met `WOO_WEBHOOK_SECRET`
- Upsert in `bookings` + `booking_items`
- Aggregatie naar `customers` via trigger

### Uitgaand (Dashboard → Woo)
- Server fn `syncWooProducts` — haalt producten + stock op (cron 1×/uur)
- Server fn `updateWooStock` — bij retour stock terugschrijven

### Secrets nodig
- `WOO_BASE_URL`
- `WOO_CONSUMER_KEY`
- `WOO_CONSUMER_SECRET`
- `WOO_WEBHOOK_SECRET`

---

## 4. BTW & prijzen

- **Default 21%** per product
- **9%** voor categorie `consumpties` (popcorn, suikerspin, frisdrank, ingrediënten)
- Per product override-veld `vat_rate` (21 | 9)
- Facturen splitsen automatisch BTW-totalen per tarief

---

## 5. Offerte → Factuur flow

```
WooCommerce order type="offerte"
   → bookings.booking_status = "offerte"
   → verschijnt in /offertes pipeline
   → status: nieuw → verstuurd → nagebeld → akkoord/afgewezen
   → bij akkoord: knop "Maak factuur"
   → factuur lokaal opgeslagen + gepusht naar Moneybird
   → betaalstatus handmatig bijwerken (geen Mollie)
```

Reminder: na 3 dagen "verstuurd" zonder reactie → taak "Nabellen offerte".

PDF generator: `jspdf` + logo, BTW-splitsing, geldig 14 dagen.

---

## 6. Moneybird koppeling

- OAuth2 via Moneybird (eenmalig connect-knop in Instellingen)
- Server fn `pushInvoiceToMoneybird` bij elke factuur-aanmaak
- Contacts sync: klant zonder Moneybird-id wordt aangemaakt bij eerste factuur
- Webhook `api/public/moneybird/webhook` voor betaalstatus terug
- Secrets: `MONEYBIRD_CLIENT_ID`, `MONEYBIRD_CLIENT_SECRET`, `MONEYBIRD_ADMIN_ID`

---

## 7. Magazijn flow

### Inpakken
- `/inpakken` toont vandaag + morgen
- Per boeking checklist `booking_items` met checkbox + scan-knop
- Scan via telefooncamera (`@zxing/browser`) → matcht barcode op `products.barcode`
- Klaar → `bookings.booking_status = "packed"`

### Beschikbaarheidskalender
- `/voorraad/<productId>` toont kalender 90 dagen vooruit
- Gereserveerd (bookings status `processing`) vs Uit (status `packed`/`shipped`)
- Waarschuwing rood als reserveringen > stock_total

### Schade
- Bij uitgifte: verplicht 1 foto voor breekbare items (`products.fragile = true`)
- Bij retour: vergelijking, schade-knop → registreert in `damage_reports`
- Schadekosten → automatisch in `deposits` verrekend

### Retour
- `/retour` aparte pagina van inpakken
- Scan terug → `cleaning_status` checklist → klaar

---

## 8. Communicatie

### Email triggers (Lovable Emails)
| Trigger | Template |
|---|---|
| Offerte verstuurd | `quote-sent` |
| Factuur verstuurd | `invoice-sent` |
| Herinnering factuur (T+14) | `invoice-reminder` |
| Leverafspraak T-2 | `delivery-reminder` |
| Onderweg | `on-the-way` |
| Retour bevestigd | `return-confirmed` |

### WhatsApp (alleen deeplinks)
- Knop per boeking: opent `https://wa.me/<phone>?text=<template>`
- Templates: "Onderweg", "10 min", "Vandaag rond X uur"
- Log naar `whatsapp_log` (wat verzonden, niet of gelezen)

---

## 9. Auth & rollen

- Email/password login (Lovable Cloud auth)
- Tabel `user_roles` met enum `admin` | `medewerker`
- Security definer `has_role(user_id, role)` voor RLS
- `_authenticated` layout beschermt alles behalve `/login`
- Medewerker ziet niet: facturen, omzet-statistieken, klant-totalen
- Admin ziet alles

---

## 10. Pagina-overzicht (definitief)

```
/                       Dashboard home (KPI's + vandaag)
/boekingen              Lijst alle boekingen
/boekingen/$id          Detail
/klanten                Lijst
/klanten/$id            Detail + notities + tags
/offertes               Pipeline kanban
/offertes/$id           Detail
/facturen               Lijst
/facturen/$id           Detail + Moneybird status
/inpakken               Vandaag/morgen
/retour                 Retour check-in
/voorraad               Productenlijst
/voorraad/$id           Kalender + schade-historie
/statistieken           Omzet, top producten, utilisatie
/taken                  Reminders (offerte nabellen, etc.)
/instellingen           Moneybird connect, Woo secrets check, gebruikers
/tv                     Magazijn TV-modus (bestaand)
/login                  Auth
```

Verwijder de stub-pagina's die niet in deze lijst staan.

---

## 11. Bouwvolgorde voor Claude (technisch, geen prioriteit-keuze meer)

1. **Fundering**: auth + rollen + `_authenticated` layout + migratie alle tabellen
2. **Woo koppeling**: webhook + sync server fns + secrets opzetten
3. **Klanten + Boekingen + Statistieken**: leesschermen op fundering
4. **Magazijn**: inpakken + scan + kalender + schade + retour
5. **Offertes + Facturen + Moneybird**: pipeline + PDF + push
6. **Communicatie**: email templates + triggers + WhatsApp deeplinks
7. **Polish**: takenlijst, instellingen, dashboard home, RLS audit, security scan

---

## 12. Wat Claude NIET hoeft te beslissen

- Geen keuze tussen Mollie/Stripe → niet doen
- Geen klantportaal → niet bouwen
- Geen Twilio/MessageBird → alleen wa.me links
- Geen alternatieve boekhoudpakketten → Moneybird is de enige
- Geen multi-tenant / workspaces → 1 bedrijf, 1 admin

---

## 13. Acceptatie per module

Elke module is "klaar" als:
- Migratie draait schoon op leeg Supabase project
- Pagina laadt zonder console errors
- CRUD werkt incl. RLS (medewerker mag niet wat hij niet mag)
- Audit log krijgt een regel bij wijziging
- Mobiel (390px breed) bruikbaar — alle magazijn-flows zijn primair mobiel

---

Wil je dat ik dit blueprint document letterlijk als `BLUEPRINT.md` in de repo zet zodat je het direct aan Claude kan geven? Of eerst nog ergens iets aanpassen / toevoegen?
