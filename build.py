# -*- coding: utf-8 -*-
# Generiert lebenslauf-de.html und resume-en.html in /Users/edgarheinz/Projects/Lebenslauf
# Benötigt: figure_cut.png (Kopf+Hände-Freisteller), pjs-latin.woff2 (Plus Jakarta Sans latin, variabel)
import base64, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
def b64(fn):
    return base64.b64encode(open(os.path.join(HERE, fn), 'rb').read()).decode()

FIGURE_B64 = b64('figure_cut.webp')
FONT_B64 = b64('pjs-latin.woff2')

# ---------- Lucide icons (stroke-based, currentColor) ----------
def lucide(fn):
    s = open(os.path.join(HERE, 'assets', f'lucide-{fn}.svg')).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    inner = re.search(r'<svg\b[^>]*>(.*)</svg>', s, re.S).group(1)
    inner = re.sub(r'\s+', ' ', inner).strip()
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">{inner}</svg>')

LUCIDE = {k: lucide(k) for k in ('globe', 'mail', 'phone', 'house', 'sun', 'moon')}
LINKEDIN = ('<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0zM.3 8.2h4.4V24H.3zM8.6 8.2h4.2v2.2h.1c.6-1.1 2-2.3 4.2-2.3 4.5 0 5.3 3 5.3 6.8V24h-4.4v-7.9c0-1.9 0-4.3-2.6-4.3s-3 2-3 4.1V24H8.6z"/></svg>')

# ---------- Skill-Logos ----------
def si_path(fn):
    s = open(os.path.join(HERE, 'assets', f'si-{fn}.svg')).read()
    return re.search(r'<path d="([^"]+)"', s).group(1)

def tile(inner, bg):
    return (f'<svg viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="28" height="28" rx="6" fill="{bg}"/>{inner}</svg>')

def si_tile(fn, bg, fg, scale=0.79):
    off = (28 - 24 * scale) / 2
    return tile(f'<g transform="translate({off:.2f},{off:.2f}) scale({scale})">'
                f'<path d="{si_path(fn)}" fill="{fg}"/></g>', bg)

def adobe(letters, bg, fg):
    return tile(f'<text x="14" y="18.5" text-anchor="middle" font-family="\'Plus Jakarta Sans\',sans-serif" '
                f'font-size="11.5" font-weight="700" fill="{fg}">{letters}</text>', bg)

# Offizielles Figma-Logo (viewBox 0 0 38 57), skaliert in die 28er-Kachel
FIGMA = tile('<g transform="translate(8,5) scale(0.3158)">'
             '<path fill="#1ABCFE" d="M19 28.5c0-5.247 4.253-9.5 9.5-9.5s9.5 4.253 9.5 9.5-4.253 9.5-9.5 9.5-9.5-4.253-9.5-9.5z"/>'
             '<path fill="#0ACF83" d="M0 47.5C0 42.253 4.253 38 9.5 38H19v9.5c0 5.247-4.253 9.5-9.5 9.5S0 52.747 0 47.5z"/>'
             '<path fill="#FF7262" d="M19 0v19h9.5c5.247 0 9.5-4.253 9.5-9.5S33.747 0 28.5 0H19z"/>'
             '<path fill="#F24E1E" d="M0 9.5C0 14.747 4.253 19 9.5 19H19V0H9.5C4.253 0 0 4.253 0 9.5z"/>'
             '<path fill="#A259FF" d="M0 28.5C0 33.747 4.253 38 9.5 38H19V19H9.5C4.253 19 0 23.253 0 28.5z"/>'
             '</g>', '#2E2E2D')

GEMINI = tile('<defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="1">'
              '<stop offset="0" stop-color="#4285F4"/><stop offset=".55" stop-color="#9B72CB"/>'
              '<stop offset="1" stop-color="#D96570"/></linearGradient></defs>'
              f'<g transform="translate(2.26,2.26) scale(0.98)"><path d="{si_path("googlegemini")}" fill="url(#gg)"/></g>',
              '#FFFFFF')

