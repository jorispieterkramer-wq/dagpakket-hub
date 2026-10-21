"""Fase 4d — sitewide correcties in bestaande (niet herbouwde) kf-page-widgets."""
import re
ZONE = 'Het tarief en de gratis-grens voor bezorgen hangen af van je zone. Bereken het met je postcode.'
RULES = [
    # WhatsApp: vast 085-nummer heeft geen WhatsApp
    (re.escape('https://wa.me/31852129150'), 'https://wa.me/31636161518'),
    # hero-pill
    (r'(✓|&#x2713;) Gratis v\.a\. (?:€|&#x20AC;)150', r'\1 Gratis afhalen in Fochteloo'),
    # feestverhuur: bezorgkosten-FAQ als geheel (anders blijft 'die drempel' hangen)
    (re.escape('Gratis bezorging in Noord-Nederland vanaf €150 besteding. Bij bestellingen onder die drempel rekenen we een kleine '
               'bezorgvergoeding. Buiten Noord-Nederland betaal je DHL-verzendkosten. Check de transportpagina voor het exacte tarief '
               'op basis van jouw postcode.'),
     'Eigen bezorging in Noord-Nederland gaat per zone: het tarief en de gratis-grens hangen af van je zone. Bereken het met je '
     'postcode op de <a href="/contact/">contactpagina</a>. Buiten Noord-Nederland versturen we kleinere producten met DHL: €16 per '
     'pakket, gratis vanaf €150.'),
    # FAQ provincie: 'Ja, wij bezorgen gratis in X en omgeving bij een besteding vanaf €150.'
    (r'Ja, wij bezorgen gratis in ([^<.]+?) en omgeving bij een besteding vanaf €150\.',
     r'Ja, wij bezorgen in \1 en omgeving. Het tarief en de gratis-grens hangen af van je zone.'),
    # FAQ-vraag zonder 'gratis'
    (r'(<button class="kf-faq-q">Bezorgen jullie[^<?]*?) gratis( [^<?]*?\?)', r'\1\2'),
    # body-zinnen
    (r'zonder borg en met gratis bezorging vanaf €150\.', 'zonder borg. ' + ZONE.replace('Bereken het met je postcode.', '').strip()),
    (r'Gratis bezorging (?:in [^.<]+? )?vanaf €150 besteding\.', ZONE),
    # niet-bestaande transportpagina
    (re.escape('Check de transportpagina voor het exacte tarief op basis van jouw postcode.'),
     'Bereken het exacte tarief met je postcode op de <a href="/contact/">contactpagina</a>.'),
    # interne links naar 301 → eind-URL
    (re.escape('href="/silent-disco-huren/"'), 'href="/silent-disco-verhuur/"'),
    (re.escape('href="/product-category/tenten-verwarming-huren/stretchtenten-huren/"'),
     'href="/product-category/tenten-verwarming-huren/tenten-verwarming-stretchtenten-huren/"'),
    (re.escape('href="/product-category/tenten-verwarming-huren/heaters-huren/"'),
     'href="/product-category/tenten-verwarming-huren/tenten-verwarming-verwarming-huren/"'),
    (re.escape('href="/statafel-huren/"'), 'href="/product/statafel-huren/"'),
    (re.escape('href="/product-category/activiteiten-huren/"'), 'href="/product-category/activiteiten-attracties-huren/"'),
]


def apply(html):
    counts = []
    for pat, rep in RULES:
        html, n = re.subn(pat, rep, html)
        counts.append(n)
    return html, counts


def leftovers(html):
    t = re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>|<script.*?</script>', '', html, flags=re.S))
    return {'wa852': html.count('31852129150'),
            'claims': re.findall(r'[^.]{0,40}gratis[^.]{0,40}(?:€|&#x20AC;)\s?150[^.]{0,20}', t, re.I)}
