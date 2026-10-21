"""
Fase 4b — Silent Disco-cluster. Hub = oriëntatie (primaire CTA naar het product),
product = boeken. Regio's linken naar hub én product.

Feiten (bron: productpagina's, /contact/, audit-intro van Joris):
- Silent disco koptelefoons: per stuk te huren, maximaal 3 muziekkanalen tegelijk.
- Glow Bundel per persoon: koptelefoons incl. Bluetooth zender + glow-in-the-dark armbanden;
  aantal personen = aantal in de winkelmand.
- Zenders los te huren: Bluetooth zender, bedrade zender.
- Kleinere producten via DHL door heel NL (€16, gratis vanaf €150); grotere producten eigen
  bezorging per zone; gratis afhalen in Fochteloo.
- Geen echte silent-disco-review beschikbaar ("Femke B."/"Martijn K." zijn sjabloonteksten):
  echte reviews van de homepage worden gebruikt, met hun eigen context.
"""
import os as _os
from build import url, TEL
from reviews import JURGEN, BABYSHOWER, MARJOLIJN

U = url('/wp-content/uploads')
IMG = {
    # Bestaande site-afbeeldingen; alt-teksten beschrijven wat er te zien is.
    'feest': (U + '/2026/08/Gemini_Generated_Image_sbd730sbd730sbd7_11zon.webp',
              'Avondfeest onder een tent met feestverlichting en gasten'),
    'tuin': (U + '/2026/08/Gemini_Generated_Image_afvuyfafvuyfafvu_11zon.webp',
             'Tuinfeest met tenten en verlichting in de avond'),
    'locatie': (U + '/2026/08/Gemini_Generated_Image_afvuyfafvuyfafvu_11zon.webp',
                'Feestlocatie in de tuin met tenten en lichtjes'),
    'binnen': (U + '/2026/02/unnamed-1_11zon.webp',
               'Kinderen dansen met silent disco koptelefoons onder een feesttent'),
}
PROD = url('/product/silent-disco-huren/')
GLOW = url('/product/silent-disco-glow-bundel-per-persoon-huren/')
BT = url('/product/bluetooth-zender-huren/')
BEDRAAD = url('/product/bedrade-zender-huren/')
HUB = url('/silent-disco-verhuur/')
CONTACT = url('/contact/')
CAT = url('/product-category/licht-geluid-huren/geluid-huren/'
          if _os.environ.get('DPV_HOST', 'live') == 'live' else '/product-category/geluidsapparatuur-huren/silent-disco-huren/')
CARDS = {'product_ids': [47241, 51209], 'cat_url': CAT,
         'product_alts': {47241: 'Silent disco koptelefoons huren', 51209: 'Silent disco glow bundel per persoon huren'}}

ZONE = 'Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.'
CALC = f'<a href="{CONTACT}">Bereken het met je postcode</a>'
FAQ_INTRO = 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.'
TRUST = [
    ('shield', 'Geen borg', 'Je betaalt alleen de huurprijs'),
    ('pin', 'Gratis afhalen in Fochteloo', 'Vanaf 16:00 de dag voor je event'),
    ('truck', 'Levering in heel Nederland', 'Verzonden met DHL'),
    ('gift', 'Gratis verzending vanaf €150', 'Met DHL, bij een besteding vanaf €150'),
]
LEV_DHL = {'icon': 'calendar', 'h3': 'Verzending met DHL',
           'p': 'Silent disco versturen we met DHL door heel Nederland, voor €16 per pakket en gratis vanaf €150. '
                'Het pakket is er één tot twee werkdagen voor je huurdatum.'}
LEV_AFHALEN = {'icon': 'pin', 'h3': 'Gratis afhalen in Fochteloo',
               'p': 'Ophalen op Verlaat 3 in Fochteloo is altijd gratis: vanaf 16:00 de dag voor je feest, terugbrengen tot 16:00 de dag erna.'}
LEV_COMBI = lambda gebied: {'icon': 'truck', 'h3': 'Samen met grotere producten',
                            'p': f'Combineer je silent disco met bijvoorbeeld een partytent? Dan bezorgen we in {gebied} alles in één keer zelf. {ZONE}',
                            'link': (CONTACT, 'Bereken je bezorgkosten')}
B2B_CHECKS = [
    'Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen',
    'Betalen op factuur, met je eigen referentie of PO-nummer',
]

PAGES = []