# Google Antigravity: offizielles Mark (blaues, schwebendes A) von antigravity.google
AG_PATH = ('M89.6992 93.695C94.3659 97.195 101.366 94.8617 94.9492 88.445C75.6992 69.7783 79.7825 '
           '18.445 55.8659 18.445C31.9492 18.445 36.0325 69.7783 16.7825 88.445C9.78251 95.445 '
           '17.3658 97.195 22.0325 93.695C40.1159 81.445 38.9492 59.8617 55.8659 59.8617C72.7825 '
           '59.8617 71.6159 81.445 89.6992 93.695Z')
ANTIGRAVITY = tile(f'<g transform="translate(3.45,3.07) scale(0.19)"><path d="{AG_PATH}" fill="#3186FF"/></g>',
                   '#FFFFFF')

# Pitch: offizielles Mark von pitch.com
PITCH_PATH = ('M 26.58 12.713 C 26.283 16.726 23.089 20.355 18.984 20.521 L 18.984 17.484 C 18.978 14.697 '
              '17.002 12.304 14.267 11.77 L 4.09 9.793 L 4.09 2.935 C 4.09 2.058 4.482 1.228 5.158 0.67 '
              'C 5.835 0.112 6.725 -0.113 7.586 0.054 L 18.055 2.086 C 23.847 3.346 26.945 7.781 26.58 12.713 Z '
              'M 7.697 22.302 C 8.717 22.501 9.454 23.393 9.455 24.432 L 9.455 28.597 C 9.454 29.017 9.266 '
              '29.414 8.943 29.68 C 8.619 29.947 8.193 30.055 7.781 29.975 L 1.758 28.805 C 0.738 28.606 0 '
              '27.714 0 26.675 L 0 22.511 C 0 22.092 0.188 21.694 0.512 21.427 C 0.836 21.161 1.262 21.053 '
              '1.674 21.133 L 7.697 22.301 Z M 13.783 14.027 C 15.439 14.349 16.636 15.799 16.638 17.486 '
              'L 16.638 23.728 C 16.637 24.367 16.351 24.973 15.857 25.38 C 15.364 25.786 14.715 25.951 '
              '14.087 25.829 L 11.755 25.377 L 11.755 24.432 C 11.751 22.293 10.234 20.457 8.135 20.047 '
              'L 2.112 18.878 C 2.091 18.874 2.066 18.872 2.046 18.867 L 2.046 14.346 C 2.046 13.706 2.332 '
              '13.1 2.826 12.694 C 3.32 12.287 3.969 12.122 4.597 12.244 L 13.783 14.026 Z')
PITCH = tile(f'<g transform="translate(6.0,5.0) scale(0.6)"><path d="{PITCH_PATH}" fill="#FFFFFF"/></g>', '#1D1D1F')

SKILLS = [
    ('Adobe Photoshop',      adobe('Ps', '#001E36', '#31A8FF')),
    ('Adobe Illustrator',    adobe('Ai', '#330000', '#FF9A00')),
    ('Adobe InDesign',       adobe('Id', '#49021F', '#FF3366')),
    ('Adobe After Effects',  adobe('Ae', '#1F0740', '#9999FF')),
    ('Adobe Premiere',       adobe('Pr', '#00005B', '#9999FF')),
    ('Figma',                FIGMA),
    ('Claude Code',          si_tile('claude', '#262624', '#D97757')),
    ('Antigravity',          ANTIGRAVITY),
    ('Gemini',               GEMINI),
    ('Wix Studio',           si_tile('wix', '#0C6EFC', '#FFFFFF', scale=0.72)),
    ('Framer',               si_tile('framer', '#0F0F0F', '#FFFFFF', scale=0.62)),
    ('Pitch',                PITCH),
]

# ---------- Inhalte ----------
COMMON = dict(
    linkedin='linkedin.com/in/edgar-heinz/', site='edgarheinz.com',
    mail='eh.edgarheinz@gmail.com', phone='+49 176 7021 4158',
    addr='Am Schilfpark 12g<br>21029 Hamburg, Germany',
)

