#!/usr/bin/env python3
"""
Regiopagina-generator Dagpakketverhuur.

Bouwt de HTML-widget voor Elementor (1 container, 1 HTML-widget) volgens de
vaste regionale SEO-architectuur:

  A  hub        /lasergame-huren/
  B  provincie  /lasergame-huren-<provincie>/
  C  stad       /lasergame-huren-<stad>/

Stijl = homepage (Shadow DOM, zelfde tokens, typografie, knoppen, cards,
radius, schaduwen en responsive spacing). De productkaarten staan bewust in
de light DOM (slot), net als op de homepage, zodat dpv-shop ze kan bedienen.

Gebruik:  python3 build.py            → schrijft out/<slug>.html
De inhoud per pagina staat in content_*.py; de opbouw per template hieronder.
"""
import html, json, os, re, sys, importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://staging.dagpakketverhuur.nl'
WA = 'https://wa.me/31636161518'
TEL = 'tel:0852129150'

e = html.escape


def url(path):
    # Relatief: dezelfde HTML werkt op staging én live, zonder staging-URL's.
    return path


# ---------------------------------------------------------------- icons
# Lijn-iconen in de stijl van de site (stroke = currentColor).
ICONS = {
    'shield': '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
    'pin': '<path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    'truck': '<path d="M3 6h11v9H3z"/><path d="M14 9h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'gift': '<path d="M4 11h16v9H4z"/><path d="M3 7h18v4H3z"/><path d="M12 7v13"/><path d="M12 7c-1.5-3-5-3-5-.8C7 7 9 7 12 7Zm0 0c1.5-3 5-3 5-.8C17 7 15 7 12 7Z"/>',
    'cake': '<path d="M4 20h16v-7H4z"/><path d="M4 16c2 1 3-1 4 0s2 1 4 0 2-1 4 0 3 1 4 0"/><path d="M12 13V9"/><path d="M12 6.5c.8-.8.8-1.7 0-2.5-.8.8-.8 1.7 0 2.5Z"/>',
    'users': '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2c3 .2 5.5 2.6 5.5 5.8"/>',
    'briefcase': '<path d="M3 8h18v12H3z"/><path d="M8 8V5h8v3"/><path d="M3 13h18"/>',
    'school': '<path d="m12 4 10 5-10 5L2 9l10-5Z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
    'star': '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9L12 3Z"/>',
    'cart': '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.2a1 1 0 0 0 1 .8h9.7a1 1 0 0 0 1-.8L21 7H6"/>',
    'calendar': '<path d="M4 6h16v15H4z"/><path d="M4 10h16"/><path d="M8 3v5M16 3v5"/>',
    'return': '<path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/>',
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4V5Z"/>',
    'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    'check': '<path d="m5 12 4.5 4.5L19 7"/>',
}


