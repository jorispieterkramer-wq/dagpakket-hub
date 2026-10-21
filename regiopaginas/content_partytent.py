"""
Fase 4a — Partytent-cluster (A hub, B provincie, C stad).

Feiten (bron: productpagina's en /contact/):
- Easy up 3x3 en 3x6 (wit/zwart): "binnen enkele minuten" / "snel op te zetten";
  3x6: stevig aluminium frame; 3x3 zwart: haringen + handleiding inbegrepen,
  "Ophalen of eigen bezorging mogelijk"; zijwanden en verzwaring optioneel.
- Pagodetent 5x5m zand: partnerproduct, "voorstel op maat"; voor entree, stand, bar, buffet.
- Opblaasbare partytent 5x4m: "opvallende en snelle feestopstelling", tuinfeesten, events.
- Tentgewicht-zakken: leeg geleverd, zelf te vullen met zand of grind.
- Partytenten gaan NIET via DHL: eigen bezorging per zone of gratis afhalen in Fochteloo.
- Geen personencapaciteiten: die staan op geen enkele productpagina (gemeld in rapport).
"""
import os as _os
from build import url, TEL
from reviews import BABYSHOWER

U = url('/wp-content/uploads')
IMG = {
    'hero': (U + '/2026/03/Gemini_Generated_Image_ilhhoqilhhoqilhh-1_11zon.webp',
             'Witte easy up partytent met statafels in een tuin'),
    'zwart': (U + '/2026/02/Gemini_Generated_Image_d6sx83d6sx83d6sx_11zon.webp',
              'Zwarte easy up partytent met statafels en feestverlichting op een terras'),
    'wit': (U + '/2026/04/Gemini_Generated_Image_4hdhpp4hdhpp4hdh_11zon.webp',
            'Witte easy up partytent met statafels op een gazon'),
    'detail': (U + '/2026/02/Gemini_Generated_Image_hcx0pshcx0pshcx0_11zon.webp',
               'Detail van het aluminium frame van een zwarte easy up partytent met lampjes'),
    'tuinfeest': (U + '/2026/08/Gemini_Generated_Image_afvuyfafvuyfafvu_11zon.webp',
                  'Tenten met verlichting boven een tuinfeest'),
}

HUB = url('/partytent-huren/')
CONTACT = url('/contact/')
CAT = url('/product-category/tenten-verwarming-huren/')  # 200 op staging en live, geen redirect
P = {
    'wit33': url('/product/easy-up-partytent-huren-wit-3x3m/'),
    'wit36': url('/product/easy-up-partytent-wit-3x6m/'),
    'zwart33': url('/product/partytent-huren-zwart-3x3/'),
    'zwart36': url('/product/easy-up-partytent-3x6-zwart-huren/'),
    'pagode': url('/product/pagodetent-5-x-5m-zand-huren/'),
    'opblaas': url('/product/opblaasbare-partytent-huren/'),
    'gewicht': url('/product/tentgewichten-huren/'),
    'zijwand33': url('/product/easy-up-partytent-zijwanden-wit-3x3m/'),
    'zijwand36': url('/product/easy-up-partytent-zijwanden-wit-3x6m/'),
}
ALTS = {48874: 'Easy up partytent wit 3x3m huren', 49830: 'Easy up partytent wit 3x6m huren',
        47199: 'Easy up partytent zwart 3x3m huren', 49828: 'Easy up partytent zwart 3x6m huren',
        50386: 'Pagodetent 5x5m zand huren', 50150: 'Opblaasbare partytent 5x4m huren'}
HUB_CARDS = {'product_ids': [48874, 49830, 47199, 49828, 50386, 50150], 'prod_cols': 3,
             'cat_url': CAT, 'product_alts': ALTS}
REG_CARDS = {'product_ids': [48874, 49830, 47199, 49828], 'prod_cols': 4,
             'cat_url': CAT, 'product_alts': {k: ALTS[k] for k in (48874, 49830, 47199, 49828)}}

ZONE = 'Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.'
CALC = f'<a href="{CONTACT}">Bereken het met je postcode</a>'
FAQ_INTRO = 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.'
REVIEW = {'h2': 'Wat klanten zeggen', 'data': BABYSHOWER}

TRUST = [
    ('shield', 'Geen borg', 'Je betaalt alleen de huurprijs'),
    ('pin', 'Gratis afhalen in Fochteloo', 'Vanaf 16:00 de dag voor je event'),
    ('truck', 'Bezorging in Noord-Nederland', 'Tarief per zone, check je postcode'),
    ('bolt', 'Easy up in enkele minuten', 'Uitklappen, op hoogte zetten, klaar'),
]
CHECKS = [
    'Easy up-tenten staan binnen enkele minuten',
    'Zijwanden en tentgewichten los bij te huren',
    'Zelf ophalen in Fochteloo is altijd gratis',
    'Geen borg — je betaalt alleen de huurprijs',
]
LEV_EIGEN = lambda gebied: {
    'icon': 'truck', 'h3': 'Wij bezorgen en halen op',
    'p': f'Partytenten bezorgen we zelf in {gebied}, op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
    'link': (CONTACT, 'Bereken je bezorgkosten'),
}
LEV_AFHALEN = {
    'icon': 'pin', 'h3': 'Gratis afhalen in Fochteloo',
    'p': 'Op Verlaat 3 in Fochteloo haal je je tent gratis op, vanaf 16:00 de dag voor je feest. '
         'Terugbrengen kan tot 16:00 de dag erna; die uren tellen niet als extra huurdag.',
}
LEV_RETOUR = {
    'icon': 'return', 'h3': 'Terug na je feest',
    'p': 'Lever de tent compleet en droog in, in de bijgeleverde hoes. Even afvegen is genoeg; schoonmaken doen wij.',
}
B2B_CHECKS = [
    'Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen',
    'Betalen op factuur, met je eigen referentie of PO-nummer',
    'Tenten, meubilair en verwarming op één order',
]