EN = dict(
    lang='en', other_file='../', other_label='DE',
    title='Edgar Heinz — Resume', print_label='Save as PDF',
    meta='Edgar Heinz — Senior Visual Designer from Hamburg. Resume: brand design, art direction, web design, and vibe coding.',
    hi="Hi, I&rsquo;m", role='Senior Visual Designer',
    h_exp='Professional experience', h_expertise='Expertise', h_skills='Skills',
    h_lang='Languages', h_edu='Education',
    expertise=['Art Direction','Creative Direction','Brand Design','Web Design','Advertising','Event Design','Vibe Coding'],
    langs=[('German','Native'),('English','Fluent'),('Russian','Basic')],
    edu=[('A-Levels','', 'Otto-Hahn-Gymnasium<br>Geesthacht, Germany','2001 – 2010'),
         ('Bachelor of Arts','Communication Design','University of Applied Sciences<br>Hamburg, Germany','2011 – 2016')],
    jobs=[
        ('June 2026 – today','Senior Brand Designer','at awork',
         "As Brand Lead, I own awork&rsquo;s visual identity and drive its continuous evolution — keeping the brand distinctive and recognisable in a crowded SaaS market. I set the art and creative direction across all touchpoints, from ads, web, and sales materials to events and content, and raise the bar for a cohesive, credible brand appearance. With clear guidelines, templates, and hands-on enablement, I empower the team to create on-brand independently — moving fast, without design bottlenecks."),
        ('December 2023 – June 2026','Design Lead','at halpy',
         "As Design Lead, I was responsible for creative and art direction across all touchpoints — print, digital, and web. I built digital products hands-on through vibe coding (app features, widgets, and more), shot and edited video content, and shaped halpy&rsquo;s social media presence. From first concept to final asset, I owned the company&rsquo;s entire visual output."),
        ('January 2021 – December 2023','Communication Design','at THINKS Design GmbH',
         "As a senior communication designer, I led a small team of working students and interns and coordinated internal as well as external projects — from planning and task distribution to design execution, client meetings, and the complete client communication. I was also responsible for the branding and packaging design of STRYVE, the company&rsquo;s in-house brand, and redesigned and maintained the THINKS Design website."),
        ('April 2017 – December 2020','Communication Design','at Wunder Mobility',
         "As the first designer in the marketing team, my primary task was to develop a holistic branding and a corresponding guideline for a uniform, authentic, and consistent brand appearance. By introducing an illustration style — used from then on in apps, websites, ads, and animations — I gave Wunder a distinctive, recognisable look. Beyond that, I was responsible for event design, advertising, web design, merchandise, animations, and presentations, with a growing focus on web design."),
        ('March 2016 – July 2017','Startup foundation','for Stickerbuddy',
         "To build a second foothold, I founded a start-up together with two friends. I took on conceptual work on the development and refinement of the business concept as well as all design-related tasks, such as creating the visual identity."),
        ('September 2015 – April 2017','Freelancing','for Mad About Hair &amp; TAM Fashion',
         "During this time I worked for various clients. My tasks included the conception and creation of visual identities, packaging design, web design, and retouching."),
        ('October 2011 – April 2017','Honorary employee','for the AWO at the Katharinenschule Hafencity',
         "During my studies, I volunteered for the AWO in the afternoon care of the Katharinenschule in Hamburg&rsquo;s Hafencity — supporting children (grades 1–4) through lunch, games, and homework, and later running my own courses for smaller groups, including &ldquo;Lego architecture&rdquo;, streetball, and drawing."),
        ('February 2013 – July 2013','Internship Art Direction','at Jung von Matt/Fleet',
         "During my internship in the creative department of Jung von Matt/Fleet, I developed and visually implemented compelling advertising ideas for well-known clients such as Sixt, GE, Edeka, Zalando, and Daimler. Working closely with the art directors, the creative director, and the management, I gained valuable agency experience."),
    ],
)

