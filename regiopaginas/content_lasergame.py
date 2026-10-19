"""
Inhoud lasergame-regiopagina's (proef: hub, Drenthe, Emmen).

Vaste feiten (niet afwijken):
- gratis bezorging vanaf €150 (altijd met die voorwaarde), geen borg,
  gratis afhalen in Fochteloo, DHL door heel NL, lasergame vanaf 6 jaar
- NOOIT een aantal laserguns noemen
- geen verzonnen reviews, reistijden, kilometers, klanten of lokale feiten

Bronnen op de site: /contact/ (bezorging, afhalen, retour, annuleren, zakelijk),
productpagina's Compact/XL (verschil, gebruik), /zakelijk/ (aanvraag),
homepage (review Jurgen Elshof).
"""
from build import url, WA, TEL

U = url('/wp-content/uploads')
IMG = {
    'bos': (U + '/2025/05/52a59f90-fec7-40b7-a816-61c4fadf6b13-2-min.jpg',
            'Groep spelers met laserguns tijdens een lasergame in het bos'),
    'kids': (U + '/2026/02/Ontwerp-zonder-titel-_1__11zon.webp',
             'Kinderen met laserguns in de tuin tijdens een kinderfeestje'),
    'tuin': (U + '/2026/02/Ontwerp-zonder-titel_11zon.webp',
             'Spelers met laserguns verstoppen zich achter de struiken in een tuin'),
    'veld': (U + '/2025/03/IMG_3620-min-768x1024.jpg',
             'Groep speelt lasergame op een grasveld met pallets als dekking'),
}

COMPACT = url('/product/lasergame-compacte-huren/')
XL = url('/product/lasergame-xl-huren/')
HUB = url('/lasergame-huren/')
CAT = url('/product-category/activiteiten-attracties-huren/attracties-activiteiten-huren/')  # live: 301-doel van /product-category/lasergame-huren/, 200 zonder redirect
CONTACT = url('/contact/')

# ------------------------------------------------------------------ gedeeld
TRUST = [
    ('shield', 'Geen borg', 'Je betaalt alleen de huurprijs'),
    ('pin', 'Gratis afhalen in Fochteloo', 'Vanaf 16:00 de dag voor je event'),
    ('truck', 'Levering in heel Nederland', 'Verzonden met DHL'),
    ('gift', 'Gratis verzending vanaf €150', 'Met DHL, bij een besteding vanaf €150'),
]

PRODUCT_CHECKS = [
    'Binnen 5 minuten speelklaar',
    'Binnen en buiten te spelen',
    'Geschikt vanaf 6 jaar',
    'Geen borg — je betaalt alleen de huurprijs',
]

# Echte voorwaarden van /contact/.
LEV_EIGEN = lambda gebied: {
    'icon': 'truck', 'h3': 'Wij bezorgen en halen op',
    'p': f'In {gebied} bezorgen we ook zelf, op het tijdslot dat je bij het afrekenen kiest. '
         'Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.',
    'link': (CONTACT, 'Bereken je bezorgkosten'),
}
LEV_DHL = {
    'icon': 'calendar', 'h3': 'Verzending met DHL',
    'p': 'Lasergames versturen we met DHL door heel Nederland, voor €16 per pakket en gratis vanaf €150. '
         'Je pakket is er één tot twee werkdagen voor je huurdatum.',
}
LEV_AFHALEN = {
    'icon': 'pin', 'h3': 'Gratis afhalen in Fochteloo',
    'p': 'Ophalen op Verlaat 3 in Fochteloo is altijd gratis: vanaf 16:00 de dag voor je event, '
         'inleveren tot 16:00 de dag erna. Die uren tellen niet als extra huurdag.',
}

B2B_CHECKS = [
    'Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen',
    'Betalen op factuur, met je eigen referentie of PO-nummer',
    'Alle prijzen inclusief 21% btw, apart op je factuur',
]

PAGES = []

