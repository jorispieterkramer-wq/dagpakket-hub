"""
Fase 3 — overige lasergame-regiopagina's (zelfde templates als de pilot:
B = Drenthe, C = Emmen). Gedeelde blokken en feiten komen uit content_lasergame.

Feiten: alleen wat op de site staat (/contact/, productpagina's, /zakelijk/,
homepage-review). Omliggende plaatsen zijn bestaande plaatsen; er worden geen
reistijden, afstanden, klanten of lokale feiten genoemd.
"""
from build import url, TEL
from content_lasergame import (IMG, U, COMPACT, XL, HUB, CAT, CONTACT, TRUST, PRODUCT_CHECKS,
                               LEV_EIGEN, LEV_DHL, LEV_AFHALEN, B2B_CHECKS)

IMG = dict(IMG)
IMG['binnen'] = (U + '/2025/09/F4E27435-5E6B-4CE1-A3FA-FB4B5AE65C54.jpeg',
                 "Collega's spelen binnen lasergame tijdens een bedrijfsuitje")
IMG['heg'] = (U + '/2025/09/IMG_395C64FA2DE4-1.jpg',
              'Kind met lasergun sluipt langs een heg in de tuin')

CARDS = {'product_ids': [47238, 47235], 'cat_url': CAT,
         'product_alts': {47238: 'Lasergame Compact huren', 47235: 'Lasergame XL huren'}}
PROD_CHECKS = {'checks': PRODUCT_CHECKS, 'info_h3': 'Bij beide sets'}
FAQ_INTRO = 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.'
ZONE = 'Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.'
CALC = f'<a href="{CONTACT}">Bereken het met je postcode</a>'

PAGES = []