DE = dict(
    lang='de', other_file='en/', other_label='EN',
    title='Edgar Heinz — Lebenslauf', print_label='Als PDF speichern',
    meta='Edgar Heinz — Senior Visual Designer aus Hamburg. Lebenslauf: Brand Design, Art Direction, Webdesign und Vibe Coding.',
    hi='Hi, ich bin', role='Senior Visual Designer',
    h_exp='Berufserfahrung', h_expertise='Expertise', h_skills='Skills',
    h_lang='Sprachen', h_edu='Ausbildung',
    expertise=['Art Direction','Creative Direction','Brand Design','Webdesign','Advertising','Event Design','Vibe Coding'],
    langs=[('Deutsch','Muttersprache'),('Englisch','Fließend'),('Russisch','Grundkenntnisse')],
    edu=[('Abitur','','Otto-Hahn-Gymnasium<br>Geesthacht','2001 – 2010'),
         ('Bachelor of Arts','Kommunikationsdesign','Hochschule für Angewandte<br>Wissenschaften Hamburg','2011 – 2016')],
    jobs=[
        ('Juni 2026 – heute','Senior Brand Designer','bei awork',
         "Als Brand Lead verantworte ich die visuelle Identität von awork und entwickle sie kontinuierlich weiter — damit die Marke in einem dicht besetzten SaaS-Markt unverwechselbar und wiedererkennbar bleibt. Ich gebe die Art- und Creative Direction über alle Touchpoints vor, von Ads, Web und Sales-Materialien bis zu Events und Content, und sorge für einen konsistenten, glaubwürdigen Markenauftritt. Mit klaren Guidelines, Templates und Hands-on-Enablement befähige ich das Team, eigenständig on-brand zu arbeiten — schnell und ohne Design-Bottlenecks."),
        ('Dezember 2023 – Juni 2026','Design Lead','bei halpy',
         "Als Design Lead verantwortete ich die Creative- und Art Direction über alle Touchpoints — Print, Digital und Web. Per Vibe Coding habe ich digitale Produkte wie App-Features und Widgets hands-on gebaut, Videos gedreht und geschnitten und den Social-Media-Auftritt von halpy geprägt. Vom ersten Konzept bis zum finalen Asset lag der gesamte visuelle Output des Unternehmens in meiner Hand."),
        ('Januar 2021 – Dezember 2023','Communication Design','bei THINKS Design GmbH',
         "Als Senior Communication Designer habe ich ein kleines Team aus Werkstudenten und Praktikanten geführt und interne wie externe Projekte koordiniert — von Planung und Aufgabenverteilung über Design und Umsetzung bis zu Meetings und der kompletten Kundenkommunikation. Zusätzlich verantwortete ich Branding und Packaging Design der hauseigenen Marke STRYVE und habe die Website von THINKS Design neu gestaltet und betreut."),
        ('April 2017 – Dezember 2020','Communication Design','bei Wunder Mobility',
         "Als erster Designer im Marketing-Team war es meine Hauptaufgabe, ein ganzheitliches Branding samt Guideline für einen einheitlichen, authentischen und konsistenten Markenauftritt zu entwickeln. Mit der Einführung eines Illustrationsstils — fortan in Apps, Websites, Ads und Animationen im Einsatz — habe ich Wunder einen unverwechselbaren Look gegeben. Darüber hinaus verantwortete ich Event Design, Advertising, Webdesign, Merchandise, Animationen und Präsentationen — mit wachsendem Schwerpunkt auf Webdesign."),
        ('März 2016 – Juli 2017','Startup-Gründung','Stickerbuddy',
         "Um ein zweites Standbein aufzubauen, habe ich gemeinsam mit zwei Freunden ein Start-up gegründet. Ich übernahm konzeptionelle Aufgaben bei der Entwicklung und Schärfung des Geschäftskonzepts sowie alle designrelevanten Aufgaben — etwa die Gestaltung der visuellen Identität."),
        ('September 2015 – April 2017','Freelancing','für Mad About Hair &amp; TAM Fashion',
         "In dieser Zeit habe ich für verschiedene Kunden gearbeitet. Zu meinen Aufgaben gehörten Konzeption und Gestaltung visueller Identitäten, Packaging Design, Webdesign und Retusche."),
        ('Oktober 2011 – April 2017','Ehrenamtliche Tätigkeit','für die AWO an der Katharinenschule Hafencity',
         "Während meines Studiums habe ich mich bei der AWO in der Nachmittagsbetreuung der Katharinenschule in der Hamburger Hafencity engagiert — von der Begleitung der Kinder (Klasse 1–4) bei Mittagessen, Spielen und Hausaufgaben bis zu eigenen Kursen für kleinere Gruppen, darunter &bdquo;Lego-Architektur&ldquo;, Streetball und Zeichnen."),
        ('Februar 2013 – Juli 2013','Praktikum Art Direction','bei Jung von Matt/Fleet',
         "Im Rahmen meines Praktikums in der Kreation von Jung von Matt/Fleet habe ich für namhafte Kunden wie Sixt, GE, Edeka, Zalando und Daimler aussagekräftige Werbeideen entwickelt und visuell umgesetzt. In enger Zusammenarbeit mit den Art Directors, dem Creative Director und der Geschäftsführung konnte ich wertvolle Agenturerfahrung sammeln."),
    ],
)