PAGES = []

# ================================================================== A — HUB
PAGES.append({
    **HUB_CARDS, 'template': 'A', 'id': 49773, 'slug': 'partytent-huren', 'naam': 'PARTYTENT HUREN (HUB)',
    'plaats': 'Noord-Nederland',
    'seo_title': 'Partytent huren | Easy up 3x3 & 3x6 | Dagpakketverhuur',
    'meta': 'Partytent huren voor een tuinfeest, bruiloft of bedrijfsevent? Easy up 3x3 of 3x6, pagodetent of opblaasbaar. '
            'Geen borg, gratis afhalen in Fochteloo.',
    'hero': {
        'img': IMG['hero'][0], 'alt': IMG['hero'][1], 'pos': '50% 55%',
        'eyebrow': 'Partytent · Easy up 3x3 & 3x6',
        'h1': 'Partytent huren voor<br>je feest in de buitenlucht',
        'sub': 'Easy up-tenten die binnen enkele minuten staan, in wit of zwart. '
               'Gratis afhalen in Fochteloo, of wij bezorgen in Noord-Nederland.',
        'cta': 'Bekijk partytenten',
    },
    'trust': TRUST,
    'products': {
        'h2': 'Kies je partytent', 'cat_link': CAT, 'cat_label': 'Alle tenten en verwarming', 'wide': True,
        'lead': 'Easy up in 3x3 of 3x6 meter, in wit of zwart, plus een pagodetent en een opblaasbare tent.',
        'checks': CHECKS, 'info_h3': 'Goed om te weten',
        'info_link': (P['gewicht'], 'Tentgewichten bijhuren'),
    },
    'keuze': {
        'h2': 'Welk formaat past bij jouw feest?',
        'lead': 'We noemen bewust geen aantallen personen: dat hangt af van tafels, stoelen en of je staat of zit. '
                'Twijfel je? Bel ons, dan denken we mee.',
        'cols': 'dpv-g4',
        'items': [
            {'tag': 'Easy up 3x3 m', 'h3': 'Een overkapping voor de bar of het buffet',
             'p': 'Snel op te zetten en ideaal als overkapping bij een borrel, verjaardag of buitenactiviteit. '
                  'Zijwanden en tentgewichten huur je los bij.',
             'link': (P['wit33'], 'Bekijk de 3x3 wit')},
            {'tag': 'Easy up 3x6 m', 'h3': 'Meer ruimte voor gasten of catering',
             'p': 'Dezelfde snelle opbouw met een stevig aluminium frame, maar dubbel zo lang. '
                  'Handig voor een tafelopstelling, catering of een bar.',
             'link': (P['wit36'], 'Bekijk de 3x6 wit')},
            {'tag': 'Pagodetent 5x5 m', 'h3': 'Voor een entree, stand of buffet',
             'p': 'Een nette, compacte tent voor op locatie. Dit product bieden we aan met een partner: '
                  'je ontvangt een voorstel op maat.',
             'link': (P['pagode'], 'Bekijk de pagodetent')},
            {'tag': 'Opblaasbaar 5x4 m', 'h3': 'Opvallend en snel opgezet',
             'p': 'Een opblaasbare partytent voor een opvallende feestopstelling, bij een tuinfeest of buitenevent.',
             'link': (P['opblaas'], 'Bekijk de opblaasbare tent')},
        ],
    },
    'gelegenheden': {
        'h2': 'Voor elk feest buiten',
        'items': [
            {'icon': 'sun', 'h3': 'Tuinfeest of verjaardag',
             'p': 'Droog en in de schaduw zitten, wat het weer ook doet. Een 3x3 is vaak al genoeg voor de bar.'},
            {'icon': 'gift', 'h3': 'Bruiloft of receptie',
             'p': 'Een witte easy up of de pagodetent geeft een nette uitstraling bij de ontvangst.'},
            {'icon': 'briefcase', 'h3': 'Bedrijfsfeest, markt of stand',
             'p': 'Zwarte easy ups voor een strakke stand, DJ-opstelling of bar op locatie.',
             'link': (url('/zakelijk/'), 'Zakelijk huren')},
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Een overkapping voor de taart en de limonade, terwijl de kinderen buiten spelen.',
             'link': (url('/kinderfeestje/'), 'Kinderfeestje regelen')},
        ],
    },
    'stappen': {
        'h2': 'Zo werkt huren',
        'items': [
            ('Kies je tent', 'Kies formaat en kleur, en huur zijwanden of tentgewichten erbij als je die wilt.'),
            ('Kies je datum', 'Bij het afrekenen kies je je eventdatum. Je betaalt de dagprijs voor die dag.'),
            ('Bezorgen of afhalen', 'Wij bezorgen in Noord-Nederland, of je haalt de tent gratis op in Fochteloo.'),
            ('Retour', 'Compleet en droog terug tot 16:00 de dag na je feest, of klaarzetten om op te halen.'),
        ],
    },
    'regio': {
        'h2': 'Partytent huren in Noord-Nederland',
        'lead': 'In Friesland, Groningen en Drenthe bezorgen we zelf. Kies je provincie voor bezorging, afhalen en vragen uit de buurt.',
        'items': [
            ('Friesland', 'Partytent huren in Friesland', url('/partytent-huren-friesland/')),
            ('Drenthe', 'Partytent huren in Drenthe', url('/partytent-huren-drenthe/')),
            ('Groningen', 'Partytent huren in Groningen', url('/partytent-huren-groningen/')),
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk',
        'h2': 'Voor bedrijven, scholen en verenigingen',
        'p': 'Een open dag, sportdag of personeelsfeest? Combineer tenten met meubilair en verwarming en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS,
        'img': IMG['zwart'][0], 'alt': IMG['zwart'][1],
    },
    'review': REVIEW,
    'faq': {
        'h2': 'Veelgestelde vragen',
        'intro': FAQ_INTRO,
        'items': [
            ('Kan ik een partytent zelf opzetten?',
             'Ja. Een easy up-tent klap je uit, zet je op de juiste hoogte en staat binnen enkele minuten. '
             'Bij de zwarte 3x3 zitten haringen en een handleiding.'),
            ('Wat kost bezorgen?',
             f'Partytenten bezorgen we zelf in Noord-Nederland. {ZONE.split(". ")[0]}. {CALC}. Zelf afhalen in Fochteloo is altijd gratis.'),
            ('Kan ik zijwanden of gewichten bijhuren?',
             f'Ja. Er zijn zijwanden voor de 3x3 en de 3x6, en <a href="{P["gewicht"]}">tentgewicht-zakken</a> die je zelf vult met zand of grind.'),
            ('Kan de tent blijven staan bij harde wind?',
             'Gebruik de tent niet bij extreem slecht weer of harde wind. Met tentgewichten staat hij stabieler.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg.'),
            ('Kan ik annuleren of mijn datum wijzigen?',
             'Kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, inclusief bezorgkosten.'),
        ],
    },
    'final': {
        'img': IMG['wit'][0], 'alt': IMG['wit'][1], 'cta': 'Bekijk partytenten',
        'h2': 'Klaar voor een feest in de buitenlucht?',
        'p': 'Kies je tent en je datum. Geen borg, en zelf afhalen in Fochteloo is gratis.',
        'links': [('Easy up 3x3 wit', P['wit33']), ('Easy up 3x6 wit', P['wit36']), ('Tentgewichten', P['gewicht'])],
    },
})


