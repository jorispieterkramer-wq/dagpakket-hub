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


MCP = 'https://staging.dagpakketverhuur.nl/wp-json/mcp/mcp-adapter-default-server'
_sid = None


def mcp(ability, params):
    """Voert een WordPress-ability uit via de MCP-adapter van de site."""
    global _sid
    hdr = ['-H', 'Accept: application/json, text/event-stream']
    if _sid is None:
        init = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'deploy', 'version': '1'}}})
        r = subprocess.run(['curl', '-sS', '-D', '-', '-o', '/dev/null', '-X', 'POST', MCP, *hdr,
                            '-H', 'Content-Type: application/json', '--data-binary', '@-'],
                           input=init.encode(), capture_output=True)
        _sid = [l.split(':', 1)[1].strip() for l in r.stdout.decode().splitlines()
                if l.lower().startswith('mcp-session-id')][0]
    call = json.dumps({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {
        'name': 'mcp-adapter-execute-ability', 'arguments': {'ability_name': ability, 'parameters': params}}})
    res = curl('-X', 'POST', MCP, *hdr, '-H', f'Mcp-Session-Id: {_sid}', data=call)
    assert not res.get('error') and not res.get('result', {}).get('isError'), res
    return res


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

    # Elementor serveert anders zijn element-cache (oude HTML). Een document-save
    # via de Elementor-MCP met de bestaande pagina-instellingen leegt die cache;
    # de instellingen gaan volledig mee, zodat er niets wegvalt.
    settings = page['meta']['_elementor_page_settings'] or {}
    mcp('elementor/update-page-settings', {'post_id': pid, 'settings': settings})
    after = curl(API + f'{pid}?context=edit&_fields=meta,content')
    assert after['meta']['_elementor_page_settings'] == settings, 'pagina-instellingen gewijzigd'
    print(slug, 'render nieuw' if 'dpv-rg-host' in after['content']['rendered'] else 'RENDER NOG OUD')