# ================================================================== B — FRIESLAND
PAGES.append({
    **CARDS, 'template': 'B', 'id': 49689, 'slug': 'lasergame-huren-friesland',
    'naam': 'LASERGAME HUREN FRIESLAND (PROVINCIE)', 'plaats': 'Friesland',
    'seo_title': 'Lasergame huren in Friesland | Dagpakketverhuur',
    'meta': 'Lasergame huren in Friesland? Gratis afhalen in Fochteloo of wij bezorgen in Leeuwarden, Drachten en omgeving. '
            'Geen borg, Compact of XL, vanaf 6 jaar.',
    'hero': {
        'img': IMG['bos'][0], 'alt': IMG['bos'][1], 'pos': '50% 55%',
        'eyebrow': 'Lasergame · Friesland',
        'h1': 'Lasergame huren in Friesland',
        'sub': 'Ons magazijn staat in Fochteloo: daar haal je je set gratis op. '
               'Thuis laten bezorgen of met DHL laten versturen kan ook.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Friesland',
        'h2': 'Vanuit Fochteloo, het hele Friese land door',
        'p': [
            'Fochteloo ligt in het zuidoosten van Friesland, en daar staan onze lasergames klaar. Ophalen op Verlaat 3 '
            'is altijd gratis. Dat kan vanaf 16:00 de dag voor je feest; terugbrengen doe je tot 16:00 de dag erna.',
            'Woon je verder weg in de provincie? Dan rijden wij langs op het tijdslot dat je bij het afrekenen kiest. '
            f'{ZONE} Liever per post: met DHL is verzenden gratis vanaf €150.',
        ],
    },
    'products': {**PROD_CHECKS, 'h2': 'Lasergame Compact of XL',
                 'lead': 'Allebei dezelfde bediening. Met Compact zijn rondes kort en snel, XL houdt elke speler langer in het spel.',
                 'info_link': (HUB, 'Welke set past bij jouw groep?')},
    'toepassingen': {
        'h2': 'Waar Friezen een lasergame voor huren',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Vanaf 6 jaar doet iedereen mee. Een achtertuin met een paar bosjes is al een prima speelveld.',
             'link': (url('/kinderfeestje-friesland/'), 'Kinderfeestje in Friesland')},
            {'icon': 'users', 'h3': 'Verjaardag met vrienden',
             'p': 'Teams kiezen, guns aan en strijden om de winst. Er hoeft niemand te begeleiden.'},
            {'icon': 'briefcase', 'h3': 'Bedrijfsuitje op eigen terrein',
             'p': 'Op het grasveld naast kantoor of in een loods: jullie bepalen de locatie.'},
            {'icon': 'school', 'h3': 'Clubdag of schoolactiviteit',
             'p': 'Verenigingen en scholen betalen op factuur en krijgen vooraf een vaste prijs.'},
        ],
    },
    'steden': {
        'h2': 'Lasergame huren in Friese steden',
        'lead': 'Voor deze plaatsen staat bezorging en een eigen vragenlijst op een aparte pagina.',
        'items': [
            ('Leeuwarden', 'Lasergame huren in Leeuwarden', url('/lasergame-huren-leeuwarden/')),
            ('Drachten', 'Lasergame huren in Drachten', url('/lasergame-huren-drachten/')),
        ],
    },
    'levering': {
        'h2': 'Ophalen, laten brengen of versturen',
        'lead': 'Je kiest de manier bij het afrekenen. Zondag zijn we dicht: ophalen of terugbrengen schuift dan naar zaterdag of maandag.',
        'items': [LEV_AFHALEN, LEV_EIGEN('Friesland'), LEV_DHL],
    },
    'b2b': {
        'kicker': 'Zakelijk in Friesland',
        'h2': 'Voor teams, scholen en clubs',
        'p': 'Organiseer je een uitje voor collega’s of een sportmiddag voor leerlingen? Laat weten wat je zoekt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS[:2],
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Friesland',
        'intro': FAQ_INTRO,
        'items': [
            ('Waar haal ik de lasergame op?',
             'Op de parkeerplaats aan Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor je event. Ophalen is altijd gratis '
             'en we laten vooraf weten wanneer alles klaarligt.'),
            ('Komen jullie ook bezorgen in Friesland?',
             f'Ja, Friesland hoort bij ons eigen bezorggebied. {ZONE.split(". ")[0]}. {CALC}.'),
            ('Valt mijn feest op zondag?',
             'Dan regelen we ophalen en terugbrengen op zaterdag of maandag. Die extra dag rekenen we niet als huurdag.'),
            ('Wat is het verschil tussen Compact en XL?',
             'Compact heeft drie balken met levens, XL vier. Compact is kleiner en voordeliger; XL geeft per ronde een langer spel.'),
            ('Vanaf welke leeftijd kan je meedoen?',
             'Vanaf 6 jaar. Er is geen ervaring nodig, ook niet voor volwassenen.'),
        ],
    },
    'final': {
        'img': IMG['tuin'][0], 'alt': IMG['tuin'][1],
        'h2': 'Lasergame in Friesland regelen?',
        'p': 'Kies je set en je datum. Gratis ophalen in Fochteloo, of DHL-verzending gratis vanaf €150.',
        'links': [('Alle lasergame-informatie', HUB), ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== B — GRONINGEN
PAGES.append({
    **CARDS, 'template': 'B', 'id': 49664, 'slug': 'lasergame-huren-groningen',
    'naam': 'LASERGAME HUREN GRONINGEN (PROVINCIE)', 'plaats': 'Groningen',
    'seo_title': 'Lasergame huren in Groningen | Dagpakketverhuur',
    'meta': 'Lasergame huren in Groningen voor een feest, teamuitje of schoolactiviteit? Wij bezorgen en halen op, '
            'of DHL levert. Geen borg, Compact of XL.',
    'hero': {
        'img': IMG['binnen'][0], 'alt': IMG['binnen'][1], 'pos': '50% 45%',
        'eyebrow': 'Lasergame · Groningen',
        'h1': 'Lasergame huren in Groningen',
        'sub': 'In de stad of op het platteland: wij brengen je lasergame tot aan de deur, '
               'of je laat hem met DHL versturen.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Groningen',
        'h2': 'Een lasergame voor heel Groningen',
        'p': [
            'De provincie Groningen valt binnen ons eigen bezorggebied in Noord-Nederland. Bij het afrekenen kies je een '
            f'tijdslot, en na je event halen we de set weer op. {ZONE}',
            'Komt bezorgen niet uit? Dan versturen we je lasergame met DHL, gratis vanaf €150, of je haalt hem zelf '
            'gratis op in Fochteloo. Borg betaal je in geen van de gevallen.',
        ],
    },
    'products': {**PROD_CHECKS, 'h2': 'Lasergame Compact of XL',
                 'lead': 'Compact voor snelle potjes en kleinere groepen, XL als je langer per ronde wilt spelen.',
                 'info_link': (HUB, 'Hulp bij kiezen')},
    'toepassingen': {
        'h2': 'Populair in Groningen',
        'items': [
            {'icon': 'users', 'h3': 'Studentenhuis of vriendengroep',
             'p': 'Een avond strijd in de tuin of een grote ruimte. Iedereen snapt het spel binnen een paar minuten.'},
            {'icon': 'briefcase', 'h3': 'Teamuitje',
             'p': 'Een actief uitje op jullie eigen locatie, binnen of buiten, zonder begeleider.'},
            {'icon': 'school', 'h3': 'Schoolfeest of sportdag',
             'p': 'Speel op het schoolplein, het sportveld of in de gymzaal. Scholen betalen op factuur.'},
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Geschikt vanaf 6 jaar. Combineer het met andere activiteiten voor een hele middag.',
             'link': (url('/kinderfeestje-groningen/'), 'Kinderfeestje in Groningen')},
        ],
    },
    'steden': None,  # geen eigen Groningse stadspagina's
    'levering': {
        'h2': 'Zo krijg je je lasergame in Groningen',
        'lead': 'Kies bezorgen, verzenden of zelf ophalen bij het afrekenen. Op zondag zijn we gesloten.',
        'items': [LEV_EIGEN('de provincie Groningen'), LEV_DHL, LEV_AFHALEN],
    },
    'b2b': {
        'kicker': 'Zakelijk in Groningen',
        'h2': 'Bedrijven, scholen en verenigingen',
        'p': 'Plan je een personeelsuitje, een sportdag of een clubactiviteit in Groningen? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': [B2B_CHECKS[0], B2B_CHECKS[2]],
        'img': IMG['bos'][0], 'alt': IMG['bos'][1],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Groningen',
        'intro': FAQ_INTRO,
        'items': [
            ('Bezorgen jullie ook in de stad Groningen?',
             f'Ja, de hele provincie Groningen valt binnen ons bezorggebied. {ZONE.split(". ")[0]}. {CALC}.'),
            ('Wanneer is mijn DHL-pakket er?',
             'Eén tot twee werkdagen voor je huurdatum. Je krijgt per mail een trackingcode.'),
            ('Kunnen we binnen spelen?',
             'Ja. Beide sets werken binnen en buiten; een hal, gymzaal of grote ruimte is prima.'),
            ('Moet ik vooraf betalen?',
             'Ja, een bestelling moet volledig betaald zijn vóór de huurdatum, of vóór de verzenddatum bij DHL. '
             'Zakelijke klanten kunnen op factuur betalen.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg.'),
        ],
    },
    'final': {
        'img': IMG['kids'][0], 'alt': IMG['kids'][1],
        'h2': 'Lasergame in Groningen regelen?',
        'p': 'Kies je set en je datum. Geen borg, en met DHL gratis verzonden vanaf €150.',
        'links': [('Alle lasergame-informatie', HUB), ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== C — LEEUWARDEN
PAGES.append({
    **CARDS, 'template': 'C', 'id': 49866, 'slug': 'lasergame-huren-leeuwarden',
    'naam': 'LASERGAME HUREN LEEUWARDEN (STAD)', 'plaats': 'Leeuwarden',
    'seo_title': 'Lasergame huren in Leeuwarden | Dagpakketverhuur',
    'meta': 'Lasergame huren in Leeuwarden, Stiens of Grou? Wij bezorgen en halen op, of je haalt gratis af in Fochteloo. '
            'Geen borg, Compact of XL, vanaf 6 jaar.',
    'hero': {
        'img': IMG['kids'][0], 'alt': IMG['kids'][1], 'pos': '50% 30%',
        'eyebrow': 'Lasergame · Leeuwarden',
        'h1': 'Lasergame huren in Leeuwarden',
        'sub': 'Voor een feestje in de tuin, een teamuitje of een sportmiddag. '
               'Wij bezorgen in Leeuwarden en de dorpen rondom.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Leeuwarden',
        'h2': 'Thuisbezorgd in Leeuwarden',
        'p': [
            'In Leeuwarden en omgeving brengen we je lasergame zelf langs, op het tijdslot dat je bij het afrekenen kiest. '
            f'Na afloop halen we alles weer op. {ZONE}',
            'Heb je een tuin, een veldje in de buurt of een grote ruimte binnen? Meer is niet nodig: de sets zijn binnen '
            '5 minuten speelklaar en werken binnen en buiten.',
        ],
    },
    'products': {**PROD_CHECKS, 'h2': 'Lasergame Compact of XL',
                 'lead': 'Compact voor korte, snelle rondes; XL als je per ronde wat langer wilt spelen.',
                 'info_link': (HUB, 'Welke set past bij jouw groep?')},
    'stappen': {
        'h2': 'Zo werkt huren in Leeuwarden',
        'items': [
            ('Kies je set', 'Lasergame Compact of XL, in het aantal dat je nodig hebt.'),
            ('Kies je tijdslot', 'Bij het afrekenen kies je je eventdatum en wanneer we bij je langskomen.'),
            ('Wij brengen het', 'Eén tot twee dagen vooraf bevestigen we het moment. Dan staan we op tijd voor de deur.'),
            ('Klaarzetten voor ophalen', 'Zet alles compleet en droog klaar tot 16:00 de dag na je event.'),
        ],
    },
    'gelegenheden': {
        'h2': 'Waarvoor huur je een lasergame in Leeuwarden?',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Vanaf 6 jaar speelt iedereen mee. Bij regen verhuis je het spel gewoon naar binnen.',
             'link': (url('/kinderfeestje-leeuwarden/'), 'Kinderfeestje in Leeuwarden')},
            {'icon': 'users', 'h3': 'Vrijgezellenfeest of verjaardag',
             'p': 'Een fanatieke battle voor volwassenen: teams maken, levens tellen, winnaar uitroepen.'},
            {'icon': 'briefcase', 'h3': 'Teamuitje',
             'p': 'Op jullie eigen terrein, zonder begeleider. Iedereen kan direct meedoen.'},
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk in Leeuwarden',
        'h2': 'Ook voor bedrijven, scholen en verenigingen in Leeuwarden',
        'p': 'Organiseer je een sportdag, een uitje voor collega’s of een clubactiviteit? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS[:2],
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
    },
    'levering': {
        'h2': 'Levering in Leeuwarden en omgeving',
        'lead': f'We bezorgen in Leeuwarden en de dorpen eromheen, onder meer in deze plaatsen. {ZONE}',
        'plaatsen': ['Leeuwarden', 'Stiens', 'Grou', 'Goutum', 'Wirdum', 'Jirnsum', 'Warga'],
        'items': [LEV_EIGEN('Leeuwarden en omgeving'), LEV_AFHALEN, LEV_DHL],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Leeuwarden',
        'intro': FAQ_INTRO,
        'items': [
            ('Bezorgen jullie ook in Stiens of Grou?',
             f'Ja, we bezorgen in Leeuwarden en de dorpen eromheen, zoals Stiens, Grou en Goutum. {ZONE.split(". ")[0]}. {CALC}.'),
            ('Wanneer hoor ik hoe laat jullie komen?',
             'Je kiest een tijdslot bij het afrekenen. Eén tot twee dagen voor je huurdatum nemen we contact op om het te bevestigen.'),
            ('Hoeveel ruimte heb ik nodig?',
             'Een tuin, veldje of grote ruimte binnen is genoeg. Struiken, meubels of pallets maken het spel leuker.'),
            ('Kan ik mijn datum nog wijzigen?',
             'Ja, wijzigen of annuleren kan kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg.'),
        ],
    },
    'final': {
        'img': IMG['heg'][0], 'alt': IMG['heg'][1],
        'h2': 'Lasergame in Leeuwarden regelen?',
        'p': 'Kies je set en je datum, wij komen bij je langs. Of laat je set met DHL versturen: gratis vanaf €150.',
        'links': [('Lasergame huren in Friesland', url('/lasergame-huren-friesland/')), ('Alle lasergame-informatie', HUB),
                  ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== C — DRACHTEN
PAGES.append({
    **CARDS, 'template': 'C', 'id': 49891, 'slug': 'lasergame-huren-drachten',
    'naam': 'LASERGAME HUREN DRACHTEN (STAD)', 'plaats': 'Drachten',
    'seo_title': 'Lasergame huren in Drachten | Dagpakketverhuur',
    'meta': 'Lasergame huren in Drachten, Opeinde of Rottevalle? Wij bezorgen en halen op in Smallingerland. '
            'Geen borg, Compact of XL, voor feest en teamuitje.',
    'hero': {
        'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'pos': '50% 40%',
        'eyebrow': 'Lasergame · Drachten',
        'h1': 'Lasergame huren in Drachten',
        'sub': 'Een lasergame voor de tuin, het park of de sporthal. '
               'Wij bezorgen in Drachten en de rest van Smallingerland.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Drachten',
        'h2': 'Bezorgd in Drachten en Smallingerland',
        'p': [
            'Woon je in Drachten of in een van de dorpen van Smallingerland? Dan bezorgen we je lasergame zelf, '
            f'op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
            'Wil je liever zelf rijden? Ophalen in Fochteloo is gratis, vanaf 16:00 de dag voor je event. '
            'En met DHL versturen is gratis vanaf €150.',
        ],
    },
    'products': {**PROD_CHECKS, 'h2': 'Lasergame Compact of XL',
                 'lead': 'Kort en fel spelen met Compact, of langere rondes met XL. De bediening is hetzelfde.',
                 'info_link': (HUB, 'Hulp bij kiezen')},
    'stappen': {
        'h2': 'Zo werkt huren in Drachten',
        'items': [
            ('Kies je set', 'Zet Compact of XL in je winkelwagen, met het aantal dat je wilt.'),
            ('Kies bezorgen of ophalen', 'Bij het afrekenen kies je je datum en of we bezorgen, of dat je zelf ophaalt in Fochteloo.'),
            ('Spelen', 'Guns aan, teams maken en spelen. Binnen een paar minuten ben je bezig.'),
            ('Terug', 'Compleet en droog inleveren of klaarzetten, tot 16:00 de dag na je event.'),
        ],
    },
    'gelegenheden': {
        'h2': 'Waarvoor huur je een lasergame in Drachten?',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Een middag rennen, verstoppen en strijden. Iedereen vanaf 6 jaar doet mee.',
             'link': (url('/kinderfeestje-drachten/'), 'Kinderfeestje in Drachten')},
            {'icon': 'school', 'h3': 'Sportdag of schoolactiviteit',
             'p': 'Op het sportveld of in de gymzaal. Scholen betalen op factuur.'},
            {'icon': 'sun', 'h3': 'Buurtfeest',
             'p': 'Straat tegen straat op een grasveld. Snel opgezet, en na afloop zetten we alles weer op.'},
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk in Drachten',
        'h2': 'Ook voor bedrijven, scholen en verenigingen in Drachten',
        'p': 'Een teamuitje, sportdag of clubmiddag in Smallingerland? Laat weten wat je zoekt en vraag een zakelijke prijs aan.',
        'checks': [B2B_CHECKS[0], B2B_CHECKS[1]],
        'img': IMG['binnen'][0], 'alt': IMG['binnen'][1],
    },
    'levering': {
        'h2': 'Levering in Drachten en omgeving',
        'lead': f'We bezorgen in Drachten en de dorpen van Smallingerland, onder meer in deze plaatsen. {ZONE}',
        'plaatsen': ['Drachten', 'Drachtstercompagnie', 'Opeinde', 'Rottevalle', 'Boornbergum', 'Houtigehage', 'Nijega'],
        'items': [LEV_EIGEN('Drachten en omgeving'), LEV_AFHALEN, LEV_DHL],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Drachten',
        'intro': FAQ_INTRO,
        'items': [
            ('Bezorgen jullie ook in de dorpen rond Drachten?',
             f'Ja, we bezorgen in heel Smallingerland, zoals in Opeinde, Rottevalle en Boornbergum. {ZONE.split(". ")[0]}. {CALC}.'),
            ('Kan ik de lasergame zelf ophalen?',
             'Ja, gratis op Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor je event. We laten vooraf weten wanneer alles klaarligt.'),
            ('Welke set past bij een kinderfeestje?',
             'Compact is kleiner en voordeliger en ideaal voor korte, snelle rondes. Voor langere potjes kies je XL.'),
            ('Moet ik iets schoonmaken?',
             'Nee. Lever alles compleet en droog in; even afvegen is genoeg, schoonmaken doen wij.'),
            ('Betaal ik borg?',
             'Nee, we vragen op dit moment geen borg.'),
        ],
    },
    'final': {
        'img': IMG['veld'][0], 'alt': IMG['veld'][1],
        'h2': 'Lasergame in Drachten regelen?',
        'p': 'Kies je set en je datum, wij komen in Drachten langs. Of verstuur met DHL: gratis vanaf €150.',
        'links': [('Lasergame huren in Friesland', url('/lasergame-huren-friesland/')), ('Alle lasergame-informatie', HUB),
                  ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})

# ================================================================== C — ASSEN
PAGES.append({
    **CARDS, 'template': 'C', 'id': 49874, 'slug': 'lasergame-huren-assen',
    'naam': 'LASERGAME HUREN ASSEN (STAD)', 'plaats': 'Assen',
    'seo_title': 'Lasergame huren in Assen | Dagpakketverhuur',
    'meta': 'Lasergame huren in Assen, Loon of Rolde? Wij bezorgen en halen op, of je haalt gratis af in Fochteloo. '
            'Geen borg, Compact of XL, vanaf 6 jaar.',
    'hero': {
        'img': IMG['heg'][0], 'alt': IMG['heg'][1], 'pos': '50% 35%',
        'eyebrow': 'Lasergame · Assen',
        'h1': 'Lasergame huren in Assen',
        'sub': 'Voor een kinderfeestje, een clubactiviteit of een teamuitje. '
               'Wij bezorgen in Assen en de omliggende dorpen.',
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Lasergame in Assen',
        'h2': 'Lasergame laten bezorgen in Assen',
        'p': [
            'In Assen en omgeving brengen we je lasergame op het tijdslot dat je bij het afrekenen kiest, en halen we hem '
            f'na je event weer op. {ZONE}',
            'Zelf ophalen kan ook, gratis in Fochteloo. Speel je in een gymzaal of op een veld? Beide sets werken binnen '
            'en buiten en zijn binnen 5 minuten klaar voor gebruik.',
        ],
    },
    'products': {**PROD_CHECKS, 'h2': 'Lasergame Compact of XL',
                 'lead': 'Compact: drie balken met levens, korte rondes. XL: vier balken, een langer spel per ronde.',
                 'info_link': (HUB, 'Welke set past bij jouw groep?')},
    'stappen': {
        'h2': 'Zo werkt huren in Assen',
        'items': [
            ('Set kiezen', 'Bepaal hoeveel Compact- of XL-sets je nodig hebt en zet ze in je winkelwagen.'),
            ('Datum en tijdslot', 'Kies bij het afrekenen je eventdatum en het tijdslot voor de bezorging.'),
            ('Bezorging in Assen', 'We komen op het gekozen moment. Liever zelf ophalen? Dat kan gratis in Fochteloo.'),
            ('Ophalen', 'Zet alles compleet klaar tot 16:00 de dag na je event; wij komen het halen.'),
        ],
    },
    'gelegenheden': {
        'h2': 'Waarvoor huur je een lasergame in Assen?',
        'items': [
            {'icon': 'cake', 'h3': 'Kinderfeestje',
             'p': 'Geschikt vanaf 6 jaar. Een tuin of grote kamer is genoeg voor een middag actie.',
             'link': (url('/kinderfeestje-assen/'), 'Kinderfeestje in Assen')},
            {'icon': 'users', 'h3': 'Vereniging of clubactiviteit',
             'p': 'Een afsluiter van het seizoen of een activiteit voor de jeugdleden. Verenigingen betalen op factuur.'},
            {'icon': 'briefcase', 'h3': 'Teamuitje',
             'p': 'Een actieve teamactiviteit op eigen locatie, zonder dat er iemand hoeft te begeleiden.'},
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk in Assen',
        'h2': 'Ook voor bedrijven, scholen en verenigingen in Assen',
        'p': 'Plan je een uitje met collega’s, een schoolactiviteit of een clubdag in Assen? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': [B2B_CHECKS[0], B2B_CHECKS[2]],
        'img': IMG['bos'][0], 'alt': IMG['bos'][1],
    },
    'levering': {
        'h2': 'Levering in Assen en omgeving',
        'lead': f'We bezorgen in Assen en de dorpen eromheen, onder meer in deze plaatsen. {ZONE}',
        'plaatsen': ['Assen', 'Loon', 'Witten', 'Rhee', 'Rolde', 'Vries'],
        'items': [LEV_EIGEN('Assen en omgeving'), LEV_DHL, LEV_AFHALEN],
    },
    'review': {'h2': 'Wat klanten zeggen'},
    'faq': {
        'h2': 'Vragen over lasergame in Assen',
        'intro': FAQ_INTRO,
        'items': [
            ('Bezorgen jullie ook in Rolde of Vries?',
             f'Ja, we bezorgen in Assen en de dorpen eromheen, zoals Loon, Rolde en Vries. {ZONE.split(". ")[0]}. {CALC}.'),
            ('Kunnen we in een gymzaal spelen?',
             'Ja. Beide sets werken binnen en buiten, dus een gymzaal, sporthal of grote ruimte is prima.'),
            ('Kan onze vereniging op factuur betalen?',
             'Ja. Vul bij het afrekenen je organisatie en eventueel een referentie in en kies betalen op factuur. '
             'De factuur moet vóór de huurdatum betaald zijn.'),
            ('Wat als ik moet annuleren?',
             'Wijzigen of annuleren kan kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, '
             'inclusief bezorgkosten.'),
            ('Vanaf welke leeftijd is lasergame geschikt?',
             'Vanaf 6 jaar. Tieners en volwassenen spelen net zo goed mee.'),
        ],
    },
    'final': {
        'img': IMG['kids'][0], 'alt': IMG['kids'][1],
        'h2': 'Lasergame in Assen regelen?',
        'p': 'Kies je set en je datum, wij bezorgen in Assen. Of laat je set met DHL versturen: gratis vanaf €150.',
        'links': [('Lasergame huren in Drenthe', url('/lasergame-huren-drenthe/')), ('Alle lasergame-informatie', HUB),
                  ('Lasergame Compact', COMPACT), ('Lasergame XL', XL)],
    },
})
