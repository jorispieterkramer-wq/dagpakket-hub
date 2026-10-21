"""
Gedeelde hulplaag voor staging en live (masteropdracht 21-10-2026).

- Hosting-firewall: max. 1 request tegelijk, ≥3 s pauze tussen requests;
  bij 000/429 één keer 60 s wachten en opnieuw (geen lus).
- Back-up per pagina vóór elke wijziging: page-JSON (incl. post_content, status),
  Elementor-JSON en Yoast title/meta.
- Alleen de HTML-widgets in _elementor_data worden aangepast; slug, status,
  template en pagina-instellingen worden na het opslaan gecontroleerd.
- Daarna Elementor-cache legen (CSS + element-cache); LiteSpeed leegt de
  paginacache van de bijgewerkte pagina zelf.
"""
import fcntl, json, os, re, subprocess, time

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
HOSTS = {'staging': 'https://staging.dagpakketverhuur.nl', 'live': 'https://dagpakketverhuur.nl'}
_STAMP = '/tmp/dpv-last-request'
GAP = 3.0


def _throttle():
    with open(_STAMP + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            last = float(open(_STAMP).read())
        except Exception:
            last = 0
        wait = GAP - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
        open(_STAMP, 'w').write(str(time.time()))


def request(url, method='GET', data=None, headers=(), want='json'):
    """want: 'json' | 'text' | 'status' (code|redirect) | 'head+text'"""
    for attempt in (1, 2):
        _throttle()
        cmd = ['curl', '-sS', '-X', method, '--max-time', '60']
        for h in headers:
            cmd += ['-H', h]
        if data is not None:
            cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
        if want == 'status':
            cmd += ['-o', '/dev/null', '-w', '%{http_code}|%{redirect_url}']
        else:
            cmd += ['-w', '\n__HTTP__%{http_code}', '-D', '-' if want == 'head+text' else '/dev/null']
        cmd.append(url)
        r = subprocess.run(cmd, input=data.encode() if data is not None else None, capture_output=True)
        out = r.stdout.decode('utf-8', 'replace')
        code = out.split('|')[0] if want == 'status' else out.rsplit('__HTTP__', 1)[-1].strip()
        if code in ('000', '429') and attempt == 1:
            time.sleep(60)
            continue
        break
    if want == 'status':
        return out
    body = out.rsplit('\n__HTTP__', 1)[0]
    if want == 'json':
        try:
            return json.loads(body)
        except Exception:
            raise RuntimeError(f'Geen JSON van {url} (HTTP {code}): {body[:300]}')
    return body, code


def api(host, path, **kw):
    return request(HOSTS[host] + '/wp-json' + path, **kw)


def get_page(host, pid):
    return api(host, f'/wp/v2/pages/{pid}?context=edit')


def get_post(host, pid, kind='pages'):
    return api(host, f'/wp/v2/{kind}/{pid}?context=edit')


def backup(host, pid, phase, kind='pages', date='2026-10-21'):
    """Back-up vóór wijziging. Geeft (post, pad-prefix) terug."""
    p = get_post(host, pid, kind)
    d = os.path.join(REPO, 'backups', date, phase, host)
    os.makedirs(d, exist_ok=True)
    base = os.path.join(d, f'{pid}')
    json.dump(p, open(base + '.json', 'w'), ensure_ascii=False, indent=1)
    open(base + '.content.html', 'w', encoding='utf-8').write((p.get('content') or {}).get('raw', ''))
    ed = (p.get('meta') or {}).get('_elementor_data') or '[]'
    json.dump(json.loads(ed), open(base + '.elementor.json', 'w'), ensure_ascii=False, indent=1)
    yo = {'yoast_head_json': {k: (p.get('yoast_head_json') or {}).get(k) for k in ('title', 'description', 'robots', 'canonical')},
          'status': p.get('status'), 'slug': p.get('slug'), 'link': p.get('link')}
    json.dump(yo, open(base + '.yoast.json', 'w'), ensure_ascii=False, indent=1)
    return p, os.path.relpath(base, REPO)


def html_widgets(data):
    """Alle HTML-widgets (recursief) in _elementor_data."""
    out = []

    def walk(els):
        for e in els:
            if e.get('widgetType') == 'html':
                out.append(e)
            walk(e.get('elements', []))
    walk(data)
    return out


def save_elementor(host, pid, before, data, kind='pages'):
    body = json.dumps({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, ensure_ascii=False)
    res = api(host, f'/wp/v2/{kind}/{pid}', method='POST', data=body)
    if 'meta' not in res:
        raise RuntimeError(f'Opslaan mislukt {pid}: {str(res)[:300]}')
    assert json.loads(res['meta']['_elementor_data']) == data, 'opgeslagen data wijkt af'
    for k in ('slug', 'status', 'link'):
        assert res.get(k) == before.get(k), k
    if 'template' in before:
        assert res.get('template') == before.get('template'), 'template'
    assert res['meta'].get('_elementor_page_settings') == before['meta'].get('_elementor_page_settings'), 'pagina-instellingen'
    return res


_SID = {}


def mcp(host, ability, params):
    """WordPress-ability via de MCP-adapter (alleen staging heeft die)."""
    url = HOSTS[host] + '/wp-json/mcp/mcp-adapter-default-server'
    hdr = ['Accept: application/json, text/event-stream']
    if host not in _SID:
        _throttle()
        init = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'dpv', 'version': '1'}}})
        r = subprocess.run(['curl', '-sS', '-D', '-', '-o', '/dev/null', '-X', 'POST', url, '-H', hdr[0],
                            '-H', 'Content-Type: application/json', '--data-binary', '@-'], input=init.encode(), capture_output=True)
        _SID[host] = [l.split(':', 1)[1].strip() for l in r.stdout.decode().splitlines()
                      if l.lower().startswith('mcp-session-id')][0]
    call = json.dumps({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {
        'name': 'mcp-adapter-execute-ability', 'arguments': {'ability_name': ability, 'parameters': params}}})
    res = request(url, method='POST', data=call, headers=hdr + [f'Mcp-Session-Id: {_SID[host]}'])
    if res.get('error') or res.get('result', {}).get('isError'):
        raise RuntimeError(str(res)[:300])
    return res


