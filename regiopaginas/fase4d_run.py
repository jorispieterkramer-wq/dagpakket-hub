"""Fase 4d runner: python3 fase4d_run.py <host> [slug...]  — back-up → regels → opslaan → cache → QA."""
import json, os, sys
import wp, fase4d_rules as R

IDS = json.load(open('fase4d_ids.json'))
# tekstcorrecties ("noem nooit een aantal laserguns") — exact, met verwacht aantal
EXTRA = {
    'home': [('<h2>Begonnen met 12 lasergunsets, nooit meer gestopt</h2>', '<h2>Begonnen met lasergame, nooit meer gestopt</h2>', 1),
             ('begonnen met het verhuren van 12 lasergunsets aan', 'begonnen met het verhuren van lasergames aan', 1)],
    'zakelijk': [('begon ik met 12 lasergunsets;', 'begon ik met het verhuren van lasergames;', 1)],
}
PATHS = {'home': '/'}


def resolve(host, slug):
    if slug == 'home':
        return 3883
    r = wp.api(host, f'/wp/v2/pages?slug={slug}&_fields=id,link')
    assert len(r) == 1, (slug, r)
    return r[0]['id']


def run(host, slug):
    pid = resolve(host, slug)
    bpath = f'backups/2026-10-21/fase4d/{host}/{pid}'
    if os.path.exists(os.path.join(wp.REPO, bpath + '.json')):  # eerste back-up nooit overschrijven
        before = wp.get_page(host, pid)
    else:
        before, bpath = wp.backup(host, pid, 'fase4d')
    data = json.loads(before['meta']['_elementor_data'])
    ws = wp.html_widgets(data)
    total = [0] * len(R.RULES)
    for old, new, n in EXTRA.get(slug, []):
        c = sum(w['settings'].get('html', '').count(old) for w in ws)
        assert c == n, (slug, old, c)
        for w in ws:
            w['settings']['html'] = w['settings']['html'].replace(old, new)
    for w in ws:
        w['settings']['html'], cnt = R.apply(w['settings'].get('html', ''))
        total = [a + b for a, b in zip(total, cnt)]
    if sum(total) == 0 and slug not in EXTRA:
        return {'slug': slug, 'id': pid, 'changed': 0}
    wp.save_elementor(host, pid, before, data)
    try:
        wp.clear_cache(host, pid)
    except RuntimeError:  # 502 van de MCP-adapter: 60 s wachten, één keer opnieuw
        import time; time.sleep(60); wp.clear_cache(host, pid)
    left = R.leftovers(''.join(w['settings']['html'] for w in ws))
    q = wp.qa(host, PATHS.get(slug, f'/{slug}/'), check_links=False)
    return {'slug': slug, 'id': pid, 'backup': bpath, 'rules': total, 'left': left,
            'qa': {k: q[k] for k in ('status', 'h1', 'self_canonical', 'robots', 'wa', 'staging_in_live', 'blanket_claim', 'guns')}}


if __name__ == '__main__':
    host = sys.argv[1]
    for s in sys.argv[2:] or list(IDS) + ['home']:
        print(json.dumps(run(host, s), ensure_ascii=False), flush=True)
