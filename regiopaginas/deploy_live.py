#!/usr/bin/env python3
"""
Livegang van één regiopagina op https://dagpakketverhuur.nl.
Gebruik: python3 deploy_live.py <slug>      (één pagina per keer)

Stappen:
1. Back-up naar backups/live-<datum>/: volledige page-JSON (incl. post content),
   Elementor-JSON en Yoast title/meta.
2. Vervangt alleen settings.html van de bestaande HTML-widget in _elementor_data.
   Slug, status, template, pagina-instellingen, Yoast, canonical en robots blijven
   onaangeroerd.
3. Leegt de Elementor-cache (CSS en element-cache worden opnieuw opgebouwd);
   de paginacache van LiteSpeed wordt bij het bijwerken van de pagina geleegd.
4. Verifieert de live-URL: 200 zonder redirect, 1 H1, alleen wa.me/31636161518,
   geen 'staging', geen aantal laserguns, nieuwe inhoud zichtbaar.
"""
import datetime, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://dagpakketverhuur.nl'
API = SITE + '/wp-json'


def curl(*args, data=None, raw=False):
    cmd = ['curl', '-sS', *args]
    if data is not None:
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
    r = subprocess.run(cmd, input=data.encode() if data else None, capture_output=True)
    out = r.stdout.decode()
    return out if raw else json.loads(out)


def main(slug):
    seo = json.load(open(os.path.join(ROOT, 'out', slug + '.seo.json')))
    html = open(os.path.join(ROOT, 'out', slug + '.html'), encoding='utf-8').read()
    assert 'staging' not in html, 'staging-URL in widget'
    pid = seo['id']

    # 1. back-up
    page = curl(f'{API}/wp/v2/pages/{pid}?context=edit')
    assert page['slug'] == slug, (page.get('slug'), slug)
    bdir = os.path.join(ROOT, '..', 'backups', 'live-' + datetime.date.today().isoformat())
    os.makedirs(bdir, exist_ok=True)
    base = os.path.join(bdir, f'page-{pid}-{slug}')
    json.dump(page, open(base + '.json', 'w'), ensure_ascii=False, indent=1)
    open(base + '.content.html', 'w', encoding='utf-8').write(page['content']['raw'])
    data = json.loads(page['meta']['_elementor_data'])
    json.dump(data, open(base + '.elementor.json', 'w'), ensure_ascii=False, indent=1)
    yoast = curl(f'{API}/yoast/v1/bulk_editor/posts?content_type=page&include={pid}')
    json.dump(yoast, open(base + '.yoast.json', 'w'), ensure_ascii=False, indent=1)
    print('back-up:', os.path.relpath(bdir, os.path.join(ROOT, '..')) + f'/page-{pid}-{slug}.*')

    # 2. alleen het HTML-blok
    assert len(data) == 1 and data[0]['elType'] == 'container', 'onverwachte opbouw'
    widgets = data[0]['elements']
    assert len(widgets) == 1 and widgets[0].get('widgetType') == 'html', 'onverwachte opbouw'
    widgets[0]['settings']['html'] = html
    body = json.dumps({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, ensure_ascii=False)
    res = curl('-X', 'POST', f'{API}/wp/v2/pages/{pid}', data=body)
    new = json.loads(res['meta']['_elementor_data'])[0]['elements'][0]['settings']['html']
    assert new == html, 'opgeslagen HTML wijkt af'
    for k in ('slug', 'status', 'template'):
        assert res[k] == page[k], k
    assert res['meta']['_elementor_page_settings'] == page['meta']['_elementor_page_settings']
    print('opgeslagen:', res['modified'])

    # 3. cache
    r = curl('-X', 'DELETE', f'{API}/elementor/v1/cache', '-w', '\n%{http_code}', raw=True)
    print('elementor-cache geleegd:', r.strip().splitlines()[-1])

    # 4. verificatie
    out = curl('-D', '-', f'{SITE}/{slug}/?v={int(datetime.datetime.now().timestamp())}', raw=True)
    head, _, doc = out.partition('\r\n\r\n')
    while doc.startswith('HTTP/'):
        head, _, doc = doc.partition('\r\n\r\n')
    status = curl('-o', '/dev/null', '-w', '%{http_code}|%{redirect_url}', f'{SITE}/{slug}/', raw=True)
    tpl = doc[doc.find('id="dpv-rg-prods"'):doc.find('</template>', doc.find('id="dpv-rg-tpl"'))]
    text = re.sub(r'<[^>]+>', ' ', tpl)
    checks = {
        'HTTP 200 zonder redirect': status == '200|',
        'nieuwe inhoud': 'dpv-rg-host' in doc and 'kf-page' not in doc,
        'precies 1 H1': len(re.findall(r'<h1[\s>]', doc)) == 1,
        'WhatsApp alleen 31636161518': set(re.findall(r'wa\.me/\d+', doc)) == {'wa.me/31636161518'},
        "geen 'staging' in pagina-blok": 'staging' not in tpl,
        'geen aantal laserguns': not re.search(r'\b\d+\s*(?:laser)?guns?\b', text, re.I),
    }
    for k, v in checks.items():
        print(('  ✓ ' if v else '  ✗ ') + k)
    print('LiteSpeed:', re.findall(r'(?i)x-litespeed-cache[^\r\n]*', head))
    return all(checks.values())


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'één slug per keer'
    sys.exit(0 if main(sys.argv[1]) else 1)