def clear_cache(host, pid=None, kind='pages'):
    """live (admin): Elementor 'Bestanden & data wissen' (CSS + element-cache).
    staging (editor, 403 op die route): document-save via de Elementor-MCP met de
    bestaande pagina-instellingen; dat leegt element-cache en CSS van die pagina."""
    if host == 'live':
        body, code = api(host, '/elementor/v1/cache', method='DELETE', want='text')
        return code
    p = get_post(host, pid, kind)
    settings = p['meta'].get('_elementor_page_settings') or {}
    mcp(host, 'elementor/update-page-settings', {'post_id': pid, 'settings': settings})
    after = get_post(host, pid, kind)
    assert after['meta'].get('_elementor_page_settings') == settings, 'pagina-instellingen gewijzigd'
    return 'doc-save'



def replace_in_widgets(host, pid, phase, pairs, kind='pages'):
    """pairs: [(oud, nieuw, verwacht_aantal_of_None)]. Back-up → vervangen → opslaan → cache."""
    before, bpath = backup(host, pid, phase, kind)
    data = json.loads(before['meta']['_elementor_data'])
    ws = html_widgets(data)
    report = []
    for old, new, expect in pairs:
        n = sum(w['settings'].get('html', '').count(old) for w in ws)
        if expect is not None and n != expect:
            raise RuntimeError(f'{pid}: "{old[:60]}" {n}× gevonden, verwacht {expect}')
        for w in ws:
            w['settings']['html'] = w['settings'].get('html', '').replace(old, new)
        report.append((old, n))
    save_elementor(host, pid, before, data, kind)
    return bpath, report


def fetch_page(host, path):
    body, code = request(HOSTS[host] + path, want='text')
    return body, code


def status(host_or_url, path=''):
    url = host_or_url if host_or_url.startswith('http') else HOSTS[host_or_url] + path
    return request(url, want='status')


# ---------------------------------------------------------------- QA
def _decoded_scripts(html):
    import base64
    out = ''
    for m in re.finditer(r'src="data:text/javascript;base64,([^"]+)"', html):
        try:
            out += base64.b64decode(m.group(1)).decode('utf-8', 'ignore')
        except Exception:
            pass
    return out


BLANKET = re.compile(r'gratis\s+bezorg\w*\s+(?:in\s+[\w\- ]+\s+)?(?:v\.a\.|vanaf)\s*€\s*150|bezorgen\s+is\s+gratis|gratis\s+bezorg\w*\s+bij\s+een\s+besteding', re.I)
GUNS = re.compile(r'\b\d+\s*(?:laser)?guns?\b|\b\d+\s+lasergunsets?\b', re.I)


def qa(host, path, check_links=True, link_cache=None):
    """QA-checklist voor één URL. Interne links worden (gethrottled) gecontroleerd."""
    st = status(host, path)
    html, code = fetch_page(host, path)
    full = html + _decoded_scripts(html)
    canon = re.findall(r'<link rel="canonical" href="([^"]+)"', html)
    robots = re.findall(r'<meta name=.robots. content=.([^"\']+)', html)
    text = re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>|<script.*?</script>', ' ', full, flags=re.S))
    res = {
        'status': st,
        'h1': len(re.findall(r'<h1[\s>]', full)),
        'canonical': canon[0] if canon else None,
        'self_canonical': bool(canon) and canon[0].rstrip('/') == (HOSTS[host] + path).rstrip('/'),
        'robots': robots[0] if robots else None,
        'wa': sorted(set(re.findall(r'wa\.me/\d+', full))),
        'staging_in_live': (host == 'live') and ('staging.' in full),
        'blanket_claim': BLANKET.findall(text),
        'guns': GUNS.findall(text),
    }
    if check_links:
        cache = link_cache if link_cache is not None else {}
        links = set()
        for h in re.findall(r'href="([^"#?]+)', full):
            if h.startswith(HOSTS[host]):
                h = h[len(HOSTS[host]):]
            if h.startswith('/') and not h.startswith('//') and not re.search(r'\.(css|js|png|jpe?g|webp|svg|ico|xml|woff2?)$|/wp-(json|content|includes|admin)|/feed/|xmlrpc', h):
                links.add(h)
        bad = []
        for l in sorted(links):
            if l not in cache:
                cache[l] = status(host, l)
            if cache[l] != '200|':
                bad.append((l, cache[l]))
        res['links'] = len(links)
        res['bad_links'] = bad
    return res