# ================================================================== A — HUB (oriëntatie)
PAGES.append({
    **CARDS, 'template': 'A', 'id': 49767, 'slug': 'silent-disco-verhuur', 'naam': 'SILENT DISCO VERHUUR (HUB)',
    'plaats': 'Nederland',
    'seo_title': 'Silent disco huren | Heel Nederland via DHL | Dagpakketverhuur',
    'meta': 'Silent disco huren voor een verjaardag, bruiloft of bedrijfsfeest? Draadloze koptelefoons met tot 3 kanalen, '
            'via DHL door heel Nederland. Geen borg.',
    'hero': {
        'img': IMG['feest'][0], 'alt': IMG['feest'][1], 'pos': '50% 40%',
        'eyebrow': 'Silent disco · Heel Nederland',
        'h1': 'Silent disco huren<br>door heel Nederland',
        'sub': 'Iedereen danst op zijn eigen muziek, zonder geluidsoverlast. Verzonden met DHL, of gratis afhalen in Fochteloo.',
        'cta': 'Silent disco boeken', 'cta_href': PROD,
    },
    'trust': TRUST,
    'intro': {
        'kicker': 'Wat is silent disco?',
        'h2': 'Dansen zonder geluidsoverlast',
        'p': [
            'Silent disco huren voor een verjaardag, bruiloft, bedrijfsfeest of tuinfeest? Bij Dagpakketverhuur huur je complete '
            'silent disco sets met draadloze koptelefoons en zender. De sets zijn eenvoudig zelf aan te sluiten en worden via DHL '
            'door heel Nederland geleverd. Je kiest zelf hoeveel koptelefoons en muziekkanalen je nodig hebt.',
            'Met maximaal 3 muziekkanalen tegelijk kiest iedere gast zijn eigen muziek. De buren horen niets, dus je kunt binnen '
            'en buiten doorgaan zolang je wilt.',
        ],
    },
    'products': {
        'h2': 'Zo stel je je silent disco samen', 'cat_link': CAT, 'cat_label': 'Alle geluidsapparatuur',
        'lead': 'Huur koptelefoons per stuk, of de Glow Bundel per persoon met zender en glow-armbanden.',
        'checks': ['Maximaal 3 muziekkanalen tegelijk', 'Binnen en buiten te gebruiken', 'Via DHL door heel Nederland', 'Geen borg'],
        'info_h3': 'Goed om te weten', 'info_link': (PROD, 'Naar silent disco boeken'),
    },
    'keuze': {
        'h2': 'Wat heb je nodig?',
        'items': [
            {'tag': 'Koptelefoons', 'h3': 'Per stuk, zoveel als je gasten',
             'p': 'Draadloze silent disco koptelefoons met tot 3 kanalen. Je kiest zelf het aantal.',
             'link': (PROD, 'Koptelefoons kiezen')},
            {'tag': 'Glow Bundel', 'h3': 'Alles per persoon, met glow-effect',
             'p': 'Koptelefoons inclusief Bluetooth zender en glow-in-the-dark armbanden. Aantal personen = aantal in je winkelmand.',
             'link': (GLOW, 'Bekijk de Glow Bundel')},
            {'tag': 'Zender', 'h3': 'Muziek naar de koptelefoons',
             'p': f'Kies een <a href="{BT}">Bluetooth zender</a> voor je telefoon of een <a href="{BEDRAAD}">bedrade zender</a> voor een mengpaneel of laptop.',
             'soft': True},
        ],
    },
    'gelegenheden': {
        'h2': 'Voor welk feest?',
        'items': [
            {'icon': 'gift', 'h3': 'Bruiloft', 'p': 'Dansen tot laat, terwijl de omgeving niets hoort. Ieder kiest zijn eigen kanaal.'},
            {'icon': 'users', 'h3': 'Verjaardag of tuinfeest', 'p': 'Een feest in de tuin dat gewoon door kan na tienen.'},
            {'icon': 'briefcase', 'h3': 'Bedrijfsfeest', 'p': 'Een activiteit waar iedereen aan meedoet, zonder dat je hoeft te schreeuwen.',
             'link': (url('/zakelijk/'), 'Zakelijk huren')},
            {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een kinderdisco in de woonkamer zonder dat het hele huis meedreunt.',
             'link': (url('/kinderfeestje/'), 'Kinderfeestje regelen')},
        ],
    },
    'stappen': {
        'h2': 'Zo werkt huren',
        'items': [
            ('Kies je set', 'Koptelefoons per stuk of de Glow Bundel per persoon, plus een zender als je die nodig hebt.'),
            ('Kies je datum', 'Bij het afrekenen kies je je feestdatum en of je laat verzenden of zelf ophaalt.'),
            ('Aansluiten', 'Zender aan je muziekbron, koptelefoons aan en kanaal kiezen.'),
            ('Retour', 'Compleet terug tot 16:00 de dag na je feest.'),
        ],
    },
    'regio': {
        'h2': 'Silent disco in Noord-Nederland',
        'lead': 'In Friesland, Groningen en Drenthe kun je ook gratis afhalen in Fochteloo of alles met grotere producten laten bezorgen.',
        'items': [
            ('Friesland', 'Silent disco huren in Friesland', url('/silent-disco-huren-friesland/')),
            ('Drenthe', 'Silent disco huren in Drenthe', url('/silent-disco-huren-drenthe/')),
            ('Groningen', 'Silent disco huren in Groningen', url('/silent-disco-huren-groningen/')),
        ],
    },
    'b2b': {
        'kicker': 'Zakelijk',
        'h2': 'Voor bedrijven, scholen en verenigingen',
        'p': 'Een personeelsfeest, schoolfeest of clubavond? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
        'checks': B2B_CHECKS + ['Alle prijzen inclusief 21% btw, apart op je factuur'],
        'img': IMG['binnen'][0], 'alt': IMG['binnen'][1],
    },
    'review': {'h2': 'Wat klanten zeggen', 'data': BABYSHOWER},
    'faq': {
        'h2': 'Veelgestelde vragen',
        'intro': FAQ_INTRO,
        'items': [
            ('Hoeveel kanalen heeft een silent disco?', 'Maximaal 3 muziekkanalen tegelijk. Gasten kiezen zelf welk kanaal ze luisteren.'),
            ('Hoeveel koptelefoons heb ik nodig?',
             'Dat bepaal je zelf: je huurt de koptelefoons per stuk. Bij de Glow Bundel kies je het aantal personen.'),
            ('Wat heb ik nodig om muziek af te spelen?',
             'Een zender: Bluetooth voor je telefoon, of bedraad voor een laptop of mengpaneel. In de Glow Bundel zit een Bluetooth zender.'),
            ('Bezorgen jullie door heel Nederland?',
             'Ja, met DHL: €16 per pakket, gratis vanaf €150. Het pakket is er één tot twee werkdagen voor je huurdatum.'),
            ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.'),
            ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor je huurdatum. Daarna rekenen we 100% van het huurbedrag, inclusief verzendkosten.'),
        ],
    },
    'final': {
        'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'cta': 'Silent disco boeken', 'cta_href': PROD,
        'h2': 'Klaar voor een stille disco?',
        'p': 'Kies je koptelefoons en je datum. Geen borg, en met DHL gratis verzonden vanaf €150.',
        'links': [('Silent disco koptelefoons', PROD), ('Glow Bundel per persoon', GLOW)],
    },
})