def provincie(pid, slug, prov, hero, intro_p, toepassingen, steden, faq, final_img, meta, b2b_img, lev_lead):
    return {
        **REG_CARDS, 'template': 'B', 'id': pid, 'slug': slug, 'naam': f'PARTYTENT HUREN {prov.upper()} (PROVINCIE)',
        'plaats': prov,
        'seo_title': f'Partytent huren in {prov} | Dagpakketverhuur',
        'meta': meta,
        'hero': {**hero, 'eyebrow': f'Partytent · {prov}', 'h1': f'Partytent huren in {prov}', 'cta': 'Bekijk partytenten'},
        'trust': TRUST,
        'intro': {'kicker': f'Partytent in {prov}', 'h2': intro_p[0], 'p': intro_p[1:]},
        'products': {'h2': 'Easy up partytent 3x3 of 3x6', 'wide': True, 'checks': CHECKS, 'info_h3': 'Goed om te weten',
                     'lead': 'In wit of zwart. Liever een pagodetent of opblaasbare tent? Die vind je op de overzichtspagina.',
                     'info_link': (HUB, 'Alle partytenten en de keuzehulp')},
        'toepassingen': toepassingen,
        'steden': steden,
        'levering': {'h2': 'Bezorgen, afhalen en terugbrengen', 'lead': lev_lead,
                     'items': [LEV_EIGEN(prov), LEV_AFHALEN, LEV_RETOUR]},
        'b2b': {'kicker': f'Zakelijk in {prov}', 'h2': 'Bedrijven, scholen en verenigingen',
                'p': f'Een evenement, open dag of personeelsfeest in {prov}? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
                'checks': B2B_CHECKS[:2], 'img': b2b_img[0], 'alt': b2b_img[1]},
        'review': REVIEW,
        'faq': {'h2': f'Vragen over een partytent in {prov}', 'intro': FAQ_INTRO, 'items': faq},
        'final': {'img': final_img[0], 'alt': final_img[1], 'cta': 'Bekijk partytenten',
                  'h2': f'Partytent in {prov} regelen?',
                  'p': 'Kies je tent en je datum. Geen borg, en zelf afhalen in Fochteloo is gratis.',
                  'links': [('Alle partytenten', HUB), ('Easy up 3x3 wit', P['wit33']), ('Easy up 3x6 zwart', P['zwart36'])]},
    }


# ================================================================== B — FRIESLAND
PAGES.append(provincie(
    49725, 'partytent-huren-friesland', 'Friesland',
    {'img': IMG['wit'][0], 'alt': IMG['wit'][1], 'pos': '50% 45%',
     'sub': 'Haal je partytent gratis op in Fochteloo, of laat hem bezorgen in Leeuwarden, Heerenveen en de rest van Friesland.'},
    ['Afhalen in Fochteloo of thuisbezorgd',
     'Ons magazijn staat in Fochteloo, in het zuidoosten van Friesland. Daar haal je een easy up-tent gratis op, vanaf 16:00 '
     'de dag voor je feest.',
     f'Liever thuisbezorgd? In heel Friesland brengen we tenten zelf, op het tijdslot dat je bij het afrekenen kiest. {ZONE}'],
    {'h2': 'Populair in Friesland', 'items': [
        {'icon': 'sun', 'h3': 'Tuinfeest', 'p': 'Een droge plek voor de bar of het buffet, wat het Friese weer ook doet.'},
        {'icon': 'gift', 'h3': 'Bruiloft of jubileum', 'p': 'Witte easy ups voor een nette ontvangst van je gasten.'},
        {'icon': 'users', 'h3': 'Dorpsfeest of vereniging', 'p': 'Meerdere 3x6-tenten naast elkaar voor een markt of feestterrein.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een overkapping voor taart en limonade in de tuin.',
         'link': (url('/kinderfeestje-friesland/'), 'Kinderfeestje in Friesland')}]},
    {'h2': 'Partytent huren in Friese steden', 'lead': 'Voor deze plaatsen staat bezorging en een eigen vragenlijst op een aparte pagina.',
     'items': [('Leeuwarden', 'Partytent huren in Leeuwarden', url('/partytent-huren-leeuwarden/')),
               ('Heerenveen', 'Partytent huren in Heerenveen', url('/partytent-huren-heerenveen/'))]},
    [('Waar haal ik de partytent op?',
      'Op de parkeerplaats aan Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor je feest. We laten vooraf weten wanneer alles klaarligt.'),
     ('Bezorgen jullie in heel Friesland?', f'Ja, Friesland valt binnen ons eigen bezorggebied. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Welk formaat kies ik?',
      'Een 3x3 is een handige overkapping voor bar of buffet; een 3x6 geeft ruimte voor een tafelopstelling of catering.'),
     ('Feest op zondag?', 'Dan regelen we ophalen en terugbrengen op zaterdag of maandag, zonder extra huurdag.')],
    IMG['zwart'],
    'Partytent huren in Friesland? Easy up 3x3 of 3x6 in wit of zwart. Gratis afhalen in Fochteloo of wij bezorgen. Geen borg, snel opgezet.',
    IMG['detail'],
    'Je kiest bij het afrekenen. Op zondag zijn we gesloten; ophalen en terugbrengen gaan dan op zaterdag of maandag.'))