# ================================================================== A — HUB
PAGES.append({
    'template': 'A', 'id': 49762, 'slug': 'lasergame-huren', 'naam': 'LASERGAME HUREN (HUB)',
    'plaats': 'Nederland',
    'seo_title': 'Lasergame huren | Compact & XL | Dagpakketverhuur',
    'meta': 'Lasergame huren voor een kinderfeestje, bedrijfsuitje of sportdag. Kies Compact of XL, geen borg, '
            'gratis afhalen in Fochteloo of DHL-levering in heel NL.',
    'product_ids': [47238, 47235], 'cat_url': CAT,
    'product_alts': {47238: 'Lasergame Compact huren', 47235: 'Lasergame XL huren'},
    'hero': {
        'img': IMG['bos'][0], 'alt': IMG['bos'][1], 'pos': '50% 40%',
        'eyebrow': 'Lasergame · Compact & XL',
        'h1': 'Lasergame huren,<br>thuis of op locatie',
        'sub': 'Kies een set die bij je groep past en speel binnen een paar minuten. '
               'Geen borg, gratis afhalen in Fochteloo of verzonden met DHL.',
    },
    'trust': TRUST,
    'products': {
        'h2': 'Kies je lasergame', 'cat_link': CAT,
        'lead': 'Twee sets die op dezelfde manier werken. Het verschil zit in de speelduur per ronde.',
        'checks': PRODUCT_CHECKS, 'info_h3': 'Bij beide sets',
        'info_link': (CAT, 'Bekijk ook de bundels en accessoires'),
    },
    'keuze': {
        'h2': 'Welke set past bij jouw groep?',
        'items': [
            {'tag': 'Lasergame Compact', 'h3': 'Kinderfeestje of kleinere groep',
             'p': 'Kleiner en voordeliger. De guns hebben drie balken met levens, dus rondes zijn kort en vol actie. '
                  'Handig voor thuis, in de tuin of een grote ruimte binnen.',
             'link': (COMPACT, 'Bekijk Lasergame Compact')},
            {'tag': 'Lasergame XL', 'h3': 'Grotere groep of langer spel',
             'p': 'Vier balken met levens, dus een uitgebreider spel per ronde. '
                  'Fijn voor tieners, volwassenen en bedrijfsuitjes op een veld, in een park of in een hal.',
             'link': (XL, 'Bekijk Lasergame XL')},
            {'icon': 'phone', 'soft': True, 'h3': 'Twijfel je nog?',
             'p': 'Vertel ons hoe groot je groep is en waar je speelt, dan denken we mee. '
                  'Bel 085 212 9150, ma–za van 9:00 tot 21:00.',
             'link': (TEL, 'Bel ons')},
        ],
    },
    'gelegenheden': {
        'h2': 'Voor elke gelegenheid',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Vanaf 6 jaar speelt iedereen mee. Combineer het met andere activiteiten voor een compleet feest.',
             'link': (url('/kinderfeestje/'), 'Kinderfeestje regelen')},
            {'icon': 'users', 'h3': 'Verjaardag of vriendengroep',
             'p': 'In de tuin, in het park of op een veld: jij kiest waar je speelt en hoe fanatiek het wordt.'},
            {'icon': 'briefcase', 'h3': 'Bedrijfsuitje',
             'p': 'Een actieve teamactiviteit zonder begeleiding: iedereen kan direct meedoen.',
             'link': (url('/zakelijk/'), 'Zakelijk huren')},
            {'icon': 'school', 'h3': 'School, sportdag of vereniging',
             'p': 'Binnen één werkdag een vaste prijs en betalen op factuur. We denken mee over de planning.',
             'link': (url('/zakelijk/'), 'Zakelijke prijs aanvragen')},
        ],
    },
    'stappen': {
        'h2': 'Zo werkt huren',
        'items': [
            ('Kies je set', 'Compact of XL, en hoeveel je nodig hebt. Zet alles in je winkelwagen.'),
            ('Kies je datum', 'Bij het afrekenen kies je je eventdatum. Je betaalt de dagprijs voor die dag.'),
            ('Levering of afhalen', 'Wij bezorgen in Noord-Nederland, DHL levert in heel Nederland, of je haalt gratis af in Fochteloo.'),
            ('Retour', 'Lever alles compleet en droog in tot 16:00 de dag na je event, of zet het klaar om op te halen.'),
        ],
    },
    'regio': {
        'h2': 'Lasergame huren in Noord-Nederland',
        'lead': 'In Friesland, Drenthe en Groningen bezorgen we ook zelf. Kies je provincie voor bezorging, afhalen en veelgestelde vragen bij jou in de buurt.',
        'items': [
            ('Friesland', 'Lasergame huren in Friesland', url('/lasergame-huren-friesland/')),
            ('Drenthe', 'Lasergame huren in Drenthe', url('/lasergame-huren-drenthe/')),
            ('Groningen', 'Lasergame huren in Groningen', url('/lasergame-huren-groningen/')),
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk',
        'h2': 'Voor bedrijven, scholen en verenigingen',
        'p': 'Organiseer je een teamuitje, sportdag of clubactiviteit? Vertel ons wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS,
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
    },
    'review': {'h2': 'Ervaringen van onze klanten', 'sub': 'Gemiddeld 4,8 op Google'},
    'faq': {
        'h2': 'Veelgestelde vragen',
        'intro': 'Staat je vraag er niet bij? Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.',
        'items': [
            ('Wat is het verschil tussen Compact en XL?',
             'Beide sets werken op dezelfde manier. De Compact guns hebben drie balken met levens, de XL guns vier. '
             'Compact is kleiner en voordeliger en ideaal voor snelle spellen; XL geeft een uitgebreider spel per ronde.'),
            ('Vanaf welke leeftijd is lasergame geschikt?',
             'Vanaf 6 jaar. Kinderen, tieners en volwassenen kunnen meedoen zonder ervaring.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg. Je hoeft dus niets vooruit te betalen dat je later terugkrijgt.'),
            ('Wat kost bezorgen?',
             'Lasergames versturen we met DHL door heel Nederland: €16 per pakket, gratis vanaf €150. '
             'In Noord-Nederland bezorgen we ook zelf. Het tarief en de gratis-grens hangen af van je zone. '
             f'<a href="{CONTACT}">Bereken het met je postcode</a>. Zelf afhalen in Fochteloo is altijd gratis.'),
            ('Kan ik binnen en buiten spelen?',
             'Ja. Speel in de tuin, in een park, op een veld of binnen in een grote ruimte of hal.'),
            ('Kan ik annuleren of mijn datum wijzigen?',
             'Wijzigen of annuleren kan kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, '
             'inclusief verzend- en bezorgkosten.'),
        ],
    },
    'final': {
        'img': IMG['tuin'][0], 'alt': IMG['tuin'][1],
        'h2': 'Klaar voor een potje lasergame?',
        'p': 'Kies je set, kies je datum en wij regelen de rest. Geen borg, gratis DHL-verzending vanaf €150.',
        'links': [('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== B — DRENTHE
PAGES.append({
    'template': 'B', 'id': 49694, 'slug': 'lasergame-huren-drenthe', 'naam': 'LASERGAME HUREN DRENTHE (PROVINCIE)',
    'plaats': 'Drenthe',
    'seo_title': 'Lasergame huren in Drenthe | Dagpakketverhuur',
    'meta': 'Lasergame huren in Drenthe? Wij bezorgen zelf in Assen, Emmen en omgeving, of je haalt gratis af in Fochteloo. '
            'Geen borg, Compact of XL, vanaf 6 jaar.',
    'product_ids': [47238, 47235], 'cat_url': CAT,
    'product_alts': {47238: 'Lasergame Compact huren', 47235: 'Lasergame XL huren'},
    'hero': {
        'img': IMG['kids'][0], 'alt': IMG['kids'][1], 'pos': '50% 35%',
        'eyebrow': 'Lasergame · Drenthe',
        'h1': 'Lasergame huren in Drenthe',
        'sub': 'Voor een feest in de tuin, een uitje met collega’s of een sportdag. '
               'Wij bezorgen zelf in Drenthe, of je haalt gratis af in Fochteloo.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Drenthe',
        'h2': 'Persoonlijk bezorgd in heel Drenthe',
        'p': [
            'Drenthe valt binnen ons eigen bezorggebied in Noord-Nederland. We brengen je lasergame op het tijdslot '
            'dat je bij het afrekenen kiest en halen alles na je event weer op. Je betaalt geen borg. '
            'Het tarief en de gratis-grens voor bezorgen hangen af van je zone. Bereken het met je postcode.',
            'Liever zelf ophalen? Dat kan altijd gratis in Fochteloo, vanaf 16:00 de dag voor je event. '
            'Of laat je set met DHL versturen: gratis vanaf €150.',
        ],
    },
    'products': {
        'h2': 'Lasergame Compact of XL',
        'lead': 'Compact voor kortere rondes en kleinere groepen, XL voor een uitgebreider spel.',
        'checks': PRODUCT_CHECKS, 'info_h3': 'Bij beide sets',
        'info_link': (HUB, 'Welke set past bij jouw groep?'),
    },
    'toepassingen': {
        'h2': 'Populair in Drenthe',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje in de tuin',
             'p': 'Vanaf 6 jaar speelt iedereen mee. Met struiken, schuurtjes of pallets heb je meteen een speelveld.',
             'link': (url('/kinderfeestje-drenthe/'), 'Kinderfeestje in Drenthe')},
            {'icon': 'briefcase', 'h3': 'Teamuitje of personeelsfeest',
             'p': 'Een actief uitje waar iedereen direct aan mee kan doen, op je eigen locatie.'},
            {'icon': 'school', 'h3': 'Sportdag of schoolevenement',
             'p': 'Speel op het sportveld of in de gymzaal. Scholen betalen op factuur.'},
            {'icon': 'users', 'h3': 'Buurtfeest of vereniging',
             'p': 'Teams tegen elkaar op een grasveld of in het park: makkelijk op te zetten, snel speelklaar.'},
        ],
    },
    'steden': {
        'h2': 'Lasergame huren in Drentse steden',
        'lead': 'Voor deze plaatsen hebben we een eigen pagina met bezorging en vragen uit de buurt.',
        'items': [
            ('Assen', 'Lasergame huren in Assen', url('/lasergame-huren-assen/')),
            ('Emmen', 'Lasergame huren in Emmen', url('/lasergame-huren-emmen/')),
        ],
    },
    'levering': {
        'h2': 'Bezorgen, verzenden of afhalen',
        'lead': 'Kies bij het afrekenen wat voor jou het beste werkt. Op zondag zijn we gesloten; ophalen en inleveren regelen we dan op zaterdag of maandag.',
        'items': [LEV_EIGEN('Drenthe'), LEV_DHL, LEV_AFHALEN],
    },
    'b2b': {
        'kicker': 'Zakelijk in Drenthe',
        'h2': 'Bedrijven, scholen en verenigingen',
        'p': 'Een sportdag, teamuitje of clubactiviteit in Drenthe? Vertel ons wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS[:2],
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Drenthe',
        'intro': 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.',
        'items': [
            ('Bezorgen jullie in heel Drenthe?',
             'Ja, Drenthe valt binnen ons eigen bezorggebied. Het tarief en de gratis-grens hangen af van je zone. '
             f'<a href="{CONTACT}">Bereken het met je postcode</a>. Verzending met DHL is gratis vanaf €150.'),
            ('Kan ik de lasergame zelf ophalen?',
             'Ja, en dat is altijd gratis. Ophalen kan vanaf 16:00 de dag voor je event op de parkeerplaats aan Verlaat 3 in Fochteloo. '
             'We nemen vooraf contact op zodra alles klaarligt.'),
            ('Is het event op zondag?',
             'Op zondag zijn we gesloten. Ophalen en inleveren regelen we dan op zaterdag of maandag, en die dag rekenen we niet als extra huurdag.'),
            ('Kan onze school of vereniging op factuur betalen?',
             'Ja. Vul bij het afrekenen je organisatie en eventueel een referentie in en kies betalen op factuur. '
             'De factuur moet vóór de huurdatum betaald zijn.'),
            ('Vanaf welke leeftijd is lasergame geschikt?',
             'Vanaf 6 jaar. Ook tieners en volwassenen spelen mee, zonder ervaring.'),
        ],
    },
    'final': {
        'img': IMG['bos'][0], 'alt': IMG['bos'][1],
        'h2': 'Lasergame in Drenthe regelen?',
        'p': 'Kies je set en je datum. Geen borg, gratis DHL-verzending vanaf €150.',
        'links': [('Alle lasergame-informatie', HUB), ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== C — EMMEN
PAGES.append({
    'template': 'C', 'id': 49882, 'slug': 'lasergame-huren-emmen', 'naam': 'LASERGAME HUREN EMMEN (STAD)',
    'plaats': 'Emmen',
    'seo_title': 'Lasergame huren in Emmen | Dagpakketverhuur',
    'meta': 'Lasergame huren in Emmen, Klazienaveen of Nieuw-Amsterdam? Wij bezorgen en halen op. '
            'Geen borg, Compact of XL, voor feestjes, scholen en teamuitjes.',
    'product_ids': [47238, 47235], 'cat_url': CAT,
    'product_alts': {47238: 'Lasergame Compact huren', 47235: 'Lasergame XL huren'},
    'hero': {
        'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'pos': '50% 45%',
        'eyebrow': 'Lasergame · Emmen',
        'h1': 'Lasergame huren in Emmen',
        'sub': 'Een lasergame voor in de tuin, het park of de sporthal. '
               'Wij bezorgen in Emmen en de dorpen eromheen.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Emmen',
        'h2': 'Bezorgd bij jou in Emmen',
        'p': [
            'Woon je in Emmen of ergens anders in de hele gemeente Emmen? Dan bezorgen we je lasergame zelf, op het tijdslot '
            'dat je bij het afrekenen kiest. Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.',
            'Speel je binnen, bijvoorbeeld in een sporthal of grote ruimte, of buiten in de tuin of het park? '
            'Beide sets werken binnen en buiten en zijn binnen 5 minuten speelklaar.',
        ],
    },
    'products': {
        'h2': 'Lasergame Compact of XL',
        'lead': 'Compact voor korte rondes en kleinere groepen, XL voor een uitgebreider spel.',
        'checks': PRODUCT_CHECKS, 'info_h3': 'Bij beide sets',
        'info_link': (HUB, 'Hulp bij kiezen'),
    },
    'stappen': {
        'h2': 'Zo werkt huren in Emmen',
        'items': [
            ('Kies je set', 'Zet Lasergame Compact of XL in je winkelwagen.'),
            ('Kies datum en tijdslot', 'Bij het afrekenen kies je je eventdatum en het tijdslot waarop we bezorgen.'),
            ('Wij bezorgen', 'We bezorgen in Emmen op het gekozen tijdslot. Liever zelf ophalen? Dat kan gratis in Fochteloo.'),
            ('Wij halen weer op', 'Zet alles compleet en droog klaar tot 16:00 de dag na je event.'),
        ],
    },
    'gelegenheden': {
        'h2': 'Waarvoor huur je een lasergame in Emmen?',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Vanaf 6 jaar speelt iedereen mee, in de tuin of binnen bij slecht weer.',
             'link': (url('/kinderfeestje-emmen/'), 'Kinderfeestje in Emmen')},
            {'icon': 'users', 'h3': 'Verjaardag of vriendengroep',
             'p': 'Teams kiezen, guns aan en spelen. Geen begeleiding nodig.'},
            {'icon': 'sun', 'h3': 'Buurtfeest of zomerfeest',
             'p': 'Een grasveld of park is genoeg. Combineer het met andere activiteiten voor een hele middag.'},
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk in Emmen',
        'h2': 'Ook voor bedrijven, scholen en verenigingen in Emmen',
        'p': 'Plan je een teamuitje, sportdag of clubactiviteit in Emmen? Vertel ons wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS[:2],
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
    },
    'levering': {
        'h2': 'Levering in Emmen en omgeving',
        'lead': 'We bezorgen in de hele gemeente Emmen, onder meer in deze plaatsen. Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.',
        'plaatsen': ['Emmen', 'Klazienaveen', 'Nieuw-Amsterdam', 'Erica', 'Schoonebeek',
                     'Emmer-Compascuum', 'Nieuw-Weerdinge', 'Zwartemeer'],
        'items': [LEV_EIGEN('Emmen en omgeving'), LEV_AFHALEN, LEV_DHL],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Emmen',
        'intro': 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.',
        'items': [
            ('Bezorgen jullie ook in de dorpen rond Emmen?',
             'Ja, we bezorgen in de hele gemeente Emmen, zoals in Klazienaveen, Nieuw-Amsterdam, Erica en Schoonebeek. '
             f'Het tarief en de gratis-grens hangen af van je zone. <a href="{CONTACT}">Bereken het met je postcode</a>.'),
            ('Kunnen we binnen spelen als het regent?',
             'Ja. Beide sets werken binnen en buiten. Een sporthal, gymzaal of grote ruimte werkt goed.'),
            ('Op welk moment wordt er bezorgd?',
             'Bij het afrekenen kies je een tijdslot. Eén tot twee dagen voor je huurdatum nemen we contact met je op om het te bevestigen.'),
            ('Wat als ik moet annuleren?',
             'Wijzigen of annuleren kan kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, '
             'inclusief bezorgkosten.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg.'),
        ],
    },
    'final': {
        'img': IMG['kids'][0], 'alt': IMG['kids'][1],
        'h2': 'Lasergame in Emmen regelen?',
        'p': 'Kies je set en je datum, wij bezorgen bij jou in Emmen. Of laat je set met DHL versturen: gratis vanaf €150.',
        'links': [('Lasergame huren in Drenthe', url('/lasergame-huren-drenthe/')), ('Alle lasergame-informatie', HUB),
                  ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})
