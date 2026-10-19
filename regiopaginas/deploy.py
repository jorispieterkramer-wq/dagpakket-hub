#!/usr/bin/env python3
"""
Zet een gegenereerde pagina op STAGING: vervangt alleen settings.html van de
bestaande HTML-widget in _elementor_data (container-id en -instellingen
blijven gelijk). Slug, status, template, canonical en noindex blijven
onaangeroerd. Gebruik: python3 deploy.py <slug> [<slug> ...]
Vereist dat de sessie geauthenticeerd is voor staging (network secret).
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
API = 'https://staging.dagpakketverhuur.nl/wp-json/wp/v2/pages/'


def curl(*args, data=None):
    cmd = ['curl', '-sS', *args]
    if data is not None:
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
    r = subprocess.run(cmd, input=data.encode() if data else None, capture_output=True)
    return json.loads(r.stdout.decode())


for slug in sys.argv[1:]:
    seo = json.load(open(os.path.join(ROOT, 'out', slug + '.seo.json')))
    html = open(os.path.join(ROOT, 'out', slug + '.html'), encoding='utf-8').read()
    pid = seo['id']
    page = curl(API + f'{pid}?context=edit&_fields=id,slug,meta')
    assert page['slug'] == slug, (page.get('slug'), slug)
    data = json.loads(page['meta']['_elementor_data'])
    assert len(data) == 1 and data[0]['elType'] == 'container', 'onverwachte opbouw'
    widgets = data[0]['elements']
    assert len(widgets) == 1 and widgets[0].get('widgetType') == 'html', 'onverwachte opbouw'
    widgets[0]['settings']['html'] = html
    body = json.dumps({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, ensure_ascii=False)
    res = curl('-X', 'POST', API + str(pid), data=body)
    new = json.loads(res['meta']['_elementor_data'])[0]['elements'][0]['settings']['html']
    print(slug, 'OK' if new == html else 'MISMATCH', res.get('modified'))
