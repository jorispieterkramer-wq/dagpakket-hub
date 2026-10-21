"""Fase 4e — clusterlinks in bestaande pagina's: python3 fase4e_pages.py <host>"""
import sys, wp

HUB_OLD = '<span class="dpv-card-link">Kinderfeestje regelen →</span></a>'
# gelblaster-link als losse regel onder het gelegenheden-grid (kaarten zijn zelf al <a>)
EDITS = {
    'lasergame-huren': [('<div class="dpv-head"><h2>Voor elke gelegenheid</h2></div>',
                         '<div class="dpv-head"><h2>Voor elke gelegenheid</h2><p>Liever spelen met waterballetjes? '
                         'Bekijk ook <a href="/product/gelblaster-huren/">gelblaster huren</a>.</p></div>', 1)],
    'zakelijk': [('Alle categorieën →</a>\n    </div>\n    <div class="cats">',
                  'Alle categorieën →</a>\n    </div>\n    <p style="margin:-8px 0 18px">Liever binnen met je team? '
                  'Bekijk ook <a href="/product/pubquiz-huren/">pubquiz huren</a>.</p>\n    <div class="cats">', 1)],
}

PHASE = 'fase4e'
if __name__ == '__main__':
    host = sys.argv[1]
    PHASE = 'fase4e-b' if '--b' in sys.argv else 'fase4e'
    sys.argv = [a for a in sys.argv if a != '--b']
    for slug, pairs in EDITS.items():
        pid = wp.api(host, f'/wp/v2/pages?slug={slug}&_fields=id')[0]['id']
        if len(sys.argv) > 2 and slug not in sys.argv[2:]:
            continue
        b, rep = wp.replace_in_widgets(host, pid, PHASE, pairs)
        wp.clear_cache(host, pid)
        q = wp.qa(host, f'/{slug}/', check_links=False)
        h, _ = wp.fetch_page(host, f'/{slug}/')
        full = h + ''.join(wp._decoded_scripts(h))
        print(slug, pid, b, rep, q['status'], q['h1'], q['wa'], 'link-ok' if pairs[0][1].split('href="')[1].split('"')[0] in full else 'LINK MIST')