def regio_base(prov):
    return {
        **CARDS, 'trust': TRUST,
        'products': {'h2': 'Silent disco koptelefoons of Glow Bundel',
                     'lead': 'Koptelefoons per stuk, of alles per persoon met zender en glow-armbanden.',
                     'checks': ['Tot 3 muziekkanalen', 'Zender los of in de Glow Bundel', 'Gratis afhalen in Fochteloo', 'Geen borg'],
                     'info_h3': 'Goed om te weten', 'info_link': (HUB, 'Alles over silent disco huren')},
        'b2b': {'kicker': f'Zakelijk in {prov}', 'checks': B2B_CHECKS,
                'img': IMG['binnen'][0], 'alt': IMG['binnen'][1]},
    }


# ================================================================== B — FRIESLAND
PAGES.append({
    **regio_base('Friesland'), 'template': 'B', 'id': 49704, 'slug': 'silent-disco-huren-friesland',
    'naam': 'SILENT DISCO HUREN FRIESLAND (PROVINCIE)', 'plaats': 'Friesland',
    'seo_title': 'Silent disco huren in Friesland | Dagpakketverhuur',
    'meta': 'Silent disco huren in Friesland? Gratis afhalen in Fochteloo of via DHL verstuurd. Koptelefoons met tot 3 kanalen, geen borg.',
    'hero': {'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'pos': '50% 50%', 'eyebrow': 'Silent disco · Friesland',
             'h1': 'Silent disco huren in Friesland', 'cta': 'Bekijk silent disco',
             'sub': 'Haal je silent disco gratis op in Fochteloo, of laat hem met DHL naar je toe sturen.'},
    'intro': {'kicker': 'Silent disco in Friesland', 'h2': 'Vanuit Fochteloo naar jouw feest',
              'p': ['Onze silent disco sets liggen klaar in Fochteloo, in het zuidoosten van Friesland. Ophalen is gratis, vanaf 16:00 de dag voor je feest.',
                    'Woon je verder weg? Dan sturen we de koptelefoons met DHL, gratis vanaf €150. Je kiest zelf hoeveel koptelefoons je nodig hebt.']},
    'toepassingen': {'h2': 'Populair in Friesland', 'items': [
        {'icon': 'gift', 'h3': 'Bruiloft op een boerderij of in de tuin', 'p': 'Doorfeesten zonder geluidsoverlast voor de omgeving.'},
        {'icon': 'users', 'h3': 'Verjaardag', 'p': 'Drie kanalen, dus jong en oud kiest zijn eigen muziek.'},
        {'icon': 'school', 'h3': 'Schoolfeest of vereniging', 'p': 'Een disco in de kantine of gymzaal. Scholen betalen op factuur.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een kinderdisco zonder dat het hele huis meedreunt.',
         'link': (url('/kinderfeestje-friesland/'), 'Kinderfeestje in Friesland')}]},
    'steden': {'h2': 'Silent disco in Friese steden', 'lead': 'Voor Leeuwarden hebben we een eigen pagina.',
               'items': [('Leeuwarden', 'Silent disco huren in Leeuwarden', url('/silent-disco-huren-leeuwarden/'))]},
    'levering': {'h2': 'Afhalen, versturen of laten bezorgen', 'lead': 'Je kiest bij het afrekenen. Op zondag zijn we gesloten.',
                 'items': [LEV_AFHALEN, LEV_DHL, LEV_COMBI('Friesland')]},
    'b2b': {**regio_base('Friesland')['b2b'], 'h2': 'Voor teams, scholen en clubs',
            'p': 'Een personeelsfeest of clubavond in Friesland? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.'},
    'review': {'h2': 'Wat klanten zeggen', 'data': JURGEN},
    'faq': {'h2': 'Vragen over silent disco in Friesland', 'intro': FAQ_INTRO, 'items': [
        ('Waar haal ik de silent disco op?', 'Op Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor je feest. Ophalen is gratis.'),
        ('Kunnen jullie het ook versturen?', 'Ja, met DHL door heel Nederland: €16 per pakket, gratis vanaf €150.'),
        ('Hoeveel kanalen zijn er?', 'Maximaal 3 tegelijk. Iedere gast kiest zelf.'),
        ('Feest op zondag?', 'Dan regelen we ophalen en terugbrengen op zaterdag of maandag, zonder extra huurdag.')]},
    'final': {'img': IMG['feest'][0], 'alt': IMG['feest'][1], 'cta': 'Bekijk silent disco',
              'h2': 'Silent disco in Friesland regelen?', 'p': 'Gratis ophalen in Fochteloo, of DHL-verzending gratis vanaf €150.',
              'links': [('Alles over silent disco', HUB), ('Silent disco koptelefoons', PROD), ('Glow Bundel', GLOW)]},
})

