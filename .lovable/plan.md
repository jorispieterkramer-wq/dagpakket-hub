# DagPakketVerhuur — Volledig uitbouwplan

Alles wat je hebt aangevinkt + jouw 2 extra wensen, opgedeeld in 6 fases. Elke fase is een afgerond stuk dat je kunt testen voordat we doorgaan. Ik werk **één fase per chatbeurt** af — anders wordt het te groot en gaan er dingen kapot.

## Eerst: Lovable Cloud aanzetten
Je gebruikt nu losse Supabase. Om alle nieuwe tabellen (CRM-notities, schadefoto's, contracten, betalingen, suppressielijsten, audit log, rechten, etc.) netjes te beheren mét RLS, migrations en secrets, zetten we **Lovable Cloud** aan. Dat blijft Supabase onder de motorkap — je bestaande `bookings`/`products`/`booking_items` blijven werken — maar nieuwe tabellen, edge logic en secrets lopen via het Lovable project. WooCommerce blijft de bron voor boekingen.

## WooCommerce koppeling (vervangt n8n waar mogelijk)
Directe REST API koppeling: `consumer_key` + `consumer_secret` als secrets. Server function `syncWooBookings` haalt orders op en upsert naar `bookings`/`booking_items`. Webhook endpoint `/api/public/woo/order` voor realtime updates bij nieuwe/gewijzigde orders. Productenmaster synct ook (stock, prijs, BTW-tarief). n8n mag blijven voor wat hij nu extra doet, maar de orderflow gaat rechtstreeks.

---

## Fase 1 — Data fundering & CRM (1 chat)
- Nieuwe tabellen: `customers` (auto-aggregatie uit bookings), `customer_notes`, `customer_tags`, `audit_log`, `product_stats` (view: aantal verhuurd + omzet per product), `user_roles` (admin/magazijn/chauffeur).
- WooCommerce sync server function + webhook endpoint.
- **Klantenpagina** volledig uitgewerkt: lijst, detailpagina met alle boekingen, notities, tags, totaalomzet per klant, contactgegevens.
- **Statistieken per product**: aantal keer verhuurd, totaalomzet, utilisatiegraad, top 10.
- Audit log helper (overal `logAction()` voor wijzigingen).

## Fase 2 — Geld: offertes, facturen, betalingen, contracten (1 chat)
- Tabellen: `quotes`, `invoices`, `payments`, `contracts`, `deposits`.
- **Offerteflow**: website-boeking met type "offerte" landt in nieuwe pagina **Offertes pipeline** (nieuw → verstuurd → nagebeld → akkoord/afgewezen). Reminder na 3 dagen → taak "Nabellen offerte" automatisch aangemaakt. PDF-offerte generator (jsPDF) met logo, BTW 9/21%, geldig 14 dagen.
- **Facturen**: PDF generator, automatische BTW-splitsing, factuurnummer-reeks, status (concept/verstuurd/betaald/herinnering).
- **Mollie**: payment links voor aanbetaling, restbetaling, borg. Webhook `/api/public/mollie/webhook` update status.
- **Borg-afhandeling**: bij retour kun je schadekosten invoeren → automatisch verrekend met borg → restitutie via Mollie refund.
- **Digitaal contract**: bij ophalen/bezorgen handtekening op tablet (canvas signature pad), opgeslagen als PNG in storage + PDF.

## Fase 3 — Magazijn pro: scan, beschikbaarheid, schade (1 chat)
- Tabellen: `availability_calendar` (per product per dag), `damage_reports`, `scan_events`, `cleaning_status`.
- **Beschikbaarheidskalender per artikel**: voorkomt dubbelboekingen, toont reservering vs. echt uit. Wordt automatisch berekend uit `booking_items`.
- **Barcode/QR scan flow** (telefooncamera via `@zxing/browser`): bij inpakken scannen → bevestig in paklijst. Bij uitgifte: scannen → status "uit". Bij retour: scannen → status "terug" → schoonmaak-checklist.
- **Schadefoto's**: bij uitgifte foto-upload (verplicht voor breekbare items), bij retour vergelijken. Storage bucket `damage-photos`.
- **Retour/check-in pagina** apart van inpakken.

## Fase 4 — Communicatie: e-mail + WhatsApp + klantportaal (1 chat)
- **Lovable Emails** voor transactional: offerte-versturen, factuur, aanbetalingherinnering, leverafspraak, "wij komen morgen tussen X-Y".
- **WhatsApp** via Twilio of MessageBird (kies bij start): templates "We zijn er vandaag rond 10:00", "We zijn nu onderweg", "We zijn er over 10 min". Knop in bezorgingspagina per stop.
- **Automatische triggers**: T-2 dagen leverafspraak, T-1 dag herinnering, op leverdag "onderweg" knop, dag na evenement retour-bevestiging.
- **Klantportaal** (publieke route `/portaal/<token>`): klant ziet eigen boekingen, kan wijzigen tot T-7, contracten downloaden, facturen zien, online betalen.

## Fase 5 — Prijzen, rapportages, leveranciers, rechten (1 chat)
- **Prijslijsten**: dagprijs/weekendprijs/weekprijs/pakketprijs per product, kortingscodes, automatische pakketkortingen.
- **Rapportages dashboard**: omzet per product/categorie/maand, utilisatiegraad (% verhuurde dagen), DSO (gemiddelde dagen tot betaling), top klanten, voorspelling drukke weken.
- **Leveranciers** tabel + koppeling aan reparaties en aankopen.
- **Multi-user rechten**: `user_roles` met enum (admin/magazijn/chauffeur/finance), RLS-policies per tabel, UI verbergt menu-items per rol.

## Fase 6 — Live-ready: auth, beveiliging, polish (1 chat)
- **Login** (email + password, met optie Google). Auth-protected routes via `_authenticated` layout.
- **RLS** aanzetten op alle tabellen.
- **Security scan** + memory bijwerken.
- **Backup-export** functie (CSV-dump alle tabellen).
- Cron jobs: dagelijkse offerte-reminder check, facturen-herinnering, sync WooCommerce.
- Final QA: alle stub-pagina's vervangen, alle modules getest, lege-states gepolijst.

---

## Wat ik nu nodig heb om Fase 1 te starten:

1. **Lovable Cloud aanzetten** (ik doe dit als je akkoord bent).
2. **WooCommerce gegevens** — heb je een staging site of mag ik op de live site? Ik ga je vragen om `WOO_URL`, `WOO_CONSUMER_KEY`, `WOO_CONSUMER_SECRET` als secrets toe te voegen wanneer we zover zijn.
3. **Voor Fase 2 later**: heb je een **Moneybird** account dat je wilt koppelen, of houden we facturen volledig in het dashboard? En heb je een **Mollie** account?
4. **Voor Fase 4 later**: voorkeur voor WhatsApp via **Twilio** of **MessageBird**? (Twilio is makkelijker, MessageBird is goedkoper in NL).

## Akkoord?
Antwoord met **"start Fase 1"** dan zet ik Lovable Cloud aan en bouw ik fase 1 volledig uit (CRM + WooCommerce sync + statistieken per product + audit log). Of geef aan welke fase je liever eerst hebt — volgorde is flexibel, ik adviseer alleen Fase 1 als basis omdat de rest erop bouwt.
