"""Fase 4e — productbeschrijvingen (alleen live; editor op staging mag geen producten bewerken)."""
import json, os
import wp

BIOS = (
    '<p>Buitenbioscoop huren voor een filmavond, tuinfeest of sportwedstrijd? Met deze set zet je in je eigen tuin of op locatie '
    'een complete bioscoop neer: een Full HD beamer, een groot opblaasbaar projectiescherm en een Fire TV Stick om direct je film '
    'of wedstrijd te starten.</p>\n'
    '<h2>Thuisbioscoop huren voor een filmavond</h2>\n'
    '<p>Stel je liever zelf iets samen? Huur dan los een <a href="/product/beamer-huren/">beamer</a> of een '
    '<a href="/product/opblaasbaar-projectiescherm-huren/">opblaasbaar projectiescherm</a>. Maak de avond compleet met een '
    '<a href="/product/popcornmachine-huren/">popcornmachine</a>.</p>\n'
    '<p>Hoort de filmavond bij een bruiloft of jubileum? Laat gasten dan een bericht inspreken in het '
    '<a href="/product/audio-gastenboek-huren/">audio gastenboek</a>.</p>\n'
    '<p>Je huurt zonder borg en haalt de set gratis af in Fochteloo. Laat je hem bezorgen, dan hangen het tarief en de '
    'gratis-grens af van je zone. Bereken het met je postcode.</p>'
)
EDITS = {
    47108: [('<a href="/product-category/activiteiten-huren/">', '<a href="/product-category/activiteiten-attracties-huren/">', 1)],
    47127: [('of <a href="https://dagpakketverhuur.nl/product/silent-disco-huren/">Silent disco</a>.</p>',
             ', <a href="https://dagpakketverhuur.nl/product/silent-disco-huren/">Silent disco</a> of een '
             '<a href="/product/buitenbioscoop-huren/">buitenbioscoop</a>.</p>', 1)],
    47130: [(None, BIOS, None)],  # beschrijving was leeg
}
D = os.path.join(wp.REPO, 'backups/2026-10-21/fase4e/live')

if __name__ == '__main__':
    os.makedirs(D, exist_ok=True)
    for pid, pairs in EDITS.items():
        pr = wp.api('live', f'/wc/v3/products/{pid}')
        f = f'{D}/product-{pid}.json'
        if not os.path.exists(f):
            json.dump(pr, open(f, 'w'), ensure_ascii=False)
        desc = pr['description']
        for old, new, n in pairs:
            if old is None:
                assert desc.strip() == '', pid
                desc = new
            else:
                assert desc.count(old) == n, (pid, old, desc.count(old))
                desc = desc.replace(old, new)
        r = wp.api('live', f'/wc/v3/products/{pid}', method='PUT', data=json.dumps({'description': desc}))
        assert r['price'] == pr['price'] and r['slug'] == pr['slug'] and r['status'] == pr['status']
        print(pid, r['slug'], 'opgeslagen', os.path.relpath(f, wp.REPO))
