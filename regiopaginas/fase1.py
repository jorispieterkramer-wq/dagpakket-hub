import sys,re,json,wp
host=sys.argv[1]
IDS=[49704,49699,49709,49900,49908,49916]
PAIRS=[('href="/product-category/geluid/"','href="/product/silent-disco-huren/"',1),
       ('href="/silent-disco-huren/"','href="/silent-disco-verhuur/"',1)]
for pid in IDS:
    bpath,rep=wp.replace_in_widgets(host,pid,'fase1',PAIRS)
    c=wp.clear_cache(host,pid)
    p=wp.get_page(host,pid); path='/'+p['slug']+'/'
    html,code=wp.fetch_page(host,path)
    ok_cta='href="/product/silent-disco-huren/" class="kf-hero-cta"' in html or re.search(r'href="/product/silent-disco-huren/"[^>]*kf-hero-cta',html)
    print(f"{host} {pid} {path} backup={bpath} cache={c} page={code} cta_nieuw={bool(ok_cta)} geluid_weg={'product-category/geluid' not in html} pill_nieuw={'href=\"/silent-disco-verhuur/\"' in html} oude_pill_weg={'href=\"/silent-disco-huren/\"' not in html}")