def icon(name, size=22):
    return (f'<svg class="dpv-ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------- css
# Basis = letterlijk de homepage (reset, tokens, wrap, hero, koppen, knoppen,
# ons-verhaal-blok, reviews, animaties). Daaronder alleen componenten die de
# homepage niet heeft, opgebouwd uit dezelfde tokens.
CSS = r"""
:host{display:block}
*{box-sizing:border-box;margin:0;padding:0;border:0;background:none;font:inherit;color:inherit;
  letter-spacing:normal;text-transform:none;text-decoration:none;list-style:none}
.dpv-home{--pri:#2f4156;--ink:#14181f;--mut:#5b6472;--soft:#9aa2ad;--line:#ececec;
  font-family:Inter,Arial,sans-serif;font-size:16px;font-weight:400;line-height:1.5;
  color:var(--ink);text-wrap:pretty;background:#fafafa;padding-bottom:96px}
a{color:var(--pri);cursor:pointer}
h1,h2,h3,.dpv-num{font-family:Poppins,Arial,sans-serif}
img{display:block;max-width:100%}
button{cursor:pointer}
.dpv-wrap{max-width:1280px;margin:0 auto;padding:72px 32px 0}
.dpv-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}

/* hero */
.dpv-hero{position:relative;height:600px;overflow:hidden;background:#14181f}
.dpv-hero>img.dpv-img{object-position:50% 50%}
.dpv-hero-scrim{position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(0deg,rgba(10,12,16,.72) 0%,rgba(10,12,16,.35) 45%,rgba(10,12,16,.1) 70%),
    linear-gradient(90deg,rgba(10,12,16,.45) 0%,rgba(10,12,16,0) 60%)}
.dpv-hero-body{position:absolute;left:0;right:0;bottom:0;padding:0 32px 56px}
.dpv-hero-inner{max-width:1280px;margin:0 auto}
.dpv-hero-col{max-width:560px}
.dpv-eyebrow{font-size:13px;font-weight:600;color:#fff;opacity:.85;letter-spacing:.03em;margin-bottom:16px}
.dpv-hero h1{font-size:42px;line-height:1.16;font-weight:700;margin-bottom:18px;color:#fff;letter-spacing:-.01em}
.dpv-hero-sub{font-size:15.5px;color:#e7e9ec;line-height:1.7;margin-bottom:28px;max-width:440px}
.dpv-cta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center}
.dpv-btn{background:#fff;color:var(--ink);font-weight:600;font-size:14.5px;
  padding:15px 26px;border-radius:8px;display:inline-block}
.dpv-btn:hover{background:#f1f2f4}
.dpv-btn-dark{background:var(--pri);color:#fff}
.dpv-btn-dark:hover{background:#24344a}
.dpv-link-ul{color:#fff;font-weight:600;font-size:14.5px;border-bottom:1.5px solid #fff;padding-bottom:2px}
.dpv-link-ul:hover{opacity:.85}

/* sectiekoppen */
.dpv-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;margin-bottom:28px;gap:8px 12px}
.dpv-head h2{font-size:22px;font-weight:700}
.dpv-head a{font-weight:600;font-size:13.5px;white-space:nowrap}
.dpv-lead{font-size:15px;color:var(--mut);line-height:1.7;max-width:640px;margin:-16px 0 28px}
.dpv-kicker{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#a8935f;margin-bottom:14px}

/* trustbar */
.dpv-trust{max-width:1280px;margin:0 auto;padding:0 32px}
.dpv-trust ul{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border-radius:12px;
  box-shadow:0 1px 3px rgba(20,24,31,.07);margin-top:-36px;position:relative}
.dpv-trust li{display:flex;gap:12px;align-items:flex-start;padding:20px 22px;border-left:1px solid var(--line)}
.dpv-trust li:first-child{border-left:0}
.dpv-trust .dpv-ic{flex-shrink:0;color:var(--pri);margin-top:1px}
.dpv-trust strong{display:block;font-weight:600;font-size:14px;line-height:1.35}
.dpv-trust small{display:block;font-size:12.5px;color:var(--mut);line-height:1.45;margin-top:2px}

/* intro */
.dpv-intro{display:grid;grid-template-columns:5fr 7fr;gap:48px;align-items:start}
.dpv-intro h2{font-size:27px;font-weight:700;line-height:1.3}
.dpv-intro p{font-size:15px;color:#5c6068;line-height:1.75;margin-bottom:14px}
.dpv-intro p:last-child{margin-bottom:0}

/* producten: kaarten in light DOM, info-kaart ernaast */
.dpv-prodrow{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}
.dpv-prodrow-wide{grid-template-columns:minmax(0,1fr)}
::slotted(#dpv-rg-prods){display:grid}

/* kaarten (zelfde wit/radius/schaduw als de productkaarten) */
.dpv-card{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(20,24,31,.07);padding:24px;
  display:flex;flex-direction:column}
.dpv-card h3{font-size:16px;font-weight:700;line-height:1.3;margin-bottom:8px}
.dpv-card p{font-size:14px;color:var(--mut);line-height:1.65}
.dpv-card .dpv-ic{color:var(--pri);margin-bottom:14px}
.dpv-card-link{margin-top:auto;padding-top:14px;font-weight:600;font-size:13.5px}
.dpv-grid{display:grid;gap:16px}
.dpv-g2{grid-template-columns:repeat(2,1fr)}
.dpv-g3{grid-template-columns:repeat(3,1fr)}
.dpv-g4{grid-template-columns:repeat(4,1fr)}
a.dpv-card{color:inherit;transition:box-shadow .2s ease,transform .2s ease}
a.dpv-card:hover{box-shadow:0 6px 18px rgba(20,24,31,.10);transform:translateY(-2px)}
a.dpv-card .dpv-card-link{color:var(--pri)}

.dpv-checks li{display:flex;gap:10px;align-items:flex-start;font-size:14px;color:#3d434c;line-height:1.5;padding:7px 0;
  border-top:1px solid var(--line)}
.dpv-checks li:first-child{border-top:0}
.dpv-checks .dpv-ic{color:var(--pri);flex-shrink:0;margin:0}

/* keuzehulp */
.dpv-pick-tag{display:inline-block;align-self:flex-start;background:#eef1f5;color:var(--pri);font-size:11.5px;font-weight:600;
  padding:3px 10px;border-radius:20px;margin-bottom:12px}
.dpv-card-soft{background:#f6f4ef;box-shadow:none}

/* stappen */
.dpv-step{position:relative}
.dpv-step-n{font-family:Poppins,Arial,sans-serif;font-weight:700;font-size:13px;color:#fff;background:var(--pri);
  width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:14px}

/* regio / steden */
.dpv-place{flex-direction:row;align-items:center;gap:14px;padding:20px 22px}
.dpv-place .dpv-ic{margin:0;flex-shrink:0}
.dpv-place strong{display:block;font-family:Poppins,Arial,sans-serif;font-weight:700;font-size:16px}
.dpv-place small{display:block;font-size:13px;color:var(--mut)}
.dpv-place .dpv-arr{margin-left:auto;color:var(--pri);font-weight:600}
.dpv-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.dpv-chips li{background:#fff;border:1px solid #e3e6ea;border-radius:20px;padding:6px 14px;font-size:13.5px;color:#3d434c}

/* ons-verhaal-blok (homepage) — hier voor zakelijk */
.dpv-about{display:grid;grid-template-columns:1fr 1fr}
.dpv-about-txt{background:#f6f4ef;padding:48px 48px 48px 0;display:flex;flex-direction:column;
  justify-content:center;min-height:420px;border-radius:18px 0 0 18px}
.dpv-about-txt>div{padding-left:32px}
.dpv-about-txt h2{font-size:27px;font-weight:700;margin-bottom:16px;line-height:1.3}
.dpv-about-txt p{font-size:15px;color:#5c6068;line-height:1.75;margin-bottom:24px;max-width:460px}
.dpv-about-txt .dpv-checks{margin-bottom:28px;max-width:460px}
.dpv-about-txt .dpv-checks li{border-color:#e6e1d6}
.dpv-link-dark{color:var(--ink);font-weight:600;font-size:14px;border-bottom:1.5px solid var(--ink);padding-bottom:2px;align-self:flex-start}
.dpv-about-img{position:relative;min-height:420px;border-radius:0 18px 18px 0;overflow:hidden;background:#f6f4ef}
.dpv-b2b-compact .dpv-about-txt,.dpv-b2b-compact .dpv-about-img{min-height:320px}

/* review (homepage-stijl, één review) */
.dpv-rev-title{font-size:22px;font-weight:700;margin-bottom:8px;text-align:center}
.dpv-rev-sub{text-align:center;font-size:14px;color:var(--mut);margin-bottom:28px}
.dpv-rev{display:grid;grid-template-columns:280px 1fr;gap:32px;align-items:center;max-width:820px;margin:0 auto}
.dpv-rev-photo{position:relative;aspect-ratio:1/1;border-radius:12px;overflow:hidden;background:#f1f2f3}
.dpv-stars{color:var(--pri);font-size:12px;letter-spacing:.15em;margin-bottom:10px}
.dpv-rev blockquote p{font-size:19px;color:#3d434c;line-height:1.55;margin-bottom:14px;font-family:Poppins,Arial,sans-serif;font-weight:500}
.dpv-rev cite{display:block;font-size:11.5px;font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;color:var(--soft);font-style:normal;line-height:1.5}

/* faq */
.dpv-faq{display:grid;grid-template-columns:4fr 8fr;gap:48px;align-items:start}
.dpv-faq-side h2{font-size:22px;font-weight:700;margin-bottom:12px}
.dpv-faq-side p{font-size:14.5px;color:var(--mut);line-height:1.7;margin-bottom:18px}
.dpv-contact{display:flex;flex-direction:column;gap:10px}
.dpv-contact a{display:flex;gap:12px;align-items:center;background:#fff;border-radius:12px;
  box-shadow:0 1px 3px rgba(20,24,31,.07);padding:14px 16px;color:var(--ink)}
.dpv-contact a:hover{box-shadow:0 6px 18px rgba(20,24,31,.10)}
.dpv-contact .dpv-ic{color:var(--pri);flex-shrink:0}
.dpv-contact strong{display:block;font-weight:600;font-size:14px}
.dpv-contact small{display:block;font-size:12.5px;color:var(--mut)}
.dpv-qa{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(20,24,31,.07);margin-bottom:10px}
.dpv-qa summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center;
  padding:18px 20px;font-weight:600;font-size:15px;line-height:1.4}
.dpv-qa summary::-webkit-details-marker{display:none}
.dpv-qa summary::after{content:'+';font-size:20px;font-weight:400;color:var(--pri);flex-shrink:0;line-height:1}
.dpv-qa[open] summary::after{content:'–'}
.dpv-qa .dpv-qa-a{padding:0 20px 18px;font-size:14.5px;color:var(--mut);line-height:1.7}
.dpv-qa .dpv-qa-a a{font-weight:600}

/* slot-cta (beeldband in hero-stijl) */
.dpv-final{position:relative;max-width:1216px;margin:72px auto 0;border-radius:18px;overflow:hidden;min-height:380px;
  display:flex;align-items:flex-end;background:#14181f}
.dpv-final .dpv-hero-scrim{background:linear-gradient(0deg,rgba(10,12,16,.78) 0%,rgba(10,12,16,.45) 55%,rgba(10,12,16,.2) 100%)}
.dpv-final-body{position:relative;padding:48px;max-width:640px}
.dpv-final h2{font-size:30px;line-height:1.2;font-weight:700;color:#fff;margin-bottom:14px}
.dpv-final p{font-size:15px;color:#e7e9ec;line-height:1.7;margin-bottom:24px}
.dpv-final-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:22px}
.dpv-final-links a{color:#fff;font-size:13.5px;font-weight:600;opacity:.85;border-bottom:1px solid rgba(255,255,255,.5)}
.dpv-final-links a:hover{opacity:1}

/* scroll-animatie (homepage) */
.dpv-anim [data-reveal]{opacity:0;transform:translateY(22px);
  transition:opacity .7s cubic-bezier(.22,.61,.36,1),transform .7s cubic-bezier(.22,.61,.36,1)}
.dpv-anim [data-reveal].is-in{opacity:1;transform:none}
.dpv-anim .dpv-hero-col{opacity:0;transform:translateY(16px);
  animation:dpvHeroIn .8s cubic-bezier(.22,.61,.36,1) .15s forwards}
@keyframes dpvHeroIn{to{opacity:1;transform:none}}

@media (max-width:1024px){
  .dpv-g4{grid-template-columns:repeat(2,1fr)}
  .dpv-trust ul{grid-template-columns:repeat(2,1fr)}
  .dpv-trust li:nth-child(3){border-left:0}
  .dpv-trust li:nth-child(n+3){border-top:1px solid var(--line)}
}
@media (max-width:860px){
  .dpv-home{padding-bottom:64px}
  .dpv-wrap{padding:48px 20px 0}
  .dpv-hero{height:480px}
  .dpv-hero h1{font-size:30px}
  .dpv-hero-sub{font-size:14.5px;margin-bottom:22px}
  .dpv-hero-body{padding:0 20px 56px}
  .dpv-head h2{font-size:18px}
  .dpv-lead{margin-top:-14px}
  .dpv-trust{padding:0 20px}
  .dpv-trust ul{grid-template-columns:minmax(0,1fr);margin-top:-28px}
  .dpv-trust li{border-left:0;border-top:1px solid var(--line);padding:14px 16px}
  .dpv-trust li:first-child{border-top:0}
  .dpv-intro,.dpv-faq{grid-template-columns:minmax(0,1fr);gap:20px}
  .dpv-intro h2{font-size:22px}
  .dpv-prodrow{grid-template-columns:minmax(0,1fr)}
  .dpv-g2,.dpv-g3,.dpv-g4{grid-template-columns:minmax(0,1fr)}
  .dpv-card{padding:20px}
  .dpv-about{grid-template-columns:minmax(0,1fr)}
  .dpv-about-txt{border-radius:18px 18px 0 0;padding:28px 20px;min-height:0}
  .dpv-about-txt>div{padding-left:0}
  .dpv-about-txt h2{font-size:22px}
  .dpv-about-img{border-radius:0 0 18px 18px;min-height:260px}
  .dpv-b2b-compact .dpv-about-txt{min-height:0}
  .dpv-b2b-compact .dpv-about-img{min-height:220px}
  .dpv-rev-title{font-size:19px}
  .dpv-rev{grid-template-columns:minmax(0,1fr);gap:18px}
  .dpv-rev blockquote p{font-size:16px}
  .dpv-final{margin:48px 20px 0;min-height:340px}
  .dpv-final-body{padding:28px 20px}
  .dpv-final h2{font-size:24px}
}
@media (prefers-reduced-motion:reduce){
  .dpv-anim [data-reveal]{opacity:1;transform:none;transition:none}
  .dpv-anim .dpv-hero-col{opacity:1;transform:none;animation:none}
}
"""

# Light-DOM-grid voor de echte WooCommerce-productkaarten (dpv-shop).
LIGHT_CSS = """
/* Volle breedte, zoals de vorige regiopagina's (thema-container opheffen). */
.elementor-widget-html > .elementor-widget-container:has(> #dpv-rg-host){padding:0 !important;margin:0 !important;max-width:none !important}
.elementor-element:has(.elementor-widget-html > .elementor-widget-container > #dpv-rg-host){max-width:none !important;width:100vw !important;margin-left:calc(50% - 50vw) !important;margin-right:calc(50% - 50vw) !important}
.elementor-element:has(#dpv-rg-host) > .elementor-widget-wrap,.elementor-element:has(#dpv-rg-host) > .elementor-container,.elementor-element:has(#dpv-rg-host) > .e-con-inner{max-width:none !important;width:100% !important}
#dpv-rg-prods{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;align-items:stretch}
#dpv-rg-prods [data-prod-card]{height:100%}
#dpv-rg-prods[data-cols="3"]{grid-template-columns:repeat(3,1fr)}
#dpv-rg-prods[data-cols="4"]{grid-template-columns:repeat(4,1fr)}
@media (max-width:860px){#dpv-rg-prods[data-cols="3"],#dpv-rg-prods[data-cols="4"]{grid-template-columns:repeat(2,1fr)}}
/* toast van dpv-shop gebruikt var(--ink); die bestaat buiten de shop niet */
.dpvs-toast{--ink:#14181f}
"""

# ---------------------------------------------------------------- js
JS = r"""
(function(){
  var host=document.getElementById('dpv-rg-host'),
      tpl=document.getElementById('dpv-rg-tpl'),
      grid=document.getElementById('dpv-rg-prods');
  if(!host||!tpl||host.dataset.dpvInit)return; host.dataset.dpvInit='1';

  /* Ontwerp in een shadow root, net als de homepage. */
  var root=host.attachShadow?host.attachShadow({mode:'open'}):host;
  root.appendChild(tpl.content.cloneNode(true));
  if(grid)host.appendChild(grid);            /* slot="prods" */
  tpl.remove();

  /* WhatsApp-tracking-bridge — gelijk aan header/footer/klantenservice:
     een klik op een wa.me-link in de shadow root wordt doorgegeven aan een
     verborgen link in de light DOM, zodat GTM en de conversietags hem zien. */
  root.addEventListener('click',function(e){
    var path=typeof e.composedPath==='function'?e.composedPath():[];var link=null;
    for(var i=0;i<path.length;i++){var el=path[i];
      if(el&&el.tagName==='A'&&el.href&&/^https:\/\/wa\.me\//i.test(el.href)){link=el;break}}
    if(!link||e.defaultPrevented)return;
    e.preventDefault();
    var bridge=document.getElementById('dpv-rg-wa-bridge');
    if(!bridge){bridge=document.createElement('a');bridge.id='dpv-rg-wa-bridge';
      bridge.setAttribute('aria-hidden','true');bridge.tabIndex=-1;
      bridge.style.cssText='position:fixed;left:-99999px;top:-99999px;width:1px;height:1px;overflow:hidden;';
      document.body.appendChild(bridge)}
    bridge.href=link.href;bridge.textContent=(link.textContent||'WhatsApp').trim();
    if(link.rel){bridge.rel=link.rel}else{bridge.removeAttribute('rel')}
    if(link.target){bridge.target=link.target}else if(e.ctrlKey||e.metaKey||e.shiftKey){bridge.target='_blank'}else{bridge.removeAttribute('target')}
    bridge.click();
  });

  /* Interne ankers (#lasergames) binnen de shadow root. */
  root.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[data-scroll]');
    if(!a)return;
    var t=root.getElementById(a.getAttribute('data-scroll'));
    if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}
  });

  /* Lazy-load-plugins komen niet in een shadow root: bronnen zelf terugzetten. */
  var unlazy=function(scope){
    scope.querySelectorAll('img,video,source').forEach(function(el){
      var d=el.dataset||{};
      var src=d.src||d.lazySrc||d.original||d.lazyOriginal||el.getAttribute('data-lazy-src');
      if(src&&(!el.getAttribute('src')||/^data:image/.test(el.getAttribute('src'))))el.setAttribute('src',src);
      var ss=d.srcset||d.lazySrcset||el.getAttribute('data-lazy-srcset');
      if(ss&&!el.getAttribute('srcset'))el.setAttribute('srcset',ss);
      el.removeAttribute('loading');
    });
  };
  unlazy(root);

  /* Scroll-animaties (homepage) */
  var wrap=root.querySelector('.dpv-home'),
      reveal=[].slice.call(root.querySelectorAll('[data-reveal]'));
  if(wrap&&reveal.length&&'IntersectionObserver' in window){
    wrap.classList.add('dpv-anim');
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});
    },{rootMargin:'0px 0px -12% 0px',threshold:.12});
    reveal.forEach(function(el){io.observe(el);});
    setTimeout(function(){reveal.forEach(function(el){el.classList.add('is-in');});},3000);
  }

  if(!grid)return;
  unlazy(grid);

  /* Alt-teksten van de productfoto's (de kaarten van dpv-shop hebben alt=""). */
  var setAlts=function(){
    var alts={};try{alts=JSON.parse(grid.dataset.alts||'{}')}catch(e){}
    Object.keys(alts).forEach(function(id){
      var b=grid.querySelector('[data-product="'+id+'"]'),card=b&&b.closest('[data-prod-card]'),img=card&&card.querySelector('img');
      if(img)img.setAttribute('alt',alts[id]);
    });
  };
  setAlts();

  /* Productkaarten actueel houden: dezelfde kaarten als op de categoriepagina
     (prijs, badge, knop). Lukt dat niet, dan blijven de meegeleverde kaarten staan. */
  var ids=[].map.call(grid.querySelectorAll('[data-product]'),function(b){return b.dataset.product;});
  if(ids.length&&window.fetch&&window.DOMParser){
    fetch(grid.dataset.src,{credentials:'same-origin'})
      .then(function(r){return r.ok?r.text():Promise.reject(r.status);})
      .then(function(t){
        var doc=new DOMParser().parseFromString(t,'text/html');
        ids.forEach(function(id){
          var btn=doc.querySelector('[data-prod-card] [data-product="'+id+'"]'),
              mine=grid.querySelector('[data-product="'+id+'"]');
          if(!btn||!mine)return;
          var fresh=btn.closest('[data-prod-card]'),old=mine.closest('[data-prod-card]');
          fresh.querySelectorAll('noscript').forEach(function(n){n.remove();});
          old.replaceWith(document.importNode(fresh,true));
        });
        unlazy(grid);
        setAlts();
      }).catch(function(){});
  }

  /* DPV Shop laden als WordPress het op deze pagina niet meestuurt (de plugin
     enqueuet alleen op shop-/product-/vaste pagina's). Dezelfde plugin-bestanden
     als op de shop; add-to-cart werkt zonder nonce (gecachte pagina's). Pas na
     'load', zodat er nooit een tweede kopie naast een normaal geladen script komt. */
  var loadShop=function(){
    if(document.getElementById('dpv-shop-js')||window.DPVS_API)return;
    window.DPVS=window.DPVS||{ajax:'/wp-admin/admin-ajax.php',nonce:'',cart_url:'/winkelwagen/',checkout:'/afreken-pagina/'};
    var base='/wp-content/plugins/dpv-shop/assets/';
    var l=document.createElement('link');l.rel='stylesheet';l.id='dpv-shop-css';l.href=base+'css/dpv-shop.css';
    document.head.appendChild(l);
    [['dpv-shop-js','js/dpv-shop.js'],['dpv-shop-ga4-js','js/dpv-ga4.js']].forEach(function(f){
      var s=document.createElement('script');s.id=f[0];s.src=base+f[1];s.async=false;document.body.appendChild(s);
    });
  };
  if(document.readyState==='complete')loadShop();else window.addEventListener('load',loadShop);

  /* Huren-knop: dpv-shop handelt hem af zodra het script draait. Draait het
     (nog) niet, dan gaat de knop naar de productpagina, zodat hij nooit dood is. */
  grid.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.js-dpvs-add');
    if(!b||window.DPVS_API)return;
    var card=b.closest('[data-prod-card]'),a=card&&card.querySelector('a[href]');
    if(a){e.preventDefault();e.stopPropagation();window.location.href=a.href;}
  },true);
})();
"""


# ---------------------------------------------------------------- sections
def sec(inner, cls='dpv-wrap', sid=None, extra=''):
    i = f' id="{sid}"' if sid else ''
    return f'<section class="{cls}"{i} data-reveal{extra}>\n{inner}\n</section>'


def head(title, link=None, lead=None):
    a = f'<a href="{e(link[0])}">{e(link[1])} →</a>' if link else ''
    out = f'<div class="dpv-head"><h2>{title}</h2>{a}</div>'
    if lead:
        out += f'<p class="dpv-lead">{lead}</p>'
    return out


def hero(d):
    return f'''<section class="dpv-hero">
  <img data-skip-lazy class="skip-lazy no-lazyload dpv-img" src="{e(d['img'])}" alt="{e(d['alt'])}" fetchpriority="high" style="object-position:{d.get('pos','50% 50%')}">
  <div class="dpv-hero-scrim"></div>
  <div class="dpv-hero-body"><div class="dpv-hero-inner"><div class="dpv-hero-col">
    <div class="dpv-eyebrow">{d['eyebrow']}</div>
    <h1>{d['h1']}</h1>
    <p class="dpv-hero-sub">{d['sub']}</p>
    <div class="dpv-cta-row">
      {f'<a class="dpv-btn" href="{e(d["cta_href"])}">' if d.get('cta_href') else '<a class="dpv-btn" href="#lasergames" data-scroll="lasergames">'}{d.get('cta','Bekijk lasergames')}</a>
      {d.get('cta2','')}
    </div>
  </div></div></div>
</section>'''


def trustbar(items):
    lis = ''.join(f'<li>{icon(i)}<div><strong>{t}</strong><small>{s}</small></div></li>' for i, t, s in items)
    return f'<section class="dpv-trust" aria-label="Voordelen"><ul>{lis}</ul></section>'


def intro(d):
    ps = ''.join(f'<p>{p}</p>' for p in d['p'])
    kicker = f'<div class="dpv-kicker">{d["kicker"]}</div>' if d.get('kicker') else ''
    return sec(f'<div class="dpv-intro"><div>{kicker}<h2>{d["h2"]}</h2></div><div>{ps}</div></div>')


def products(d):
    checks = ''.join(f'<li>{icon("check", 18)}<span>{c}</span></li>' for c in d['checks'])
    return sec(
        head(d['h2'], (d['cat_link'], d.get('cat_label', 'Alle lasergame-producten')) if d.get('cat_link') else None, d.get('lead'))
        + f'''
<div class="dpv-prodrow{' dpv-prodrow-wide' if d.get('wide') else ''}">
  <slot name="prods"></slot>
  <div class="dpv-card dpv-card-soft">
    <h3>{d['info_h3']}</h3>
    <ul class="dpv-checks">{checks}</ul>
    <a class="dpv-card-link" href="{e(d['info_link'][0])}">{e(d['info_link'][1])} →</a>
  </div>
</div>''', sid='lasergames')


def cards(items, cols='dpv-g3', tag=False):
    out = []
    for c in items:
        ic = icon(c['icon']) if c.get('icon') else ''
        tg = f'<span class="dpv-pick-tag">{c["tag"]}</span>' if c.get('tag') else ''
        lk = f'<span class="dpv-card-link">{e(c["link"][1])} →</span>' if c.get('link') else ''
        cls = 'dpv-card' + (' dpv-card-soft' if c.get('soft') else '')
        body = f'{ic}{tg}<h3>{c["h3"]}</h3><p>{c["p"]}</p>'
        if c.get('link'):
            out.append(f'<a class="{cls}" href="{e(c["link"][0])}">{body}{lk}</a>')
        else:
            out.append(f'<div class="{cls}">{body}</div>')
    return f'<div class="dpv-grid {cols}">{"".join(out)}</div>'


def steps(items):
    out = ''.join(
        f'<div class="dpv-card dpv-step"><div class="dpv-step-n">{n}</div><h3>{h}</h3><p>{p}</p></div>'
        for n, (h, p) in enumerate(items, 1))
    return f'<div class="dpv-grid dpv-g4">{out}</div>'


def places(items, cols='dpv-g3'):
    out = ''.join(
        f'<a class="dpv-card dpv-place" href="{e(href)}">{icon("pin")}<div><strong>{t}</strong><small>{s}</small></div>'
        f'<span class="dpv-arr">→</span></a>' for t, s, href in items)
    return f'<div class="dpv-grid {cols}">{out}</div>'


def b2b(d, compact=False):
    checks = ''.join(f'<li>{icon("check", 18)}<span>{c}</span></li>' for c in d['checks'])
    cls = 'dpv-about dpv-b2b-compact' if compact else 'dpv-about'
    return sec(f'''<div class="{cls}">
  <div class="dpv-about-txt"><div>
    <div class="dpv-kicker">{d['kicker']}</div>
    <h2>{d['h2']}</h2>
    <p>{d['p']}</p>
    <ul class="dpv-checks">{checks}</ul>
    <a class="dpv-link-dark" href="{e(url('/zakelijk/'))}">{d.get('cta', 'Zakelijke aanvraag doen')} →</a>
  </div></div>
  <div class="dpv-about-img"><img data-skip-lazy class="skip-lazy no-lazyload dpv-img" src="{e(d['img'])}" alt="{e(d['alt'])}" loading="lazy"></div>
</div>''')


REVIEW = {
    # Echte review (homepage). Geen locatie toegevoegd.
    'quote': 'Super goede service en heel handig geregeld. Mooi dat het zo kan.',
    'cite': 'Jurgen Elshof — bedrijfsuitje lasergame',
    'img': url('/wp-content/uploads/2025/09/F4E27435-5E6B-4CE1-A3FA-FB4B5AE65C54.jpeg'),
    'alt': "Collega's in actie tijdens een lasergame op een bedrijfsuitje",
}


def review(title, sub=None, r=None):
    r = r or REVIEW
    s = f'<p class="dpv-rev-sub">{sub}</p>' if sub else ''
    return sec(f'''<h2 class="dpv-rev-title">{title}</h2>{s}
<figure class="dpv-rev">
  <div class="dpv-rev-photo"><img data-skip-lazy class="skip-lazy no-lazyload dpv-img" src="{e(r['img'])}" alt="{e(r['alt'])}" loading="lazy"></div>
  <div><div class="dpv-stars">★ ★ ★ ★ ★</div>
    <blockquote><p>“{e(r['quote'])}”</p></blockquote>
    <figcaption><cite>{e(r['cite'])}</cite></figcaption></div>
</figure>''')


def contact_box():
    return f'''<div class="dpv-contact">
  <a href="{TEL}">{icon('phone')}<div><strong>Bel 085 212 9150</strong><small>Ma–za 9:00–21:00</small></div></a>
  <a href="{WA}">{icon('chat')}<div><strong>WhatsApp bij spoed</strong><small>06 36 16 15 18 · buiten openingstijden</small></div></a>
</div>'''


def faq(title, intro_txt, qas):
    items = ''.join(
        f'<details class="dpv-qa"><summary>{q}</summary><div class="dpv-qa-a">{a}</div></details>' for q, a in qas)
    return sec(f'''<div class="dpv-faq">
  <div class="dpv-faq-side"><h2>{title}</h2><p>{intro_txt}</p>{contact_box()}</div>
  <div>{items}</div>
</div>''')


def final(d):
    links = ''.join(f'<a href="{e(h)}">{t}</a>' for t, h in d.get('links', []))
    lk = f'<div class="dpv-final-links">{links}</div>' if links else ''
    return f'''<section class="dpv-final" data-reveal>
  <img data-skip-lazy class="skip-lazy no-lazyload dpv-img" src="{e(d['img'])}" alt="{e(d['alt'])}" loading="lazy">
  <div class="dpv-hero-scrim"></div>
  <div class="dpv-final-body">
    <h2>{d['h2']}</h2><p>{d['p']}</p>
    <div class="dpv-cta-row">{f'<a class="dpv-btn" href="{e(d["cta_href"])}">' if d.get('cta_href') else '<a class="dpv-btn" href="#lasergames" data-scroll="lasergames">'}{d.get('cta', 'Bekijk lasergames')}</a>
      <a class="dpv-link-ul" href="{TEL}">Of bel 085 212 9150</a></div>
    {lk}
  </div>
</section>'''


# ---------------------------------------------------------------- templates
def template_a(c):
    """A — hub"""
    return [
        hero(c['hero']), trustbar(c['trust']), *([intro(c['intro'])] if c.get('intro') else []), products(c['products']),
        sec(head(c['keuze']['h2'], lead=c['keuze'].get('lead')) + cards(c['keuze']['items'], c['keuze'].get('cols', 'dpv-g3'))),
        sec(head(c['gelegenheden']['h2'], lead=c['gelegenheden'].get('lead')) + cards(c['gelegenheden']['items'], 'dpv-g4')),
        sec(head(c['stappen']['h2'], lead=c['stappen'].get('lead')) + steps(c['stappen']['items'])),
        sec(head(c['regio']['h2'], lead=c['regio']['lead']) + places(c['regio']['items'])),
        *([sec(head(c['extra_places']['h2'], lead=c['extra_places'].get('lead')) + places(c['extra_places']['items'], c['extra_places'].get('cols', 'dpv-g3')))] if c.get('extra_places') else []),
        b2b(c['b2b']),
        review(c['review']['h2'], c['review'].get('sub'), c['review'].get('data')),
        faq(c['faq']['h2'], c['faq']['intro'], c['faq']['items']),
        final(c['final']),
    ]


def template_b(c):
    """B — provincie"""
    return [
        hero(c['hero']), trustbar(c['trust']), intro(c['intro']), products(c['products']),
        sec(head(c['toepassingen']['h2'], lead=c['toepassingen'].get('lead')) + cards(c['toepassingen']['items'], 'dpv-g4')),
        # Alleen bestaande stadspagina's; zonder steden (bv. Groningen) vervalt het blok.
        *([sec(head(c['steden']['h2'], lead=c['steden']['lead']) + places(c['steden']['items'], 'dpv-g2'))]
          if c.get('steden') and c['steden'].get('items') else []),
        sec(head(c['levering']['h2'], lead=c['levering'].get('lead')) + cards(c['levering']['items'], 'dpv-g3')),
        *([sec(head(c['extra_places']['h2'], lead=c['extra_places'].get('lead')) + places(c['extra_places']['items'], c['extra_places'].get('cols', 'dpv-g3')))] if c.get('extra_places') else []),
        b2b(c['b2b'], compact=True),
        review(c['review']['h2'], c['review'].get('sub'), c['review'].get('data')),
        faq(c['faq']['h2'], c['faq']['intro'], c['faq']['items']),
        final(c['final']),
    ]


def template_c(c):
    """C — stad"""
    return [
        hero(c['hero']), trustbar(c['trust']), intro(c['intro']), products(c['products']),
        sec(head(c['stappen']['h2'], lead=c['stappen'].get('lead')) + steps(c['stappen']['items'])),
        sec(head(c['gelegenheden']['h2'], lead=c['gelegenheden'].get('lead')) + cards(c['gelegenheden']['items'], 'dpv-g3')),
        *([sec(head(c['extra_places']['h2'], lead=c['extra_places'].get('lead')) + places(c['extra_places']['items'], c['extra_places'].get('cols', 'dpv-g3')))] if c.get('extra_places') else []),
        b2b(c['b2b'], compact=True),
        sec(head(c['levering']['h2'], lead=c['levering']['lead'])
            + f'<ul class="dpv-chips" aria-label="Plaatsen rond {e(c["plaats"])}">'
            + ''.join(f'<li>{p}</li>' for p in c['levering']['plaatsen']) + '</ul>'
            + '<div style="height:24px"></div>' + cards(c['levering']['items'], 'dpv-g3')),
        review(c['review']['h2'], c['review'].get('sub'), c['review'].get('data')),
        faq(c['faq']['h2'], c['faq']['intro'], c['faq']['items']),
        final(c['final']),
    ]


TEMPLATES = {'A': template_a, 'B': template_b, 'C': template_c}


# ---------------------------------------------------------------- product cards
def clean_card(card_html, alt=''):
    """Echte dpv-shop-kaart (van de categoriepagina) zonder lazy-load-placeholder."""
    c = re.sub(r'<noscript>.*?</noscript>', '', card_html, flags=re.S)
    c = re.sub(r'src="data:image/svg\+xml;base64,[^"]*"\s+data-src="([^"]+)"', r'src="\1"', c)
    c = c.replace('data-lazyloaded="1" ', '')
    c = re.sub(r'(href|src)="https://staging\.dagpakketverhuur\.nl/', r'\1="/', c)
    if alt:
        c = c.replace('alt=""', f'alt="{e(alt)}"', 1)
    return c.strip()


def render(c, cards_html):
    body = '\n\n'.join(TEMPLATES[c['template']](c))
    alts = {str(pid): a for pid, a in c['product_alts'].items()}
    grid = '\n'.join(clean_card(x, alts.get(str(pid), '')) for pid, x in zip(c['product_ids'], cards_html))
    return f'''<!--
  ============================================================
  DAGPAKKETVERHUUR — {c['naam']}  (template {c['template']})
  Gegenereerd door regiopaginas/build.py — niet met de hand
  aanpassen; wijzig de inhoud in de generator en bouw opnieuw.
  Elementor: 1 container (volle breedte, geen padding) met
  daarin alleen deze HTML-widget.
  Rendert in een SHADOW ROOT (zelfde opzet als de homepage).
  Uitzondering: de productkaarten staan bewust in de light DOM
  (slot), zodat dpv-shop de Huren-knop kan afhandelen.
  ============================================================
-->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<div id="dpv-rg-host"></div>

<!-- Echte WooCommerce-productkaarten (dpv-shop), light DOM via slot. -->
<div id="dpv-rg-prods" slot="prods"{f' data-cols="{c["prod_cols"]}"' if c.get('prod_cols') else ''} data-src="{e(c['cat_url'])}" data-alts="{e(json.dumps(alts, ensure_ascii=False))}">
{grid}
</div>
<style>{LIGHT_CSS}</style>

<template id="dpv-rg-tpl">
<style>{CSS}</style>

<div class="dpv-home">

{body}

</div>
</template>

<script>{JS}</script>
'''


def main(host='live', modules=('content_lasergame',)):
    """Bouwt out/<host>/<slug>.html (+ .seo.json). DPV_HOST stuurt host-specifieke URL's."""
    os.environ['DPV_HOST'] = host
    cards_dir = os.path.join(ROOT, 'cards')
    out_dir = os.path.join(ROOT, 'out', host)
    os.makedirs(out_dir, exist_ok=True)
    for mod in modules:
        if mod in sys.modules:
            del sys.modules[mod]
        m = importlib.import_module(mod)
        for c in m.PAGES:
            cards_html = [open(os.path.join(cards_dir, f'{pid}.html'), encoding='utf-8').read() for pid in c['product_ids']]
            out = render(c, cards_html)
            assert 'staging' not in out or host == 'staging', c['slug']
            open(os.path.join(out_dir, c['slug'] + '.html'), 'w', encoding='utf-8').write(out)
            meta = {k: c.get(k) for k in ('id', 'slug', 'seo_title', 'meta', 'template')}
            open(os.path.join(out_dir, c['slug'] + '.seo.json'), 'w', encoding='utf-8').write(
                json.dumps(meta, ensure_ascii=False, indent=1))
            print(f"[{host}] {c['slug']}: {len(out)} bytes, meta {len(c['meta'])} tekens")


if __name__ == '__main__':
    sys.path.insert(0, ROOT)
    args = sys.argv[1:]
    host = args[0] if args else 'live'
    mods = tuple(args[1:]) or ('content_lasergame',)
    main(host, mods)
