"""Woordreeks-overlap (5-gram shingles, Jaccard) tussen zichtbare teksten van gegenereerde pagina's."""
import re, html, sys, os, itertools
def text(path):
    s=open(path,encoding='utf-8').read()
    s=s[s.find('<template'):s.find('</template>')]
    s=re.sub(r'<style.*?</style>|<script.*?</script>',' ',s,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>',' ',s)).lower()
    return re.findall(r"[a-zà-ÿ0-9€']+",t)
def sh(w,n=5): return {tuple(w[i:i+n]) for i in range(len(w)-n+1)}
def score(a,b):
    A,B=sh(text(a)),sh(text(b)); return len(A&B)/len(A|B)
if __name__=='__main__':
    host=sys.argv[1]; groups=[g.split(',') for g in sys.argv[2:]]
    for g in groups:
        for a,b in itertools.combinations(g,2):
            print(f'{a:28} {b:28} {score(f"out/{host}/{a}.html",f"out/{host}/{b}.html"):.2f}')