CSS = '''
@font-face{
  font-family:'Plus Jakarta Sans';
  font-style:normal;
  font-weight:200 800;
  font-display:swap;
  src:url(data:font/woff2;base64,FONT_B64) format('woff2');
}
:root{
  --bg:#1b1b1a; --line:#3d3d3b; --accent:#f70059;
  --text:#f2f2f0; --soft:#dcdcda; --body:#e4e4e1; --muted:#a9a9a5;
  --chip:rgba(45,45,43,.92); --chip-border:#3d3d3b;
}
:root[data-theme="light"]{
  --bg:#f7f5f2; --line:#d9d6d0; --accent:#e80054;
  --text:#1d1d1b; --soft:#3c3c39; --body:#3a3a37; --muted:#75756f;
  --chip:rgba(255,255,255,.92); --chip-border:#d9d6d0;
}
*{margin:0;padding:0;box-sizing:border-box;}
html{background:var(--bg);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{
  font-family:'Plus Jakarta Sans','Avenir Next','Segoe UI',system-ui,sans-serif;
  background:var(--bg); color:var(--text); line-height:1.55; font-size:15px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
a{color:inherit;text-decoration:none;}
.page{max-width:960px;margin:0 auto;padding:0 40px 60px;}

/* action bar (screen only) */
.actions{position:fixed;top:16px;right:16px;display:flex;gap:8px;z-index:10;}
.actions a,.actions button{
  display:flex;align-items:center;gap:6px;
  font-family:inherit;font-size:13px;font-weight:600;letter-spacing:.02em;
  color:var(--text);background:var(--chip);border:1px solid var(--chip-border);
  border-radius:999px;padding:8px 14px;cursor:pointer;backdrop-filter:blur(6px);
}
.actions .primary{background:var(--accent);border-color:var(--accent);color:#fff;}
.actions a:hover,.actions button:hover{filter:brightness(1.1);}
.actions svg{width:16px;height:16px;}
:root[data-theme="light"] .icon-sun{display:none;}
:root:not([data-theme="light"]) .icon-moon{display:none;}

/* hero */
.hero{position:relative;padding-top:150px;}
.namewrap{width:fit-content;margin:0 auto;}
.hero .hi{font-size:26px;font-weight:500;color:var(--text);margin-bottom:2px;}
.hero h1{
  display:flex;gap:120px;
  font-size:96px;line-height:1;font-weight:800;color:var(--accent);
  letter-spacing:.005em;white-space:nowrap;
}
.hero .role{text-align:right;font-size:26px;font-weight:500;color:var(--text);margin-top:6px;}
.hero .figure{
  position:absolute;left:50%;bottom:-50px;transform:translateX(-50%);
  width:600px;max-width:none;z-index:2;pointer-events:none;
}
.hero .edge{border-bottom:1px solid var(--line);height:30px;}

/* columns */
.columns{display:grid;grid-template-columns:250px 1fr;gap:56px;padding-top:44px;}
h2{font-size:30px;font-weight:600;margin-bottom:10px;}
.rule{border-bottom:1px solid var(--line);margin-bottom:22px;}

/* sidebar */
.side section{margin-bottom:40px;}
.contact{list-style:none;margin-bottom:44px;}
.contact li{display:flex;align-items:flex-start;gap:14px;margin-bottom:16px;font-size:14.5px;}
.contact svg{width:19px;height:19px;flex:none;margin-top:2px;color:var(--soft);}
.plain{list-style:none;font-size:16px;}
.plain li{margin-bottom:10px;}
.skills{list-style:none;}
.skills li{display:flex;align-items:center;gap:11px;margin-bottom:11px;font-size:14.5px;}
.skills svg{width:26px;height:26px;flex:none;border-radius:6px;}
.langs{list-style:none;font-size:15px;}
.langs li{display:flex;justify-content:space-between;margin-bottom:9px;}
.langs .lvl{color:var(--muted);font-size:13.5px;}
.edu h3{font-size:17px;font-weight:700;line-height:1.3;}
.edu .sub{font-size:15px;color:var(--soft);}
.edu .inst{color:var(--muted);font-size:14px;margin-top:6px;padding-bottom:8px;}
.edu .years{font-weight:700;font-size:14px;margin-bottom:18px;}
.edu .item{border-bottom:1px solid var(--line);margin-bottom:14px;}
.edu .item:last-child{border-bottom:none;}

/* jobs */
.job{margin-bottom:34px;break-inside:avoid;}
.job .dates{color:var(--soft);font-size:15px;}
.job h3{color:var(--accent);font-size:27px;font-weight:700;line-height:1.15;margin:2px 0 0;}
.job .company{font-size:19px;font-weight:600;margin-bottom:10px;}
.job p{border-top:1px solid var(--line);padding-top:12px;color:var(--body);font-size:14.5px;}

@media screen and (max-width:760px){
  .hero{padding-top:110px;}
  .hero h1{font-size:44px;gap:56px;}
  .hero .hi{font-size:17px;}
  .hero .figure{width:300px;bottom:-25px;}
  .hero .role{font-size:15px;margin-top:4px;}
  .columns{grid-template-columns:1fr;gap:10px;}
}
@page{size:A4;margin:0;}
@media print{
  .actions{display:none;}
  body{font-size:13px;}
  .page{max-width:100%;padding:0 34px 0;}
  .hero{padding-top:60px;}
  /* Umbruch-Abstände: transparente Borders bleiben beim Seitenumbruch erhalten,
     Margins werden am Seitenanfang verworfen */
  .job{margin-bottom:0;border-top:30px solid transparent;}
  .side section{break-inside:avoid;margin-bottom:0;border-top:26px solid transparent;}
  .contact{margin-bottom:6px;}
  .columns{padding-top:26px;}
  .hero h1{font-size:62px;gap:78px;}
  .hero .hi{font-size:17px;}
  .hero .role{font-size:17px;margin-top:4px;}
  .hero .figure{width:390px;bottom:-32px;}
  .hero .edge{height:22px;}
  .columns{grid-template-columns:200px 1fr;gap:36px;padding-top:30px;}
  h2{font-size:24px;}
  .job h3{font-size:21px;}
  .job .company{font-size:16px;}
  .job p{font-size:12.5px;}
  .contact li{font-size:12px;margin-bottom:12px;}
  .skills li{font-size:12px;}
  .skills svg{width:22px;height:22px;}
  .plain{font-size:13px;}
}
'''.replace('FONT_B64', FONT_B64)