# ================================================================== B — GRONINGEN
PAGES.append(provincie(
    49717, 'partytent-huren-groningen', 'Groningen',
    {'img': IMG['zwart'][0], 'alt': IMG['zwart'][1], 'pos': '50% 50%',
     'sub': 'Een easy up-tent voor je feest of evenement in de provincie Groningen. Wij bezorgen en halen weer op.'},
    ['Bezorgd in de provincie Groningen',
     'De provincie Groningen hoort bij ons eigen bezorggebied. We brengen je partytent op het tijdslot dat je bij het afrekenen '
     f'kiest en halen hem na je feest weer op. {ZONE}',
     'Zelf ophalen kan ook, gratis in Fochteloo. Een easy up-tent staat binnen enkele minuten, en zijwanden of tentgewichten '
     'huur je erbij als je die nodig hebt.'],
    {'h2': 'Populair in Groningen', 'items': [
        {'icon': 'briefcase', 'h3': 'Bedrijfsevent of stand', 'p': 'Zwarte easy ups voor een strakke bar, stand of DJ-plek.'},
        {'icon': 'sun', 'h3': 'Barbecue of tuinfeest', 'p': 'Een 3x3 boven de grill of het buffet houdt alles droog.'},
        {'icon': 'school', 'h3': 'Schoolfeest', 'p': 'Tenten op het schoolplein voor een kraam of het buffet. Scholen betalen op factuur.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Schaduw en een droge plek voor de traktatie.',
         'link': (url('/kinderfeestje-groningen/'), 'Kinderfeestje in Groningen')}]},
    None,
    [('Bezorgen jullie ook in de stad Groningen?', f'Ja, de hele provincie Groningen valt binnen ons bezorggebied. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Is de tent geschikt voor op steen?',
      'De zwarte easy up 3x3 is geschikt voor gras, zand en steen. Op steen gebruik je tentgewichten in plaats van haringen.'),
     ('Moet ik vooraf betalen?',
      'Ja, een bestelling moet betaald zijn vóór de huurdatum. Zakelijke klanten kunnen op factuur betalen.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['wit'],
    'Partytent huren in Groningen? Easy up 3x3 of 3x6, wit of zwart, voor tuinfeest of bedrijfsevent. Wij bezorgen en halen op. Geen borg.',
    IMG['hero'],
    'Kies bezorgen of zelf ophalen bij het afrekenen. Op zondag zijn we gesloten.'))

# ================================================================== B — DRENTHE
PAGES.append(provincie(
    49731, 'partytent-huren-drenthe', 'Drenthe',
    {'img': IMG['tuinfeest'][0], 'alt': IMG['tuinfeest'][1], 'pos': '50% 50%',
     'sub': 'Een droge plek voor je gasten, van Assen tot Emmen. Wij bezorgen in Drenthe, of je haalt gratis af in Fochteloo.'},
    ['Partytenten in heel Drenthe',
     'Drenthe valt binnen ons eigen bezorggebied. We brengen je tent op het gekozen tijdslot en halen hem na afloop weer op. '
     f'{ZONE}',
     'Wil je zelf rijden? Ophalen in Fochteloo is gratis, vanaf 16:00 de dag voor je feest. Kies een 3x3 als overkapping of '
     'een 3x6 als je meer ruimte nodig hebt.'],
    {'h2': 'Populair in Drenthe', 'items': [
        {'icon': 'sun', 'h3': 'Feest in de tuin', 'p': 'Een witte easy up met statafels eronder maakt elke tuin feestklaar.'},
        {'icon': 'users', 'h3': 'Buurt- of dorpsfeest', 'p': 'Een paar tenten naast elkaar voor de bar, het buffet en de muziek.'},
        {'icon': 'briefcase', 'h3': 'Open dag of bedrijfsfeest', 'p': 'Een strakke zwarte tent voor de ontvangst van gasten.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Beschutting voor de traktatie, zon of regen.',
         'link': (url('/kinderfeestje-drenthe/'), 'Kinderfeestje in Drenthe')}]},
    {'h2': 'Partytent huren in Drentse steden', 'lead': 'Voor deze plaatsen hebben we een eigen pagina met bezorging en vragen uit de buurt.',
     'items': [('Assen', 'Partytent huren in Assen', url('/partytent-huren-assen/')),
               ('Emmen', 'Partytent huren in Emmen', url('/partytent-huren-emmen/'))]},
    [('Bezorgen jullie in heel Drenthe?', f'Ja, Drenthe valt binnen ons eigen bezorggebied. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik zijwanden bijhuren?',
      f'Ja, voor zowel de <a href="{P["zijwand33"]}">3x3</a> als de <a href="{P["zijwand36"]}">3x6</a>. Ze beschermen tegen wind en regen.'),
     ('Hoe zet ik de tent op?', 'Uitklappen, op de juiste hoogte zetten en stevig plaatsen. Dat is binnen enkele minuten gebeurd.'),
     ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag.')],
    IMG['detail'],
    'Partytent huren in Drenthe? Wij bezorgen in Assen, Emmen en omgeving of je haalt gratis af in Fochteloo. Easy up 3x3 of 3x6, geen borg.',
    IMG['wit'],
    'Je kiest bezorgen of ophalen bij het afrekenen. Op zondag zijn we gesloten; we regelen het dan op zaterdag of maandag.'))


def stad(pid, slug, stad_n, prov, prov_slug, hero, intro, stappen, gelegenheden, plaatsen, lev_lead, faq, final_img, meta, b2b_p, b2b_img):
    return {
        **REG_CARDS, 'template': 'C', 'id': pid, 'slug': slug, 'naam': f'PARTYTENT HUREN {stad_n.upper()} (STAD)',
        'plaats': stad_n,
        'seo_title': f'Partytent huren in {stad_n} | Dagpakketverhuur',
        'meta': meta,
        'hero': {**hero, 'eyebrow': f'Partytent · {stad_n}', 'h1': f'Partytent huren in {stad_n}', 'cta': 'Bekijk partytenten'},
        'trust': TRUST,
        'intro': intro,
        'products': {'h2': 'Easy up partytent 3x3 of 3x6', 'wide': True, 'checks': CHECKS, 'info_h3': 'Goed om te weten',
                     'lead': 'Wit of zwart, snel opgezet. Zijwanden en tentgewichten huur je los bij.',
                     'info_link': (HUB, 'Alle partytenten en de keuzehulp')},
        'stappen': {'h2': f'Zo werkt huren in {stad_n}', 'items': stappen},
        'gelegenheden': {'h2': f'Waarvoor huur je een partytent in {stad_n}?', 'items': gelegenheden},
        'b2b': {'kicker': f'Zakelijk in {stad_n}', 'h2': f'Ook voor bedrijven, scholen en verenigingen in {stad_n}',
                'p': b2b_p, 'checks': B2B_CHECKS[:2], 'img': b2b_img[0], 'alt': b2b_img[1]},
        'levering': {'h2': f'Levering in {stad_n} en omgeving', 'lead': lev_lead, 'plaatsen': plaatsen,
                     'items': [LEV_EIGEN(f'{stad_n} en omgeving'), LEV_AFHALEN, LEV_RETOUR]},
        'review': REVIEW,
        'faq': {'h2': f'Vragen over een partytent in {stad_n}', 'intro': FAQ_INTRO, 'items': faq},
        'final': {'img': final_img[0], 'alt': final_img[1], 'cta': 'Bekijk partytenten',
                  'h2': f'Partytent in {stad_n} regelen?',
                  'p': f'Kies je tent en je datum, wij bezorgen in {stad_n}. Of haal hem gratis op in Fochteloo.',
                  'links': [(f'Partytent huren in {prov}', url(f'/partytent-huren-{prov_slug}/')), ('Alle partytenten', HUB),
                            ('Easy up 3x3 wit', P['wit33']), ('Easy up 3x6 wit', P['wit36'])]},
    }


# ================================================================== C — LEEUWARDEN
PAGES.append(stad(
    49924, 'partytent-huren-leeuwarden', 'Leeuwarden', 'Friesland', 'friesland',
    {'img': IMG['hero'][0], 'alt': IMG['hero'][1], 'pos': '50% 55%',
     'sub': 'Voor een tuinfeest, receptie of bedrijfsevent. Wij bezorgen in Leeuwarden en de dorpen eromheen.'},
    {'kicker': 'Partytent in Leeuwarden', 'h2': 'Thuisbezorgd in Leeuwarden',
     'p': [f'In Leeuwarden en omgeving brengen we je partytent op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
           'Een easy up-tent staat binnen enkele minuten. Heb je een terras of een tuin op steen? Huur dan tentgewichten '
           'erbij, die je zelf vult met zand of grind.']},
    [('Kies je tent', 'Een 3x3 of 3x6, in wit of zwart, met of zonder zijwanden.'),
     ('Kies datum en tijdslot', 'Bij het afrekenen kies je je eventdatum en het moment van bezorgen.'),
     ('Wij bezorgen', 'Eén tot twee dagen vooraf bevestigen we het tijdslot.'),
     ('Wij halen op', 'Zet de tent droog en compleet klaar tot 16:00 de dag na je feest.')],
    [{'icon': 'gift', 'h3': 'Receptie of bruiloft', 'p': 'Witte easy ups voor een nette ontvangst in de tuin of op het erf.'},
     {'icon': 'sun', 'h3': 'Tuinfeest of barbecue', 'p': 'Een 3x3 boven de bar of de grill, en je feest gaat door bij elk weer.'},
     {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een droge plek voor taart en limonade.',
      'link': (url('/kinderfeestje-leeuwarden/'), 'Kinderfeestje in Leeuwarden')}],
    ['Leeuwarden', 'Stiens', 'Grou', 'Goutum', 'Wirdum', 'Jirnsum', 'Warga'],
    f'We bezorgen in Leeuwarden en de dorpen eromheen, onder meer in deze plaatsen. {ZONE}',
    [('Bezorgen jullie ook in Stiens of Grou?', f'Ja, we bezorgen in Leeuwarden en de dorpen eromheen. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik de tent op een terras zetten?', 'Ja. Op steen gebruik je tentgewichten; die huur je los bij.'),
     ('Wanneer hoor ik hoe laat jullie komen?', 'Eén tot twee dagen voor je huurdatum nemen we contact op met het tijdslot.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['zwart'],
    'Partytent huren in Leeuwarden, Stiens of Grou? Easy up 3x3 of 3x6, wit of zwart. Wij bezorgen en halen op, geen borg.',
    'Een open dag, personeelsfeest of evenement in Leeuwarden? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
    IMG['detail']))

# ================================================================== C — HEERENVEEN (extra lokale diepgang)
PAGES.append(stad(
    49948, 'partytent-huren-heerenveen', 'Heerenveen', 'Friesland', 'friesland',
    {'img': IMG['wit'][0], 'alt': IMG['wit'][1], 'pos': '50% 50%',
     'sub': 'Een easy up-tent voor je feest in Heerenveen of de dorpen eromheen. Bezorgd, of gratis opgehaald in Fochteloo.'},
    {'kicker': 'Partytent in Heerenveen', 'h2': 'Partytent huren in Heerenveen en omgeving',
     'p': [f'In de gemeente Heerenveen bezorgen we partytenten zelf, op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
           'Liever zelf ophalen? Dat kan altijd gratis op Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor je feest. '
           'Breng de tent tot 16:00 de dag erna terug; die uren rekenen we niet als extra huurdag.',
           'Twijfel je tussen formaten? Een 3x3 is een overkapping voor bar of buffet, een 3x6 geeft ruimte voor een '
           'tafelopstelling of catering. Zijwanden en tentgewichten maken de opstelling compleet.']},
    [('Kies formaat en kleur', 'Easy up 3x3 of 3x6, wit of zwart. Zijwanden en gewichten erbij als je wilt.'),
     ('Bezorgen of ophalen', 'Kies bij het afrekenen je datum, en of we bezorgen of dat je zelf ophaalt in Fochteloo.'),
     ('Opzetten', 'Uitklappen, op hoogte zetten, vastzetten met haringen of gewichten. Binnen enkele minuten klaar.'),
     ('Terug', 'Droog en compleet in de hoes, tot 16:00 de dag na je feest.')],
    [{'icon': 'sun', 'h3': 'Tuinfeest of verjaardag', 'p': 'Een witte easy up met statafels eronder: klaar voor je gasten.'},
     {'icon': 'users', 'h3': 'Buurt- of dorpsfeest', 'p': 'Meerdere 3x6-tenten naast elkaar voor bar, buffet en muziek.'},
     {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een schaduwplek voor de traktatie terwijl de kinderen spelen.',
      'link': (url('/kinderfeestje-heerenveen/'), 'Kinderfeestje in Heerenveen')}],
    ['Heerenveen', 'Akkrum', 'Oudehaske', 'Jubbega', 'Hoornsterzwaag', 'Nieuwehorne', 'Oudeschoot', 'Tjalleberd', 'Mildam'],
    f'We bezorgen in Heerenveen en de dorpen van de gemeente, onder meer in deze plaatsen. {ZONE}',
    [('Bezorgen jullie ook in Akkrum of Jubbega?', f'Ja, we bezorgen in de hele gemeente Heerenveen. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik de tent zelf ophalen in Fochteloo?',
      'Ja, gratis, vanaf 16:00 de dag voor je feest. We laten vooraf weten wanneer alles klaarligt.'),
     ('Welke kleur kies ik?',
      'Wit oogt licht en feestelijk, bijvoorbeeld bij een receptie. Zwart is strak en past bij een bar, stand of DJ-opstelling.'),
     ('Wat als het hard waait?',
      'Gebruik de tent niet bij extreem slecht weer of harde wind. Tentgewichten en zijwanden helpen bij een stabiele opstelling.'),
     ('Feest op zondag?', 'We zijn op zondag gesloten. Ophalen en terugbrengen gaan dan op zaterdag of maandag, zonder extra huurdag.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['tuinfeest'],
    'Partytent huren in Heerenveen, Akkrum of Jubbega? Easy up 3x3 of 3x6, wit of zwart. Wij bezorgen of je haalt gratis af in Fochteloo.',
    'Een evenement, open dag of personeelsfeest in Heerenveen? Combineer tenten met meubilair en vraag een zakelijke prijs aan.',
    IMG['zwart']))

# ================================================================== C — ASSEN
PAGES.append(stad(
    49932, 'partytent-huren-assen', 'Assen', 'Drenthe', 'drenthe',
    {'img': IMG['zwart'][0], 'alt': IMG['zwart'][1], 'pos': '50% 50%',
     'sub': 'Een partytent voor je feest of evenement in Assen. Wij bezorgen in Assen en de omliggende dorpen.'},
    {'kicker': 'Partytent in Assen', 'h2': 'Partytent laten bezorgen in Assen',
     'p': [f'In Assen en omgeving brengen we je partytent op het gekozen tijdslot en halen we hem na je feest weer op. {ZONE}',
           'Kies wit voor een lichte, feestelijke uitstraling of zwart voor een strakke bar of stand. Beide staan binnen enkele minuten.']},
    [('Tent kiezen', 'Bepaal formaat en kleur en of je zijwanden of gewichten nodig hebt.'),
     ('Datum en tijdslot', 'Kies bij het afrekenen je eventdatum en het tijdslot.'),
     ('Bezorging in Assen', 'We komen op het gekozen moment. Liever zelf ophalen? Dat kan gratis in Fochteloo.'),
     ('Ophalen', 'Zet alles droog en compleet klaar tot 16:00 de dag na je feest.')],
    [{'icon': 'users', 'h3': 'Vereniging of clubfeest', 'p': 'Een overkapping voor de bar of kraam. Verenigingen betalen op factuur.'},
     {'icon': 'sun', 'h3': 'Tuinfeest', 'p': 'Een 3x6 voor een tafelopstelling met familie en vrienden.'},
     {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Beschutting voor de traktatie, zon of regen.',
      'link': (url('/kinderfeestje-assen/'), 'Kinderfeestje in Assen')}],
    ['Assen', 'Loon', 'Witten', 'Rhee', 'Rolde', 'Vries'],
    f'We bezorgen in Assen en de dorpen eromheen, onder meer in deze plaatsen. {ZONE}',
    [('Bezorgen jullie ook in Rolde of Vries?', f'Ja, we bezorgen in Assen en de dorpen eromheen. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik meerdere tenten huren?', 'Ja, zet gewoon meerdere tenten in je winkelwagen. Bezorgkosten rekenen we één keer per bestelling.'),
     ('Moet ik de tent schoonmaken?', 'Nee. Lever hem droog en compleet in; even afvegen is genoeg, schoonmaken doen wij.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['hero'],
    'Partytent huren in Assen, Loon of Rolde? Easy up 3x3 of 3x6, wit of zwart. Wij bezorgen en halen op, of gratis afhalen in Fochteloo.',
    'Een open dag, clubfeest of bedrijfsevent in Assen? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
    IMG['wit']))

# ================================================================== C — EMMEN (extra lokale diepgang)
PAGES.append(stad(
    49940, 'partytent-huren-emmen', 'Emmen', 'Drenthe', 'drenthe',
    {'img': IMG['tuinfeest'][0], 'alt': IMG['tuinfeest'][1], 'pos': '50% 45%',
     'sub': 'Een easy up-tent voor je feest in Emmen, Klazienaveen of Nieuw-Amsterdam. Wij bezorgen en halen weer op.'},
    {'kicker': 'Partytent in Emmen', 'h2': 'Partytent huren in de hele gemeente Emmen',
     'p': [f'Van Emmen-centrum tot de dorpen in de gemeente: we bezorgen je partytent op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
           'Een easy up 3x3 is een handige overkapping voor bar of buffet. Heb je meer ruimte nodig voor een tafelopstelling of '
           'catering, kies dan de 3x6. Beide staan binnen enkele minuten.',
           'Zelf ophalen kan ook: gratis in Fochteloo, vanaf 16:00 de dag voor je feest. Zijwanden en tentgewichten huur je los bij.']},
    [('Kies je tent', 'Easy up 3x3 of 3x6, wit of zwart. Voeg zijwanden of gewichten toe als je die nodig hebt.'),
     ('Kies datum en tijdslot', 'Bij het afrekenen kies je je eventdatum en wanneer we bezorgen.'),
     ('Wij bezorgen in Emmen', 'Eén tot twee dagen vooraf bevestigen we het tijdslot.'),
     ('Wij halen weer op', 'Droog en compleet klaarzetten tot 16:00 de dag na je feest.')],
    [{'icon': 'sun', 'h3': 'Tuinfeest of barbecue', 'p': 'Een droge plek voor de grill en het buffet, wat het weer ook doet.'},
     {'icon': 'gift', 'h3': 'Receptie of jubileum', 'p': 'Witte easy ups voor een nette ontvangst van je gasten.'},
     {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Schaduw en een droge plek voor de traktatie.',
      'link': (url('/kinderfeestje-emmen/'), 'Kinderfeestje in Emmen')}],
    ['Emmen', 'Klazienaveen', 'Nieuw-Amsterdam', 'Erica', 'Schoonebeek', 'Emmer-Compascuum', 'Nieuw-Weerdinge', 'Zwartemeer', 'Weiteveen'],
    f'We bezorgen in de hele gemeente Emmen, onder meer in deze plaatsen. {ZONE}',
    [('Bezorgen jullie ook in Klazienaveen of Schoonebeek?', f'Ja, we bezorgen in de hele gemeente Emmen. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Welk formaat kies ik voor een tuinfeest?',
      'Een 3x3 als overkapping voor bar of buffet, een 3x6 als je gasten ook onder de tent wilt laten zitten.'),
     ('Kan ik de tent op een oprit of terras zetten?',
      'Ja. De zwarte 3x3 is geschikt voor gras, zand en steen. Op steen gebruik je tentgewichten.'),
     ('Wanneer hoor ik hoe laat jullie komen?', 'Eén tot twee dagen voor je huurdatum nemen we contact op met het tijdslot.'),
     ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, inclusief bezorgkosten.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['wit'],
    'Partytent huren in Emmen, Klazienaveen of Nieuw-Amsterdam? Easy up 3x3 of 3x6, wit of zwart. Wij bezorgen en halen op, geen borg.',
    'Een evenement, open dag of personeelsfeest in Emmen? Combineer tenten met meubilair en vraag een zakelijke prijs aan.',
    IMG['detail']))


# ------------------------------------------------------------------ variatie per pagina
# Gedeelde blokken (bezorgen/afhalen/retour, productintro, checklist, slot) krijgen per pagina
# een eigen formulering, zodat zusterpagina's ≤0,35 woordreeks-overlap houden. Feiten blijven gelijk.
VAR = {
    'partytent-huren-friesland': dict(
        lead='Twee formaten, twee kleuren. Kijk op de overzichtspagina voor de pagodetent en de opblaasbare tent.',
        eigen='Door heel Friesland rijden we zelf met tenten, op het tijdslot dat jij kiest bij het afrekenen. ' + ZONE,
        afhalen='Fochteloo ligt in Friesland zelf: ophalen op Verlaat 3 is gratis, vanaf 16:00 de dag voor je feest. Terugbrengen kan tot 16:00 de dag erna.',
        retour='Droog en compleet terug in de hoes. Afvegen volstaat, wij maken de tent schoon.',
        final='Kies formaat en kleur. Ophalen in Fochteloo kost niets, en borg vragen we niet.',
        checks=['Staat binnen enkele minuten', 'Wit of zwart, 3x3 of 3x6', 'Gratis ophalen in Fochteloo', 'Geen borg']),
    'partytent-huren-groningen': dict(
        lead='Een 3x3 als overkapping of een 3x6 voor meer ruimte, telkens in wit of zwart.',
        eigen='In de provincie Groningen bezorgen we tenten zelf en halen we ze ook weer op. ' + ZONE,
        afhalen='Zelf rijden mag altijd: ophalen in Fochteloo is gratis, vanaf 16:00 de dag voor het feest, en terugbrengen tot 16:00 de dag erna.',
        retour='Na afloop gaat de tent droog en compleet terug in de hoes. Schoonmaken nemen wij voor onze rekening.',
        final='Bestel je tent online. Wij bezorgen in Groningen; borg is niet nodig.',
        checks=['Easy up: uitklappen en klaar', 'Haringen en handleiding bij de zwarte 3x3', 'Zijwanden en gewichten los te huren', 'Geen borg']),
    'partytent-huren-drenthe': dict(
        lead='Easy up in wit of zwart. Voor een pagodetent of opblaasbare tent ga je naar de overzichtspagina.',
        eigen='In heel Drenthe brengen en halen we partytenten zelf, op het tijdslot dat je bij het afrekenen kiest. ' + ZONE,
        afhalen='Gratis afhalen kan in Fochteloo, vanaf 16:00 de dag voor je feest. Breng de tent terug tot 16:00 de dag erna.',
        retour='Lever de tent droog en compleet in. Even afvegen is genoeg.',
        final='Kies je tent en je datum. Wij bezorgen in Drenthe, of je haalt hem gratis op in Fochteloo.',
        checks=['Binnen enkele minuten opgezet', 'Zijwanden voor 3x3 en 3x6', 'Tentgewichten zelf te vullen met zand of grind', 'Geen borg']),
    'partytent-huren-leeuwarden': dict(
        lead='Snel opgezet en in wit of zwart verkrijgbaar. Zijwanden en gewichten zijn los te huren.',
        eigen='In Leeuwarden en de dorpen eromheen bezorgen we tenten zelf. ' + ZONE,
        afhalen='Rij je liever zelf? In Fochteloo haal je de tent gratis op, vanaf 16:00 de dag voor je feest.',
        retour='Klaarzetten voor ophalen of terugbrengen: droog, compleet en in de hoes.',
        final='Kies formaat en kleur, wij komen in Leeuwarden langs.',
        checks=['Wit of zwart', 'In enkele minuten opgezet', 'Op steen met tentgewichten', 'Geen borg'],
        extra_intro='Bij een receptie kiezen veel mensen wit; voor een bar of DJ-plek past zwart vaak beter. '
                    'Beide kleuren zijn er in 3x3 en 3x6.'),
    'partytent-huren-heerenveen': dict(
        lead='Easy up 3x3 of 3x6 in wit of zwart, met zijwanden en tentgewichten als losse extra’s.',
        eigen='In de hele gemeente Heerenveen bezorgen we zelf en halen we na je feest weer op. ' + ZONE,
        afhalen='Ophalen op Verlaat 3 in Fochteloo is gratis, vanaf 16:00 de dag ervoor; inleveren tot 16:00 de dag erna.',
        retour='De tent gaat droog en compleet terug in de hoes. Wij doen de schoonmaak.',
        final='Kies je tent, wij bezorgen in Heerenveen. Of haal hem gratis op in Fochteloo.',
        checks=['Klaar binnen enkele minuten', 'Keuze uit 3x3 en 3x6', 'Zijwanden en gewichten erbij', 'Geen borg']),
    'partytent-huren-assen': dict(
        lead='Kies een 3x3 of 3x6, in wit of zwart. De opbouw is in enkele minuten gedaan.',
        eigen='In Assen en omgeving bezorgen we zelf, op het tijdslot van jouw keuze. ' + ZONE,
        afhalen='Zelf ophalen in Fochteloo is gratis, vanaf 16:00 de dag voor je feest; terug tot 16:00 de dag erna.',
        retour='Droog en compleet inleveren of klaarzetten. Schoonmaken hoeft niet.',
        final='Kies je tent en je datum, wij bezorgen in Assen.',
        checks=['Easy up-systeem', 'Wit of zwart', 'Meerdere tenten op één bestelling', 'Geen borg']),
    'partytent-huren-emmen': dict(
        lead='Wit of zwart, 3x3 of 3x6, en binnen enkele minuten opgezet.',
        eigen='Overal in de gemeente Emmen brengen we tenten zelf en halen we ze ook weer op. ' + ZONE,
        afhalen='Gratis ophalen in Fochteloo kan vanaf 16:00 de dag voor je feest; terugbrengen tot 16:00 de dag erna.',
        retour='Droog en compleet terug in de hoes. Even afvegen, de rest doen wij.',
        final='Kies je tent en je datum, wij bezorgen in de hele gemeente Emmen.',
        checks=['Staat in enkele minuten', 'Geschikt voor gras, zand en steen (zwart 3x3)', 'Zijwanden en gewichten los te huren', 'Geen borg']),
}
for _p in PAGES:
    v = VAR.get(_p['slug'])
    if not v:
        continue
    _p['products']['lead'] = v['lead']
    _p['products']['checks'] = v['checks']
    _p['levering']['items'][0] = {**_p['levering']['items'][0], 'p': v['eigen']}
    _p['levering']['items'][1] = {**_p['levering']['items'][1], 'p': v['afhalen']}
    _p['levering']['items'][2] = {**_p['levering']['items'][2], 'p': v['retour']}
    _p['final']['p'] = v['final']
    if v.get('extra_intro'):
        _p['intro']['p'] = _p['intro']['p'] + [v['extra_intro']]
