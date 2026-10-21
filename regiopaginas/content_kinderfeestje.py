"""
Fase 4c — Kinderfeestje-cluster (A hub, B provincie, C stad).

Feiten (bron: productpagina's, /contact/):
- Lasergame vanaf 6 jaar; Compact = 3 balken levens, kleiner en voordeliger.
- Suikerspin- en popcornmachine incl. ingrediënten; aansluiten op het stopcontact, laten opwarmen.
- Springkussens (o.a. Jungle, Unicorn) en gelblaster bestaan als product; geen leeftijden genoemd
  op de productpagina's, dus hier ook niet.
- Lasergame en gelblaster kunnen met DHL (kleinere producten); springkussens en machines
  eigen bezorging per zone; gratis afhalen in Fochteloo.
- Review: echte kinderfeestje-review (Marjolijn, homepage).
- Links naar regiopagina's van andere clusters alleen als die pagina bestaat.
"""
import os as _os
from build import url, TEL
from reviews import MARJOLIJN

LIVE = _os.environ.get('DPV_HOST', 'live') == 'live'
U = url('/wp-content/uploads')
IMG = {
    'lasergame': (U + '/2026/02/Ontwerp-zonder-titel-_1__11zon.webp', 'Kinderen met laserguns in de tuin tijdens een kinderfeestje'),
    'silent': (U + '/2026/02/unnamed-1_11zon.webp', 'Kinderen dansen met silent disco koptelefoons onder een feesttent'),
    'gelblaster': (U + '/2025/12/Social-media-Kit-Dagpakketverhuur-4.png', 'Kinderen spelen met gelblasters op een kinderfeestje'),
    'tuin': (U + '/2026/02/Ontwerp-zonder-titel_11zon.webp', 'Kinderen spelen lasergame tussen de struiken in de tuin'),
    'heg': (U + '/2025/09/IMG_395C64FA2DE4-1.jpg', 'Kind met lasergun sluipt langs een heg in de tuin'),
    'tent': (U + '/2026/08/Gemini_Generated_Image_afvuyfafvuyfafvu_11zon.webp', 'Tuinfeest met tenten en lichtjes'),
}
CAT_ACT = url('/product-category/activiteiten-attracties-huren/' if LIVE else '/product-category/activiteiten-huren/')
CAT_SPRING = url('/product-category/activiteiten-attracties-huren/attracties-springkussens-huren/' if LIVE else '/product-category/springkussens-huren/')
CAT_FUN = url('/product-category/keuken-huren/keuken-funfood-huren/' if LIVE else '/product-category/funfood-huren/')
CAT_TENT = url('/product-category/tenten-verwarming-huren/')
P = {
    'compact': url('/product/lasergame-compacte-huren/'), 'spring': url('/product/springkussen-jungle-huren/'),
    'unicorn': url('/product/springkussen-unicorn-huren/'), 'suiker': url('/product/suikerspinmachine-huren/'),
    'popcorn': url('/product/popcornmachine-huren/'), 'gel': url('/product/gelblaster-huren/'),
    'bios': url('/product/buitenbioscoop-huren/'),
}
BLOG = url('/het-ultieme-kinderfeestje/')
KARAOKE = url('/karaoke-set-kinderfeestje/')
HUB = url('/kinderfeestje/')
CONTACT = url('/contact/')
ALTS = {47238: 'Lasergame Compact huren voor een kinderfeestje', 50597: 'Springkussen Jungle huren',
        47220: 'Suikerspinmachine huren', 47217: 'Popcornmachine huren', 47244: 'Gelblaster huren',
        47130: 'Buitenbioscoop huren'}
HUB_CARDS = {'product_ids': [47238, 50597, 47220, 47244, 47217, 47130], 'prod_cols': 3, 'cat_url': CAT_ACT, 'product_alts': ALTS}
REG_CARDS = {'product_ids': [47238, 50597, 47220, 47244], 'prod_cols': 4, 'cat_url': CAT_ACT,
             'product_alts': {k: ALTS[k] for k in (47238, 50597, 47220, 47244)}}

ZONE = 'Het tarief en de gratis-grens hangen af van je zone. Bereken het met je postcode.'
CALC = f'<a href="{CONTACT}">Bereken het met je postcode</a>'
FAQ_INTRO = 'Bel ons binnen openingstijden. Spoed buiten openingstijden? Stuur een WhatsApp.'
REVIEW = {'h2': 'Wat ouders zeggen', 'data': MARJOLIJN}
TRUST = [
    ('shield', 'Geen borg', 'Je betaalt alleen de huurprijs'),
    ('pin', 'Gratis afhalen in Fochteloo', 'Vanaf 16:00 de dag voor het feest'),
    ('truck', 'Bezorging in Noord-Nederland', 'Tarief per zone, check je postcode'),
    ('calendar', 'Lasergame en gelblaster per DHL', 'Door heel Nederland'),
]

