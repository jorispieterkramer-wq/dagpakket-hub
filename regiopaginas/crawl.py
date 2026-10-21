"""Eindcrawl: python3 crawl.py live  → crawl-<host>.json (wa852, laserguns-met-getal, interne links naar 301/404)."""
import json, re, sys
import wp

host = sys.argv[1]
idx, _ = wp.request(wp.HOSTS[host] + '/sitemap_index.xml', want='text')
urls = []
for sm in re.findall(r'<loc>([^<]+)</loc>', idx):
    body, _ = wp.request(sm, want='text')
    urls += re.findall(r'<loc>([^<]+)</loc>', body)
urls = sorted({u for u in urls if not re.search(r'\.(jpe?g|png|webp|gif|svg)$', u)})
print('urls', len(urls), flush=True)
res, links = {}, {}
for u in urls:
    path = u[len(wp.HOSTS[host]):] or '/'
    html, code = wp.fetch_page(host, path)
    full = html + ''.join(wp._decoded_scripts(html))
    text = re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>|<script.*?</script>', ' ', full, flags=re.S))
    ls = set()
    for h in re.findall(r'href="([^"#?]+)', full):
        if h.startswith(wp.HOSTS[host]):
            h = h[len(wp.HOSTS[host]):]
        if h.startswith('/') and not h.startswith('//') and not re.search(r'\.(css|js|png|jpe?g|webp|svg|ico|xml|woff2?|pdf)$|/wp-(json|content|includes|admin)|/feed/|xmlrpc', h):
            ls.add(h)
    for l in ls:
        links.setdefault(l, []).append(path)
    res[path] = {'code': code, 'wa852': full.count('31852129150'), 'guns': wp.GUNS.findall(text)}
    print(path, code, res[path]['wa852'], res[path]['guns'], flush=True)
bad = {}
for l in sorted(links):
    st = wp.status(host, l)
    if st != '200|':
        bad[l] = {'status': st, 'on': sorted(links[l])}
        print('BAD', l, st, len(links[l]), flush=True)
json.dump({'pages': res, 'bad_links': bad, 'n_links': len(links)}, open(f'crawl-{host}.json', 'w'), ensure_ascii=False, indent=1)
print('KLAAR', len(urls), 'pagina\'s', len(links), 'links', len(bad), 'slecht', flush=True)