# ================================================================== B — GRONINGEN
PAGES.append({
    **regio_base('Groningen'), 'template': 'B', 'id': 49699, 'slug': 'silent-disco-huren-groningen',
    'naam': 'SILENT DISCO HUREN GRONINGEN (PROVINCIE)', 'plaats': 'Groningen',
    'seo_title': 'Silent disco huren in Groningen | Dagpakketverhuur',
    'meta': 'Silent disco huren in Groningen voor een feest, studentenavond of bedrijfsfeest? Via DHL verstuurd, tot 3 kanalen, geen borg.',
    'hero': {'img': IMG['feest'][0], 'alt': IMG['feest'][1], 'pos': '50% 60%', 'eyebrow': 'Silent disco · Groningen',
             'h1': 'Silent disco huren in Groningen', 'cta': 'Bekijk silent disco',
             'sub': 'In de stad of daarbuiten: wij sturen je silent disco met DHL, of je haalt hem gratis op.'},
    'intro': {'kicker': 'Silent disco in Groningen', 'h2': 'Een feest zonder klachten van de buren',
              'p': ['Silent disco werkt overal waar muziek een probleem is: in een studentenhuis, een appartement of een tuin midden in het dorp.',
                    'We versturen de koptelefoons met DHL, gratis vanaf €150. Combineer je met grotere producten, dan bezorgen we in de provincie '
                    f'Groningen ook zelf. {ZONE}']},
    'toepassingen': {'h2': 'Populair in Groningen', 'items': [
        {'icon': 'users', 'h3': 'Studentenhuis of huisfeest', 'p': 'Feest tot laat zonder dat de buren iets horen.'},
        {'icon': 'briefcase', 'h3': 'Bedrijfsfeest', 'p': 'Een dansvloer waar iedereen zijn eigen muziek kiest.'},
        {'icon': 'school', 'h3': 'Schoolfeest', 'p': 'Een disco in de aula of gymzaal; scholen betalen op factuur.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Kinderdisco in de woonkamer, rustig voor de rest van het huis.',
         'link': (url('/kinderfeestje-groningen/'), 'Kinderfeestje in Groningen')}]},
    'steden': None,
    'levering': {'h2': 'Zo krijg je je silent disco in Groningen', 'lead': 'Kies verzenden of ophalen bij het afrekenen. Op zondag zijn we gesloten.',
                 'items': [LEV_DHL, LEV_COMBI('de provincie Groningen'), LEV_AFHALEN]},
    'b2b': {**regio_base('Groningen')['b2b'], 'h2': 'Bedrijven, scholen en verenigingen',
            'p': 'Een feest voor collega’s, een schoolfeest of een clubavond in Groningen? Vraag een zakelijke prijs aan.'},
    'review': {'h2': 'Wat klanten zeggen', 'data': BABYSHOWER},
    'faq': {'h2': 'Vragen over silent disco in Groningen', 'intro': FAQ_INTRO, 'items': [
        ('Wanneer is mijn pakket er?', 'Eén tot twee werkdagen voor je huurdatum. Je krijgt per mail een trackingcode.'),
        ('Welke zender heb ik nodig?', f'Een <a href="{BT}">Bluetooth zender</a> voor je telefoon of een <a href="{BEDRAAD}">bedrade zender</a> voor een laptop of mengpaneel.'),
        ('Moet ik vooraf betalen?', 'Ja, vóór de verzenddatum. Zakelijke klanten kunnen op factuur betalen.'),
        ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')]},
    'final': {'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'cta': 'Bekijk silent disco',
              'h2': 'Silent disco in Groningen regelen?', 'p': 'Kies je koptelefoons en je datum. Met DHL gratis verzonden vanaf €150.',
              'links': [('Alles over silent disco', HUB), ('Silent disco koptelefoons', PROD), ('Glow Bundel', GLOW)]},
})

# ================================================================== B — DRENTHE
PAGES.append({
    **regio_base('Drenthe'), 'template': 'B', 'id': 49709, 'slug': 'silent-disco-huren-drenthe',
    'naam': 'SILENT DISCO HUREN DRENTHE (PROVINCIE)', 'plaats': 'Drenthe',
    'seo_title': 'Silent disco huren in Drenthe | Dagpakketverhuur',
    'meta': 'Silent disco huren in Drenthe? Koptelefoons met tot 3 kanalen, via DHL of gratis afhalen in Fochteloo. Voor feest, bruiloft en school.',
    'hero': {'img': IMG['locatie'][0], 'alt': IMG['locatie'][1], 'pos': '50% 50%', 'eyebrow': 'Silent disco · Drenthe',
             'h1': 'Silent disco huren in Drenthe', 'cta': 'Bekijk silent disco',
             'sub': 'Van Assen tot Emmen: dansen op je eigen muziek, zonder geluidsoverlast.'},
    'intro': {'kicker': 'Silent disco in Drenthe', 'h2': 'Doorfeesten, ook als het stil moet zijn',
              'p': ['In een rustige straat of op een camping wil je de omgeving niet storen. Met silent disco hoort alleen wie een koptelefoon op heeft de muziek.',
                    'We versturen met DHL, gratis vanaf €150, of je haalt gratis op in Fochteloo. Samen met grotere producten bezorgen we in Drenthe ook zelf.']},
    'toepassingen': {'h2': 'Populair in Drenthe', 'items': [
        {'icon': 'gift', 'h3': 'Bruiloft', 'p': 'Een dansvloer die tot laat kan blijven draaien.'},
        {'icon': 'sun', 'h3': 'Tuin- of buurtfeest', 'p': 'Muziek voor iedereen, rust voor de straat.'},
        {'icon': 'school', 'h3': 'Schoolfeest', 'p': 'Drie kanalen voor verschillende muzieksmaken; scholen betalen op factuur.'},
        {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een kinderdisco met glow-armbanden uit de Glow Bundel.',
         'link': (url('/kinderfeestje-drenthe/'), 'Kinderfeestje in Drenthe')}]},
    'steden': {'h2': 'Silent disco in Drentse steden', 'lead': 'Voor deze plaatsen hebben we een eigen pagina.',
               'items': [('Assen', 'Silent disco huren in Assen', url('/silent-disco-huren-assen/')),
                         ('Emmen', 'Silent disco huren in Emmen', url('/silent-disco-huren-emmen/'))]},
    'levering': {'h2': 'Verzenden, afhalen of laten bezorgen', 'lead': 'Je kiest bij het afrekenen wat het beste uitkomt.',
                 'items': [LEV_DHL, LEV_AFHALEN, LEV_COMBI('Drenthe')]},
    'b2b': {**regio_base('Drenthe')['b2b'], 'h2': 'Bedrijven, scholen en verenigingen',
            'p': 'Een feestavond voor collega’s of leerlingen in Drenthe? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.'},
    'review': {'h2': 'Wat klanten zeggen', 'data': JURGEN},
    'faq': {'h2': 'Vragen over silent disco in Drenthe', 'intro': FAQ_INTRO, 'items': [
        ('Hoe krijg ik de silent disco in Drenthe?', 'Met DHL (gratis vanaf €150), gratis afhalen in Fochteloo, of samen met grotere producten door ons bezorgd.'),
        ('Wat zit er in de Glow Bundel?', 'Koptelefoons met Bluetooth zender en glow-in-the-dark armbanden, per persoon te huren.'),
        ('Kan ik silent disco buiten gebruiken?', 'Ja, binnen en buiten. Zo stoor je de omgeving niet.'),
        ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor je huurdatum.')]},
    'final': {'img': IMG['feest'][0], 'alt': IMG['feest'][1], 'cta': 'Bekijk silent disco',
              'h2': 'Silent disco in Drenthe regelen?', 'p': 'Kies je koptelefoons en je datum. Gratis afhalen in Fochteloo kan altijd.',
              'links': [('Alles over silent disco', HUB), ('Silent disco koptelefoons', PROD), ('Glow Bundel', GLOW)]},
})


def stad(pid, slug, s_, prov, prov_slug, hero_img, intro, stappen, gel, plaatsen, faq, review, final_img, meta, kinder):
    base = regio_base(s_)
    return {
        **base, 'template': 'C', 'id': pid, 'slug': slug, 'naam': f'SILENT DISCO HUREN {s_.upper()} (STAD)', 'plaats': s_,
        'seo_title': f'Silent disco huren in {s_} | Dagpakketverhuur', 'meta': meta,
        'hero': {'img': hero_img[0], 'alt': hero_img[1], 'pos': '50% 45%', 'eyebrow': f'Silent disco · {s_}',
                 'h1': f'Silent disco huren in {s_}', 'cta': 'Bekijk silent disco', 'sub': intro.pop('sub')},
        'intro': intro,
        'products': {**base['products'], 'h2': 'Koptelefoons of Glow Bundel'},
        'stappen': {'h2': f'Zo werkt huren in {s_}', 'items': stappen},
        'gelegenheden': {'h2': f'Waarvoor huur je een silent disco in {s_}?', 'items': gel + [kinder]},
        'b2b': {**base['b2b'], 'h2': f'Ook voor bedrijven, scholen en verenigingen in {s_}',
                'p': f'Een personeelsfeest, schoolfeest of clubavond in {s_}? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.'},
        'levering': {'h2': f'Levering in {s_} en omgeving',
                     'lead': f'Silent disco versturen we met DHL; samen met grotere producten bezorgen we ook zelf, onder meer in deze plaatsen. {ZONE}',
                     'plaatsen': plaatsen, 'items': [LEV_DHL, LEV_AFHALEN, LEV_COMBI(f'{s_} en omgeving')]},
        'review': {'h2': 'Wat klanten zeggen', 'data': review},
        'faq': {'h2': f'Vragen over silent disco in {s_}', 'intro': FAQ_INTRO, 'items': faq},
        'final': {'img': final_img[0], 'alt': final_img[1], 'cta': 'Bekijk silent disco',
                  'h2': f'Silent disco in {s_} regelen?', 'p': 'Kies je koptelefoons en je datum. Met DHL gratis verzonden vanaf €150.',
                  'links': [(f'Silent disco huren in {prov}', url(f'/silent-disco-huren-{prov_slug}/')), ('Alles over silent disco', HUB),
                            ('Silent disco koptelefoons', PROD), ('Glow Bundel', GLOW)]},
    }


PAGES.append(stad(
    49900, 'silent-disco-huren-leeuwarden', 'Leeuwarden', 'Friesland', 'friesland', IMG['feest'],
    {'sub': 'Een silent disco voor je feest in Leeuwarden: verzonden met DHL of gratis opgehaald in Fochteloo.',
     'kicker': 'Silent disco in Leeuwarden', 'h2': 'Silent disco voor je feest in Leeuwarden',
     'p': ['In een binnenstad of drukke wijk wil je niemand storen. Met silent disco dansen je gasten op hun eigen kanaal, terwijl het buiten stil blijft.',
           'We versturen de koptelefoons met DHL, gratis vanaf €150. Liever zelf ophalen? Dat kan gratis in Fochteloo.']},
    [('Kies je koptelefoons', 'Per stuk, of de Glow Bundel per persoon.'), ('Kies je datum', 'En of je laat verzenden of zelf ophaalt.'),
     ('Aansluiten', 'Zender aan je telefoon of laptop, koptelefoons aan, kanaal kiezen.'), ('Terug', 'Compleet terug tot 16:00 de dag na je feest.')],
    [{'icon': 'users', 'h3': 'Huisfeest of verjaardag', 'p': 'Feest tot laat in je appartement of tuin, zonder klachten.'},
     {'icon': 'briefcase', 'h3': 'Bedrijfsfeest', 'p': 'Een interactieve dansvloer voor collega’s.'}],
    ['Leeuwarden', 'Stiens', 'Grou', 'Goutum', 'Wirdum'],
    [('Kan ik de silent disco laten versturen naar Leeuwarden?', 'Ja, met DHL: €16 per pakket, gratis vanaf €150.'),
     ('Hoeveel kanalen zijn er?', 'Maximaal 3 tegelijk.'),
     ('Welke zender heb ik nodig?', f'Bluetooth voor je telefoon (<a href="{BT}">Bluetooth zender</a>) of bedraad voor laptop of mengpaneel.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    BABYSHOWER, IMG['tuin'],
    'Silent disco huren in Leeuwarden? Koptelefoons met tot 3 kanalen, via DHL verstuurd of gratis afhalen in Fochteloo. Geen borg.',
    {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een kinderdisco in de woonkamer.', 'link': (url('/kinderfeestje-leeuwarden/'), 'Kinderfeestje in Leeuwarden')}))

PAGES.append(stad(
    49908, 'silent-disco-huren-assen', 'Assen', 'Drenthe', 'drenthe', IMG['locatie'],
    {'sub': 'Dansen zonder geluidsoverlast in Assen: wij versturen met DHL, of je haalt gratis op in Fochteloo.',
     'kicker': 'Silent disco in Assen', 'h2': 'Silent disco huren in Assen',
     'p': ['Een feest in de tuin, de kantine van de club of een zaaltje: met silent disco hoort alleen wie een koptelefoon op heeft de muziek.',
           'Kies koptelefoons per stuk, of de Glow Bundel met zender en glow-armbanden. We versturen met DHL, gratis vanaf €150.']},
    [('Set kiezen', 'Koptelefoons per stuk of de Glow Bundel.'), ('Datum kiezen', 'Bij het afrekenen, samen met verzenden of ophalen.'),
     ('Muziek kiezen', 'Tot 3 kanalen, dus verschillende playlists tegelijk.'), ('Terugsturen of inleveren', 'Compleet, tot 16:00 de dag na je feest.')],
    [{'icon': 'users', 'h3': 'Clubavond of vereniging', 'p': 'Een disco in de kantine; verenigingen betalen op factuur.'},
     {'icon': 'sun', 'h3': 'Tuinfeest', 'p': 'Muziek tot laat, zonder de buren te storen.'}],
    ['Assen', 'Loon', 'Witten', 'Rolde', 'Vries'],
    [('Hoe snel is de silent disco er?', 'Met DHL is het pakket er één tot twee werkdagen voor je huurdatum.'),
     ('Kan onze vereniging op factuur betalen?', 'Ja, vul bij het afrekenen je organisatie in en kies betalen op factuur.'),
     ('Wat zit er in de Glow Bundel?', 'Koptelefoons met Bluetooth zender en glow-in-the-dark armbanden.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    JURGEN, IMG['feest'],
    'Silent disco huren in Assen, Rolde of Vries? Koptelefoons met tot 3 kanalen, via DHL of gratis afhalen in Fochteloo. Geen borg.',
    {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Kinderdisco met glow-armbanden.', 'link': (url('/kinderfeestje-assen/'), 'Kinderfeestje in Assen')}))

PAGES.append(stad(
    49916, 'silent-disco-huren-emmen', 'Emmen', 'Drenthe', 'drenthe', IMG['tuin'],
    {'sub': 'Een silent disco voor je feest in Emmen of de dorpen eromheen. Verzonden met DHL of gratis opgehaald.',
     'kicker': 'Silent disco in Emmen', 'h2': 'Silent disco voor feesten in Emmen',
     'p': ['Of je nu viert in Emmen, Klazienaveen of Nieuw-Amsterdam: met draadloze koptelefoons kies je zelf de muziek, zonder geluidsoverlast.',
           'We sturen de set met DHL, gratis vanaf €150, of je haalt hem gratis op in Fochteloo.']},
    [('Kies je set', 'Koptelefoons per stuk of de Glow Bundel per persoon.'), ('Kies je datum', 'Plus verzenden of zelf ophalen.'),
     ('Feesten', 'Zender aansluiten en tot 3 kanalen tegelijk draaien.'), ('Retour', 'Compleet terug tot 16:00 de dag na je feest.')],
    [{'icon': 'gift', 'h3': 'Bruiloft of jubileum', 'p': 'Een dansvloer die tot laat kan doorgaan.'},
     {'icon': 'school', 'h3': 'Schoolfeest', 'p': 'Een disco in de gymzaal; scholen betalen op factuur.'}],
    ['Emmen', 'Klazienaveen', 'Nieuw-Amsterdam', 'Erica', 'Schoonebeek'],
    [('Versturen jullie ook naar Klazienaveen of Erica?', 'Ja, met DHL door heel Nederland: €16 per pakket, gratis vanaf €150.'),
     ('Hoeveel koptelefoons heb ik nodig?', 'Dat kies je zelf; je huurt ze per stuk.'),
     ('Kan ik buiten feesten?', 'Ja, de koptelefoons werken binnen en buiten.'),
     ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor je huurdatum.')],
    BABYSHOWER, IMG['locatie'],
    'Silent disco huren in Emmen, Klazienaveen of Nieuw-Amsterdam? Tot 3 kanalen, via DHL of gratis afhalen in Fochteloo. Geen borg.',
    {'icon': 'cake', 'h3': 'Kinderfeestje', 'p': 'Een kinderdisco zonder lawaai.', 'link': (url('/kinderfeestje-emmen/'), 'Kinderfeestje in Emmen')}))


# ------------------------------------------------------------------ variatie per pagina (overlap ≤0,35)
VAR = {
    'silent-disco-huren-leeuwarden': dict(
        lead='Huur losse koptelefoons, of kies per gast de Glow Bundel met zender en lichtgevende armbanden.',
        checks=['Drie kanalen tegelijk', 'Bluetooth of bedrade zender', 'Ophalen in Fochteloo kost niets', 'Geen borg'],
        dhl='Naar Leeuwarden versturen we met DHL: €16 per pakket, gratis bij een bestelling vanaf €150. Het pakket komt één tot twee werkdagen voor je huurdatum.',
        afhalen='In Fochteloo ligt alles klaar vanaf 16:00 de dag voor je feest. Ophalen kost niets; terugbrengen tot 16:00 de dag erna.',
        lev_lead=f'Versturen gaat met DHL. Bestel je ook grotere spullen, dan rijden we in Leeuwarden en omgeving zelf langs. {ZONE}',
        final='Kies het aantal koptelefoons en je feestdatum; DHL brengt ze gratis vanaf €150.',
        b2b='Een feestavond met collega’s of een schoolfeest in Leeuwarden? Laat weten wat je zoekt; je krijgt binnen één werkdag een vaste prijs.'),
    'silent-disco-huren-assen': dict(
        lead='Kies het aantal koptelefoons, of reken per persoon met de Glow Bundel.',
        checks=['Maximaal drie muziekkanalen', 'Zender inbegrepen in de Glow Bundel', 'Binnen en buiten bruikbaar', 'Geen borg'],
        dhl='DHL bezorgt de silent disco in Assen voor €16 per pakket; vanaf €150 is verzenden gratis.',
        afhalen='Zelf rijden? Ophalen op Verlaat 3 in Fochteloo is gratis, vanaf 16:00 de dag voor je feest.',
        lev_lead=f'Silent disco gaat met DHL. Huur je er een partytent of meubilair bij, dan bezorgen we in Assen en omgeving alles zelf. {ZONE}',
        final='Kies je set en datum. Gratis afhalen in Fochteloo, of DHL gratis vanaf €150.',
        b2b='Een clubavond, schoolfeest of personeelsfeest in Assen? Vraag een zakelijke prijs aan en betaal op factuur.'),
    'silent-disco-huren-emmen': dict(
        lead='Losse koptelefoons per stuk, of de Glow Bundel per persoon met een Bluetooth zender erbij.',
        checks=['Gasten kiezen uit drie kanalen', 'Glow-armbanden in de bundel', 'Afhalen in Fochteloo is gratis', 'Geen borg'],
        dhl='Naar Emmen en de dorpen eromheen sturen we de set met DHL, gratis vanaf €150 (anders €16 per pakket).',
        afhalen='Gratis ophalen kan in Fochteloo: vanaf 16:00 de dag voor je feest, inleveren tot 16:00 de dag erna.',
        lev_lead=f'Silent disco versturen we met DHL. Met grotere producten erbij bezorgen we in de gemeente Emmen zelf. {ZONE}',
        final='Bestel je koptelefoons online; ze komen met DHL naar Emmen.',
        b2b='Een bruiloft, schoolfeest of bedrijfsavond in Emmen? Vertel wat je nodig hebt; binnen één werkdag heb je een vaste prijs.'),
    'silent-disco-huren-friesland': dict(
        lead='Koptelefoons per stuk of alles-in-één per persoon: jij kiest.',
        checks=['Tot 3 kanalen', 'Zender los of in de bundel', 'Gratis ophalen in Fochteloo', 'Geen borg']),
}
for _p in PAGES:
    v = VAR.get(_p['slug'])
    if not v:
        continue
    _p['products'] = {**_p['products'], 'lead': v['lead'], 'checks': v['checks']}
    if 'dhl' in v:
        items = [dict(i) for i in _p['levering']['items']]
        items[0]['p'] = v['dhl']; items[1]['p'] = v['afhalen']
        _p['levering'] = {**_p['levering'], 'items': items, 'lead': v['lev_lead']}
        _p['final'] = {**_p['final'], 'p': v['final']}
        _p['b2b'] = {**_p['b2b'], 'p': v['b2b']}