# Bestaande regiopagina's per cluster (gecontroleerd op 200).
LG = {'friesland', 'groningen', 'drenthe', 'leeuwarden', 'drachten', 'assen', 'emmen'}
PT = {'friesland', 'groningen', 'drenthe', 'leeuwarden', 'heerenveen', 'assen', 'emmen'}
SD = {'friesland', 'groningen', 'drenthe', 'leeuwarden', 'assen', 'emmen'}


def cluster_links(slug, naam):
    items = []
    if slug in LG:
        items.append((f'Lasergame in {naam}', 'Compact of XL, vanaf 6 jaar', url(f'/lasergame-huren-{slug}/')))
    if slug in PT:
        items.append((f'Partytent in {naam}', 'Een droge plek voor taart en limonade', url(f'/partytent-huren-{slug}/')))
    if slug in SD:
        items.append((f'Silent disco in {naam}', 'Kinderdisco zonder lawaai', url(f'/silent-disco-huren-{slug}/')))
    return {'h2': f'Meer voor je feest in {naam}', 'lead': 'Per activiteit een eigen pagina met bezorging en vragen uit de buurt.',
            'items': items, 'cols': 'dpv-g3' if len(items) == 3 else 'dpv-g2'}


PAKKETTEN = [
    {'tag': 'Actief buitenfeest', 'h3': 'Lasergame Compact + suikerspin',
     'p': f'Rennen en verstoppen met <a href="{P["compact"]}">Lasergame Compact</a> (vanaf 6 jaar), daarna suikerspinnen draaien met de '
          f'<a href="{P["suiker"]}">suikerspinmachine</a>. De machine gaat op het stopcontact en draait na het opwarmen.'},
    {'tag': 'Springen en snoepen', 'h3': 'Springkussen + popcornmachine',
     'p': f'Een <a href="{P["spring"]}">springkussen Jungle</a> of <a href="{P["unicorn"]}">Unicorn</a> voor in de tuin, en verse popcorn uit de '
          f'<a href="{P["popcorn"]}">popcornmachine</a> (inclusief ingrediënten).'},
    {'tag': 'Filmavond', 'h3': 'Buitenbioscoop + popcorn',
     'p': f'Na het spelen een film in de tuin met de <a href="{P["bios"]}">buitenbioscoop</a> en een bak popcorn erbij.', 'soft': True},
]

PAGES = []

