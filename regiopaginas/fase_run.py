"""python3 fase_run.py <host> <fase> <slug> [<slug> ...] — deploy + QA per pagina (sequentieel, gethrottled)."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp
host, phase, slugs = sys.argv[1], sys.argv[2], sys.argv[3:]
cache = {}
for s in slugs:
    bpath, c = wp.deploy_generated(host, s, phase)
    r = wp.qa(host, '/' + s + '/', link_cache=cache)
    ok = (r['status'] == '200|' and r['h1'] == 1 and r['wa'] == ['wa.me/31636161518'] and not r['blanket_claim']
          and not r['guns'] and not r['staging_in_live'] and not [b for b in r['bad_links'] if 'activiteiten-huren/' not in b[0]])
    if host == 'live':
        ok = ok and r['self_canonical'] and r['robots'].startswith('index, follow')
    print(json.dumps({'slug': s, 'backup': bpath, 'cache': c, 'OK': ok, **r}, ensure_ascii=False), flush=True)