SCRIPT = '''
(function(){
  var r=document.documentElement;
  try{
    var saved=localStorage.getItem('cv-theme');
    if(saved==='light'||saved==='dark'){ if(saved==='light') r.dataset.theme='light'; }
  }catch(e){}
  document.getElementById('themeToggle').addEventListener('click',function(){
    var light = r.dataset.theme==='light';
    if(light){ delete r.dataset.theme; } else { r.dataset.theme='light'; }
    try{ localStorage.setItem('cv-theme', light?'dark':'light'); }catch(e){}
  });
})();
'''

def render(c):
    exp_items = ''.join(f'<li>{e}</li>' for e in c['expertise'])
    skill_items = ''.join(f'<li>{svg}<span>{n}</span></li>' for n, svg in SKILLS)
    lang_items = ''.join(f'<li><span>{l}</span><span class="lvl">{v}</span></li>' for l, v in c['langs'])
    edu_items = ''.join(
        f'<div class="item"><h3>{t}</h3>' + (f'<div class="sub">{s}</div>' if s else '') +
        f'<div class="inst">{i}</div><div class="years">{y}</div></div>'
        for t, s, i, y in c['edu'])
    job_items = ''.join(
        f'<article class="job"><div class="dates">{d}</div><h3>{t}</h3>'
        f'<div class="company">{co}</div><p>{txt}</p></article>'
        for d, t, co, txt in c['jobs'])

    return f'''<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{c['meta']}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23f70059'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='sans-serif' font-size='14' font-weight='800' fill='white'%3EEH%3C/text%3E%3C/svg%3E">
<title>{c['title']}</title>
<style>{CSS}</style>
</head>
<body>
<div class="actions">
  <a href="{c['other_file']}">{c['other_label']}</a>
  <button id="themeToggle" aria-label="Toggle theme">
    <span class="icon-sun">{LUCIDE['sun']}</span>
    <span class="icon-moon">{LUCIDE['moon']}</span>
  </button>
  <button class="primary" onclick="window.print()">{c['print_label']}</button>
</div>
<div class="page">
  <header class="hero">
    <div class="namewrap">
      <div class="hi">{c['hi']}</div>
      <h1><span>Edgar</span><span>Heinz</span></h1>
      <div class="role">{c['role']}</div>
    </div>
    <img class="figure" src="data:image/webp;base64,{FIGURE_B64}" alt="Edgar Heinz">
    <div class="edge"></div>
  </header>
  <div class="columns">
    <aside class="side">
      <ul class="contact">
        <li>{LINKEDIN}<a href="https://www.linkedin.com/in/edgar-heinz/">{COMMON['linkedin']}</a></li>
        <li>{LUCIDE['globe']}<a href="https://edgarheinz.com">{COMMON['site']}</a></li>
        <li>{LUCIDE['mail']}<a href="mailto:{COMMON['mail']}">{COMMON['mail']}</a></li>
        <li>{LUCIDE['phone']}<a href="tel:+4917670214158">{COMMON['phone']}</a></li>
        <li>{LUCIDE['house']}<span>{COMMON['addr']}</span></li>
      </ul>
      <section>
        <h2>{c['h_expertise']}</h2><div class="rule"></div>
        <ul class="plain">{exp_items}</ul>
      </section>
      <section>
        <h2>{c['h_skills']}</h2><div class="rule"></div>
        <ul class="skills">{skill_items}</ul>
      </section>
      <section>
        <h2>{c['h_lang']}</h2><div class="rule"></div>
        <ul class="langs">{lang_items}</ul>
      </section>
      <section class="edu">
        <h2>{c['h_edu']}</h2><div class="rule"></div>
        {edu_items}
      </section>
    </aside>
    <main>
      <h2>{c['h_exp']}</h2>
      {job_items}
    </main>
  </div>
</div>
<script>{SCRIPT}</script>
</body>
</html>'''

OUT = '/Users/edgarheinz/Projects/Lebenslauf/docs'
os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(render(DE))
open(os.path.join(OUT, 'en', 'index.html'), 'w', encoding='utf-8').write(render(EN))
print('written to docs/')