# ================================================================== A — HUB
PAGES.append({
    **HUB_CARDS, 'template': 'A', 'id': 50414, 'slug': 'kinderfeestje', 'naam': 'KINDERFEESTJE (HUB)', 'plaats': 'Noord-Nederland',
    'seo_title': 'Kinderfeestje thuis regelen | Activiteiten huren | Dagpakketverhuur',
    'meta': 'Kinderfeestje thuis? Huur lasergame, een springkussen, gelblaster of suikerspinmachine. Geen borg, gratis afhalen in Fochteloo.',
    'hero': {'img': IMG['lasergame'][0], 'alt': IMG['lasergame'][1], 'pos': '50% 35%', 'eyebrow': 'Kinderfeestje · thuis of op locatie',
             'h1': 'Kinderfeestje thuis,<br>wij leveren de actie', 'cta': 'Bekijk activiteiten',
             'sub': 'Lasergame, een springkussen, gelblasters of een suikerspinmachine: alles voor een feest in je eigen tuin.'},
    'trust': TRUST,
    'products': {'h2': 'Populair voor kinderfeestjes', 'cat_link': CAT_ACT, 'cat_label': 'Alle activiteiten', 'wide': True,
                 'lead': 'Kies één activiteit, of combineer er een paar voor een hele middag.',
                 'checks': ['Lasergame vanaf 6 jaar', 'Machines inclusief ingrediënten', 'Alles los te combineren in één bestelling', 'Geen borg'],
                 'info_h3': 'Goed om te weten', 'info_link': (BLOG, 'Tips voor het ultieme kinderfeestje')},
    'keuze': {'h2': 'Voorbeeldpakketten', 'lead': 'Drie combinaties met bestaande producten. De prijzen zie je per product.', 'items': PAKKETTEN},
    'gelegenheden': {'h2': 'Kies wat bij je feest past', 'items': [
        {'icon': 'bolt', 'h3': 'Activiteiten', 'p': 'Lasergame, gelblaster en archery tag voor kinderen die willen rennen.', 'link': (CAT_ACT, 'Alle activiteiten')},
        {'icon': 'sun', 'h3': 'Springkussens', 'p': 'Jungle, Unicorn, Disco of Voetbal, ook met glijbaan.', 'link': (CAT_SPRING, 'Alle springkussens')},
        {'icon': 'gift', 'h3': 'Funfood', 'p': 'Suikerspin en popcorn maak je zelf met de machines.', 'link': (CAT_FUN, 'Alle funfood')},
        {'icon': 'cake', 'h3': 'Tenten', 'p': 'Een droge plek voor taart en limonade.', 'link': (CAT_TENT, 'Tenten en verwarming')}]},
    'stappen': {'h2': 'Zo werkt huren', 'items': [
        ('Kies je activiteiten', 'Zet alles in één winkelwagen; bezorgkosten rekenen we één keer per bestelling.'),
        ('Kies je datum', 'Bij het afrekenen kies je de feestdatum en bezorgen, verzenden of zelf ophalen.'),
        ('Feest!', 'Uitleg zit erbij. De machines gaan op het stopcontact.'),
        ('Retour', 'Compleet en droog terug tot 16:00 de dag na het feest.')]},
    'regio': {'h2': 'Kinderfeestje in jouw provincie', 'lead': 'Per provincie: bezorging, afhalen en activiteiten in de buurt.',
              'items': [('Friesland', 'Kinderfeestje in Friesland', url('/kinderfeestje-friesland/')),
                        ('Drenthe', 'Kinderfeestje in Drenthe', url('/kinderfeestje-drenthe/')),
                        ('Groningen', 'Kinderfeestje in Groningen', url('/kinderfeestje-groningen/'))]},
    'b2b': {'kicker': 'Scholen en verenigingen', 'h2': 'Sportdag, schoolfeest of clubdag',
            'p': 'Organiseer je een feest voor een hele klas of club? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
            'checks': ['Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen', 'Betalen op factuur, met je eigen referentie'],
            'img': IMG['gelblaster'][0], 'alt': IMG['gelblaster'][1]},
    'review': REVIEW,
    'faq': {'h2': 'Veelgestelde vragen', 'intro': FAQ_INTRO, 'items': [
        ('Vanaf welke leeftijd is lasergame geschikt?', 'Vanaf 6 jaar. Voor jongere kinderen is een springkussen een goede keuze.'),
        ('Kan ik meerdere activiteiten combineren?', 'Ja, alles is los te combineren. Bezorgkosten rekenen we één keer voor de hele bestelling.'),
        ('Wat kost bezorgen?', f'Grotere producten zoals springkussens bezorgen we zelf. {ZONE.split(". ")[0]}. {CALC}. Lasergame en gelblaster kunnen ook met DHL (€16, gratis vanaf €150).'),
        ('Moet ik een machine schoonmaken?', 'Nee. Lever alles compleet en droog in; even afvegen is genoeg, schoonmaken doen wij.'),
        ('Hebben jullie tips voor het feest?', f'Lees onze blogs over <a href="{BLOG}">het ultieme kinderfeestje</a> en een <a href="{KARAOKE}">karaokeset op een kinderfeestje</a>.'),
        ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')]},
    'final': {'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'cta': 'Bekijk activiteiten',
              'h2': 'Klaar voor het leukste feestje?', 'p': 'Kies je activiteiten en je datum. Geen borg, en afhalen in Fochteloo is gratis.',
              'links': [('Lasergame Compact', P['compact']), ('Springkussen Jungle', P['spring']), ('Suikerspinmachine', P['suiker'])]},
})


def regio_common(slug, naam):
    return {**REG_CARDS, 'trust': TRUST, 'review': REVIEW, 'extra_places': cluster_links(slug, naam),
            'products': {'h2': 'Populaire activiteiten', 'cat_link': CAT_ACT, 'cat_label': 'Alle activiteiten', 'wide': True,
                         'info_h3': 'Goed om te weten', 'info_link': (HUB, 'Voorbeeldpakketten en tips')}}


V = {  # per pagina eigen formuleringen (overlap ≤0,35)
    'friesland': dict(lead='Lasergame, springkussen, suikerspin of gelblaster: kies er één of combineer.',
                      checks=['Lasergame vanaf 6 jaar', 'Springkussens bezorgen we zelf', 'Gratis ophalen in Fochteloo', 'Geen borg']),
    'groningen': dict(lead='Vier favorieten voor een feest thuis, los of samen te huren.',
                      checks=['Machines met ingrediënten', 'Lasergame en gelblaster ook per DHL', 'Eén bestelling, één keer bezorgkosten', 'Geen borg']),
    'drenthe': dict(lead='Van springen tot suikerspinnen: alles voor een middag in de tuin.',
                    checks=['Lasergame vanaf 6 jaar', 'Springkussen met of zonder glijbaan', 'Afhalen in Fochteloo is gratis', 'Geen borg']),
    'leeuwarden': dict(lead='Kies wat past bij de leeftijd en de ruimte die je hebt.',
                       checks=['Lasergame vanaf 6 jaar', 'Suikerspin op het stopcontact', 'Bezorging per zone', 'Geen borg']),
    'heerenveen': dict(lead='Springkussen, lasergame, gelblaster of suikerspin voor een feest in Heerenveen.',
                       checks=['Springkussens zelf bezorgd', 'Machines inclusief ingrediënten', 'Gratis afhalen in Fochteloo', 'Geen borg']),
    'drachten': dict(lead='Actief buiten of lekker snoepen: combineer wat je wilt.',
                     checks=['Lasergame vanaf 6 jaar', 'Alles in één bestelling', 'Lasergame ook per DHL', 'Geen borg']),
    'assen': dict(lead='Vier activiteiten die het altijd goed doen op een kinderfeestje.',
                  checks=['Springkussen Jungle of Unicorn', 'Suikerspin met ingrediënten', 'Bezorgd of zelf opgehaald', 'Geen borg']),
    'emmen': dict(lead='Kies een activiteit voor de tuin, of maak er een hele middag van.',
                  checks=['Lasergame vanaf 6 jaar', 'Springkussens zelf bezorgd', 'Machines op het stopcontact', 'Geen borg']),
}


def lev(gebied, v=0):
    eigen = [f'Springkussens en machines bezorgen we zelf in {gebied}, op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
             f'In {gebied} brengen we grotere spullen zelf en halen ze na het feest weer op. {ZONE}',
             f'Wij rijden zelf in {gebied} met springkussens en funfoodmachines. {ZONE}'][v % 3]
    afh = ['Ophalen op Verlaat 3 in Fochteloo is gratis: vanaf 16:00 de dag voor het feest, terug tot 16:00 de dag erna.',
           'Zelf rijden kan altijd: in Fochteloo haal je gratis op vanaf 16:00 de dag ervoor; inleveren tot 16:00 de dag erna.',
           'Gratis afhalen in Fochteloo, vanaf 16:00 de dag voor het feest. Breng alles terug tot 16:00 de dag erna.'][v % 3]
    dhl = ['Lasergame en gelblaster passen in een pakket: met DHL voor €16, gratis vanaf €150.',
           'Alleen lasergame of gelblaster? Die versturen we met DHL door heel Nederland, gratis vanaf €150.',
           'Kleinere activiteiten zoals lasergame gaan met DHL: €16 per pakket, gratis vanaf €150.'][v % 3]
    return [{'icon': 'truck', 'h3': 'Wij bezorgen en halen op', 'p': eigen, 'link': (CONTACT, 'Bereken je bezorgkosten')},
            {'icon': 'pin', 'h3': 'Gratis afhalen in Fochteloo', 'p': afh},
            {'icon': 'calendar', 'h3': 'Per DHL', 'p': dhl}]


def provincie(pid, slug, naam, hero, intro, toep, steden, faq, final_img, meta, v):
    base = regio_common(slug, naam)
    return {**base, 'template': 'B', 'id': pid, 'slug': f'kinderfeestje-{slug}', 'naam': f'KINDERFEESTJE {naam.upper()} (PROVINCIE)',
            'plaats': naam, 'seo_title': f'Kinderfeestje in {naam} | Dagpakketverhuur', 'meta': meta,
            'hero': {**hero, 'eyebrow': f'Kinderfeestje · {naam}', 'h1': f'Kinderfeestje in {naam}', 'cta': 'Bekijk activiteiten'},
            'intro': intro, 'products': {**base['products'], **V[slug]},
            'toepassingen': toep, 'steden': steden,
            'levering': {'h2': 'Bezorgen, afhalen of versturen', 'lead': 'Je kiest bij het afrekenen. Op zondag zijn we gesloten.', 'items': lev(naam, v)},
            'b2b': {'kicker': f'Scholen en clubs in {naam}', 'h2': 'Schoolfeest, sportdag of clubdag',
                    'p': f'Een feest voor een klas of club in {naam}? Vertel wat je nodig hebt en vraag een zakelijke prijs aan.',
                    'checks': ['Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen', 'Betalen op factuur'],
                    'img': IMG['silent'][0], 'alt': IMG['silent'][1]},
            'faq': {'h2': f'Vragen over een kinderfeestje in {naam}', 'intro': FAQ_INTRO, 'items': faq},
            'final': {'img': final_img[0], 'alt': final_img[1], 'cta': 'Bekijk activiteiten', 'h2': f'Kinderfeestje in {naam} regelen?',
                      'p': 'Kies je activiteiten en je datum. Geen borg, en afhalen in Fochteloo is gratis.',
                      'links': [('Alles over kinderfeestjes', HUB), ('Lasergame Compact', P['compact']), ('Springkussen Jungle', P['spring'])]}}


PAGES.append(provincie(
    50437, 'friesland', 'Friesland',
    {'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'pos': '50% 40%', 'sub': 'Haal alles gratis op in Fochteloo, of laat het bezorgen in heel Friesland.'},
    {'kicker': 'Kinderfeestje in Friesland', 'h2': 'Vanuit Fochteloo naar jouw tuin',
     'p': ['Onze activiteiten staan klaar in Fochteloo, in het zuidoosten van Friesland. Ophalen is gratis, vanaf 16:00 de dag voor het feest.',
           f'Liever thuisbezorgd? In Friesland brengen we springkussens, machines en activiteiten zelf. {ZONE}']},
    {'h2': 'Favoriet in Friesland', 'items': [
        {'icon': 'bolt', 'h3': 'Lasergame in de tuin', 'p': 'Vanaf 6 jaar. Struiken en een schuurtje zijn al een speelveld.', 'link': (P['compact'], 'Lasergame Compact')},
        {'icon': 'sun', 'h3': 'Springkussen', 'p': 'Jungle of Unicorn, met of zonder glijbaan.', 'link': (CAT_SPRING, 'Springkussens')},
        {'icon': 'gift', 'h3': 'Suikerspin of popcorn', 'p': 'Machines inclusief ingrediënten.', 'link': (CAT_FUN, 'Funfood')},
        {'icon': 'users', 'h3': 'Gelblaster', 'p': 'Spannend spel voor oudere kinderen.', 'link': (P['gel'], 'Gelblaster')}]},
    {'h2': 'Kinderfeestje in Friese steden', 'lead': 'Voor deze plaatsen hebben we een eigen pagina.',
     'items': [('Leeuwarden', 'Kinderfeestje in Leeuwarden', url('/kinderfeestje-leeuwarden/')),
               ('Heerenveen', 'Kinderfeestje in Heerenveen', url('/kinderfeestje-heerenveen/')),
               ('Drachten', 'Kinderfeestje in Drachten', url('/kinderfeestje-drachten/'))]},
    [('Waar haal ik alles op?', 'Op Verlaat 3 in Fochteloo, vanaf 16:00 de dag voor het feest. Ophalen is gratis.'),
     ('Bezorgen jullie in heel Friesland?', f'Ja. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Vanaf welke leeftijd is lasergame geschikt?', 'Vanaf 6 jaar.'),
     ('Feest op zondag?', 'Dan regelen we ophalen en terugbrengen op zaterdag of maandag, zonder extra huurdag.')],
    IMG['heg'], 'Kinderfeestje in Friesland? Huur lasergame, een springkussen of suikerspinmachine. Gratis afhalen in Fochteloo of bezorgd. Geen borg.', 0))

PAGES.append(provincie(
    50448, 'groningen', 'Groningen',
    {'img': IMG['gelblaster'][0], 'alt': IMG['gelblaster'][1], 'pos': '50% 40%', 'sub': 'Activiteiten voor een feest thuis in de provincie Groningen, bezorgd en weer opgehaald.'},
    {'kicker': 'Kinderfeestje in Groningen', 'h2': 'Een feest thuis in Groningen',
     'p': [f'De provincie Groningen valt binnen ons bezorggebied. Springkussens en machines brengen we zelf. {ZONE}',
           'Alleen lasergame of gelblaster? Die kunnen ook met DHL, gratis vanaf €150.']},
    {'h2': 'Favoriet in Groningen', 'items': [
        {'icon': 'users', 'h3': 'Gelblaster', 'p': 'Een spannend spel met waterballetjes voor de wat oudere kinderen.', 'link': (P['gel'], 'Gelblaster')},
        {'icon': 'bolt', 'h3': 'Lasergame', 'p': 'Vanaf 6 jaar, binnen en buiten te spelen.', 'link': (P['compact'], 'Lasergame Compact')},
        {'icon': 'sun', 'h3': 'Springkussen', 'p': 'Voor de jongsten, in de tuin.', 'link': (CAT_SPRING, 'Springkussens')},
        {'icon': 'gift', 'h3': 'Popcorn', 'p': 'Popcornmachine met ingrediënten.', 'link': (P['popcorn'], 'Popcornmachine')}]},
    None,
    [('Bezorgen jullie in de stad Groningen?', f'Ja, in de hele provincie. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan lasergame met de post?', 'Ja, met DHL: €16 per pakket, gratis vanaf €150. Het pakket is er één tot twee werkdagen voor de huurdatum.'),
     ('Moet ik vooraf betalen?', 'Ja, vóór de huurdatum. Scholen en verenigingen kunnen op factuur betalen.'),
     ('Betaal ik borg?', 'Nee, we vragen op dit moment geen borg.')],
    IMG['lasergame'], 'Kinderfeestje in Groningen? Lasergame, gelblaster, springkussen of popcornmachine, bezorgd en opgehaald. Geen borg.', 1))

PAGES.append(provincie(
    50443, 'drenthe', 'Drenthe',
    {'img': IMG['silent'][0], 'alt': IMG['silent'][1], 'pos': '50% 40%', 'sub': 'Van Assen tot Emmen: activiteiten voor een feest in je eigen tuin.'},
    {'kicker': 'Kinderfeestje in Drenthe', 'h2': 'Kinderfeestje in heel Drenthe',
     'p': [f'Drenthe valt binnen ons eigen bezorggebied. We brengen springkussens en machines op het gekozen tijdslot. {ZONE}',
           'Liever zelf ophalen? Dat kan gratis in Fochteloo, vanaf 16:00 de dag voor het feest.']},
    {'h2': 'Favoriet in Drenthe', 'items': [
        {'icon': 'sun', 'h3': 'Springkussen met glijbaan', 'p': 'Jungle of Unicorn met glijbaan voor in de tuin.', 'link': (CAT_SPRING, 'Springkussens')},
        {'icon': 'bolt', 'h3': 'Lasergame', 'p': 'Vanaf 6 jaar; korte, snelle rondes met Compact.', 'link': (P['compact'], 'Lasergame Compact')},
        {'icon': 'gift', 'h3': 'Suikerspin', 'p': 'Machine op het stopcontact, inclusief ingrediënten.', 'link': (P['suiker'], 'Suikerspinmachine')},
        {'icon': 'cake', 'h3': 'Partytent', 'p': 'Een droge plek voor de traktatie.', 'link': (url('/partytent-huren-drenthe/'), 'Partytent in Drenthe')}]},
    {'h2': 'Kinderfeestje in Drentse steden', 'lead': 'Voor deze plaatsen hebben we een eigen pagina.',
     'items': [('Assen', 'Kinderfeestje in Assen', url('/kinderfeestje-assen/')), ('Emmen', 'Kinderfeestje in Emmen', url('/kinderfeestje-emmen/'))]},
    [('Bezorgen jullie in heel Drenthe?', f'Ja. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Hoe werkt de suikerspinmachine?', 'Aansluiten op het stopcontact, laten opwarmen en de ingrediënten toevoegen.'),
     ('Kan ik meerdere activiteiten huren?', 'Ja, en bezorgkosten rekenen we één keer per bestelling.'),
     ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor de huurdatum.')],
    IMG['tuin'], 'Kinderfeestje in Drenthe? Wij bezorgen in Assen, Emmen en omgeving: springkussen, lasergame of suikerspin. Geen borg.', 2))


def stad(pid, slug, naam, prov, prov_slug, hero, intro, stappen, gel, plaatsen, faq, final_img, meta, v):
    base = regio_common(slug, naam)
    return {**base, 'template': 'C', 'id': pid, 'slug': f'kinderfeestje-{slug}', 'naam': f'KINDERFEESTJE {naam.upper()} (STAD)', 'plaats': naam,
            'seo_title': f'Kinderfeestje in {naam} | Dagpakketverhuur', 'meta': meta,
            'hero': {**hero, 'eyebrow': f'Kinderfeestje · {naam}', 'h1': f'Kinderfeestje in {naam}', 'cta': 'Bekijk activiteiten'},
            'intro': intro, 'products': {**base['products'], 'h2': f'Activiteiten voor een feest in {naam}', **V[slug]},
            'stappen': {'h2': f'Zo werkt huren in {naam}', 'items': stappen},
            'gelegenheden': {'h2': f'Wat kies je voor een kinderfeestje in {naam}?', 'items': gel},
            'b2b': {'kicker': f'Scholen en clubs in {naam}', 'h2': f'Ook voor scholen en verenigingen in {naam}',
                    'p': f'Een schoolfeest of clubdag in {naam}? Vraag een zakelijke prijs aan.',
                    'checks': ['Binnen één werkdag een vaste prijs, inclusief bezorgen en ophalen', 'Betalen op factuur'],
                    'img': IMG['silent'][0], 'alt': IMG['silent'][1]},
            'levering': {'h2': f'Levering in {naam} en omgeving', 'lead': f'We bezorgen in {naam} en de dorpen eromheen, onder meer in deze plaatsen. {ZONE}',
                         'plaatsen': plaatsen, 'items': lev(f'{naam} en omgeving', v)},
            'faq': {'h2': f'Vragen over een kinderfeestje in {naam}', 'intro': FAQ_INTRO, 'items': faq},
            'final': {'img': final_img[0], 'alt': final_img[1], 'cta': 'Bekijk activiteiten', 'h2': f'Kinderfeestje in {naam} regelen?',
                      'p': f'Kies je activiteiten en je datum, wij bezorgen in {naam}.',
                      'links': [(f'Kinderfeestje in {prov}', url(f'/kinderfeestje-{prov_slug}/')), ('Alles over kinderfeestjes', HUB),
                                ('Lasergame Compact', P['compact'])]}}


GEL_SPRING = {'icon': 'sun', 'h3': 'Springkussen', 'p': '', 'link': (CAT_SPRING, 'Springkussens')}

PAGES.append(stad(
    50453, 'leeuwarden', 'Leeuwarden', 'Friesland', 'friesland',
    {'img': IMG['lasergame'][0], 'alt': IMG['lasergame'][1], 'pos': '50% 35%', 'sub': 'Lasergame, springkussen of suikerspin, bezorgd in Leeuwarden en de dorpen eromheen.'},
    {'kicker': 'Kinderfeestje in Leeuwarden', 'h2': 'Kinderfeestje thuis in Leeuwarden',
     'p': [f'In Leeuwarden en omgeving brengen we springkussens, machines en activiteiten op het gekozen tijdslot. {ZONE}',
           'Kleine tuin? Lasergame werkt ook binnen in een grote ruimte, en een suikerspinmachine past op elke tafel.']},
    [('Activiteiten kiezen', 'Lasergame, springkussen, gelblaster of funfood.'), ('Datum en tijdslot', 'Kies bij het afrekenen.'),
     ('Wij brengen het', 'Eén tot twee dagen vooraf bevestigen we het moment.'), ('Wij halen op', 'Klaarzetten tot 16:00 de dag na het feest.')],
    [{'icon': 'bolt', 'h3': 'Lasergame', 'p': 'Vanaf 6 jaar, binnen of buiten.', 'link': (P['compact'], 'Lasergame Compact')},
     {**GEL_SPRING, 'p': 'Jungle of Unicorn voor de jongste gasten.'},
     {'icon': 'gift', 'h3': 'Suikerspin', 'p': 'Zelf suikerspinnen draaien.', 'link': (P['suiker'], 'Suikerspinmachine')}],
    ['Leeuwarden', 'Stiens', 'Grou', 'Goutum', 'Wirdum', 'Jirnsum'],
    [('Bezorgen jullie in Stiens of Grou?', f'Ja. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan lasergame binnen?', 'Ja, in een grote ruimte. Meubels zijn prima dekking.'),
     ('Wanneer hoor ik hoe laat jullie komen?', 'Eén tot twee dagen voor de huurdatum.'),
     ('Betaal ik borg?', 'Nee.')],
    IMG['tuin'], 'Kinderfeestje in Leeuwarden, Stiens of Grou? Lasergame, springkussen of suikerspinmachine, bezorgd en opgehaald. Geen borg.', 0))

PAGES.append(stad(
    50473, 'heerenveen', 'Heerenveen', 'Friesland', 'friesland',
    {'img': IMG['heg'][0], 'alt': IMG['heg'][1], 'pos': '50% 35%', 'sub': 'Activiteiten voor een feest in Heerenveen of de dorpen van de gemeente.'},
    {'kicker': 'Kinderfeestje in Heerenveen', 'h2': 'Kinderfeestje in Heerenveen en omgeving',
     'p': [f'In de gemeente Heerenveen bezorgen we springkussens, funfoodmachines en activiteiten zelf. {ZONE}',
           'Zelf ophalen kan ook, gratis in Fochteloo, vanaf 16:00 de dag voor het feest.']},
    [('Kiezen', 'Een springkussen, lasergame, gelblaster of suikerspin.'), ('Datum', 'Kies bij het afrekenen, met bezorgen of ophalen.'),
     ('Spelen', 'Uitleg zit erbij.'), ('Terug', 'Droog en compleet tot 16:00 de dag erna.')],
    [{**GEL_SPRING, 'p': 'Met of zonder glijbaan, voor in de tuin.'},
     {'icon': 'users', 'h3': 'Gelblaster', 'p': 'Voor kinderen die van spanning houden.', 'link': (P['gel'], 'Gelblaster')},
     {'icon': 'gift', 'h3': 'Popcorn', 'p': 'Verse popcorn uit de machine.', 'link': (P['popcorn'], 'Popcornmachine')}],
    ['Heerenveen', 'Akkrum', 'Oudehaske', 'Jubbega', 'Hoornsterzwaag', 'Oudeschoot'],
    [('Bezorgen jullie in Akkrum of Jubbega?', f'Ja, in de hele gemeente. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik zelf ophalen?', 'Ja, gratis in Fochteloo.'),
     ('Wat zit er bij de popcornmachine?', 'Ingrediënten; extra navulling kun je los bestellen.'),
     ('Betaal ik borg?', 'Nee.')],
    IMG['gelblaster'], 'Kinderfeestje in Heerenveen, Akkrum of Jubbega? Springkussen, gelblaster of popcornmachine, bezorgd of zelf opgehaald.', 1))

PAGES.append(stad(
    50468, 'drachten', 'Drachten', 'Friesland', 'friesland',
    {'img': IMG['tuin'][0], 'alt': IMG['tuin'][1], 'pos': '50% 40%', 'sub': 'Bezorgd in Drachten en Smallingerland, of gratis opgehaald in Fochteloo.'},
    {'kicker': 'Kinderfeestje in Drachten', 'h2': 'Kinderfeestje in Drachten en Smallingerland',
     'p': [f'Woon je in Drachten of een van de dorpen van Smallingerland? Dan bezorgen we zelf. {ZONE}',
           'Lasergame kan ook met DHL, gratis vanaf €150.']},
    [('Kies', 'Zet je activiteiten in de winkelwagen.'), ('Plan', 'Kies datum en bezorgen of ophalen.'),
     ('Speel', 'Lasergame staat binnen 5 minuten klaar.'), ('Lever in', 'Compleet tot 16:00 de dag na het feest.')],
    [{'icon': 'bolt', 'h3': 'Lasergame', 'p': 'Vanaf 6 jaar; snel speelklaar.', 'link': (P['compact'], 'Lasergame Compact')},
     {**GEL_SPRING, 'p': 'Een springkussen in de achtertuin.'},
     {'icon': 'gift', 'h3': 'Suikerspin', 'p': 'Machine met ingrediënten.', 'link': (P['suiker'], 'Suikerspinmachine')}],
    ['Drachten', 'Drachtstercompagnie', 'Opeinde', 'Rottevalle', 'Boornbergum'],
    [('Bezorgen jullie in Opeinde of Rottevalle?', f'Ja. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan lasergame per post?', 'Ja, met DHL, gratis vanaf €150.'),
     ('Moet ik iets schoonmaken?', 'Nee, even afvegen is genoeg.'),
     ('Betaal ik borg?', 'Nee.')],
    IMG['lasergame'], 'Kinderfeestje in Drachten, Opeinde of Rottevalle? Lasergame, springkussen of suikerspin, bezorgd in Smallingerland. Geen borg.', 2))

PAGES.append(stad(
    50458, 'assen', 'Assen', 'Drenthe', 'drenthe',
    {'img': IMG['silent'][0], 'alt': IMG['silent'][1], 'pos': '50% 40%', 'sub': 'Activiteiten voor een feest in Assen, bezorgd en weer opgehaald.'},
    {'kicker': 'Kinderfeestje in Assen', 'h2': 'Kinderfeestje thuis in Assen',
     'p': [f'In Assen en omgeving brengen we je activiteiten op het tijdslot dat je kiest. {ZONE}',
           'Combineer gerust: een springkussen voor de jongsten en lasergame voor de oudere kinderen.']},
    [('Kies activiteiten', 'Los of gecombineerd.'), ('Kies tijdslot', 'Bij het afrekenen.'),
     ('Bezorging in Assen', 'We komen op het gekozen moment.'), ('Ophalen', 'Klaarzetten tot 16:00 de dag erna.')],
    [{**GEL_SPRING, 'p': 'Unicorn of Jungle voor de jongste gasten.'},
     {'icon': 'bolt', 'h3': 'Lasergame', 'p': 'Vanaf 6 jaar.', 'link': (P['compact'], 'Lasergame Compact')},
     {'icon': 'gift', 'h3': 'Popcorn', 'p': 'Popcornmachine met ingrediënten.', 'link': (P['popcorn'], 'Popcornmachine')}],
    ['Assen', 'Loon', 'Witten', 'Rolde', 'Vries'],
    [('Bezorgen jullie in Rolde of Vries?', f'Ja. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Kan ik springkussen en lasergame combineren?', 'Ja, in één bestelling, met één keer bezorgkosten.'),
     ('Kan ik annuleren?', 'Kosteloos tot 72 uur voor de huurdatum.'),
     ('Betaal ik borg?', 'Nee.')],
    IMG['heg'], 'Kinderfeestje in Assen, Rolde of Vries? Springkussen, lasergame of popcornmachine, bezorgd en opgehaald. Geen borg.', 0))

PAGES.append(stad(
    50463, 'emmen', 'Emmen', 'Drenthe', 'drenthe',
    {'img': IMG['gelblaster'][0], 'alt': IMG['gelblaster'][1], 'pos': '50% 40%', 'sub': 'Activiteiten voor een feest in Emmen, Klazienaveen of Nieuw-Amsterdam.'},
    {'kicker': 'Kinderfeestje in Emmen', 'h2': 'Kinderfeestje in de gemeente Emmen',
     'p': [f'We bezorgen in de hele gemeente Emmen, op het tijdslot dat je bij het afrekenen kiest. {ZONE}',
           'Gelblaster en lasergame zijn favoriet bij oudere kinderen; voor de jongsten is er het springkussen.']},
    [('Kies', 'Gelblaster, lasergame, springkussen of funfood.'), ('Plan', 'Datum en tijdslot bij het afrekenen.'),
     ('Feest', 'Uitleg zit erbij.'), ('Ophalen', 'Klaarzetten tot 16:00 de dag na het feest.')],
    [{'icon': 'users', 'h3': 'Gelblaster', 'p': 'Spannend teamspel met waterballetjes.', 'link': (P['gel'], 'Gelblaster')},
     {**GEL_SPRING, 'p': 'Springen tot ze moe zijn.'},
     {'icon': 'gift', 'h3': 'Suikerspin', 'p': 'Zelf draaien, inclusief ingrediënten.', 'link': (P['suiker'], 'Suikerspinmachine')}],
    ['Emmen', 'Klazienaveen', 'Nieuw-Amsterdam', 'Erica', 'Schoonebeek', 'Emmer-Compascuum'],
    [('Bezorgen jullie ook in Klazienaveen?', f'Ja, in de hele gemeente Emmen. {ZONE.split(". ")[0]}. {CALC}.'),
     ('Wat is geschikt voor jonge kinderen?', 'Een springkussen. Lasergame is geschikt vanaf 6 jaar.'),
     ('Wanneer hoor ik hoe laat jullie komen?', 'Eén tot twee dagen voor de huurdatum.'),
     ('Betaal ik borg?', 'Nee.')],
    IMG['tuin'], 'Kinderfeestje in Emmen, Klazienaveen of Nieuw-Amsterdam? Gelblaster, springkussen of suikerspin, bezorgd en opgehaald. Geen borg.', 1))
