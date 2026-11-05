# -*- coding: utf-8 -*-
# Generiert die CV-Seite (DE: docs/index.html, EN: docs/en/index.html) im Stil von edgarheinz.com
# Benötigt: figure_cut.webp (Kopf+Hände-Freisteller), pjs-latin.woff2 (Plus Jakarta Sans latin, variabel)
# python3 build.py         schreibt die beiden Seiten
# python3 build.py --pdf   schreibt zusätzlich die beiden PDFs (braucht Google Chrome)
import base64, re, os, subprocess, sys, urllib.parse

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
    return line(inner)

# Strichstärke 1.5 wie die Icons auf edgarheinz.com
def line(inner):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')

ICON = {k: lucide(k) for k in ('globe', 'phone', 'house')}
# dieselben Zeichnungen wie auf der Website (assets/js/main.js)
ICON.update(
    mail=line('<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/>'),
    linkedin=line('<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 11v6M8 7.5v.01M12 17v-3.5a2.5 2.5 0 0 1 5 0V17M12 11v6"/>'),
    moon=line('<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>'),
    sun=line('<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4l1.4-1.4M17 7l1.4-1.4"/>'),
    download=line('<path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/>'),
    arrow=('<svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"/></svg>'),
)

# Bildmarke von edgarheinz.com (Lächeln + Brille)
LOGO_SMILE = 'M13.16,22.5c-3.47.01-6.87-1.39-9.32-3.86l3.38-3.38c3.13,3.26,8.75,3.26,11.88,0l3.38,3.38c-2.45,2.47-5.85,3.87-9.32,3.86Z'
LOGO_GLASSES = 'M25.3,4.19C24.64,2.62,23.69,1.21,22.48,0l-3.38,3.38c.99.98,1.73,2.22,2.12,3.55H5.1c.39-1.34,1.13-2.57,2.12-3.55L3.84,0C.76,3-.53,7.49.2,11.71h25.92c.37-2.48.23-5.22-.82-7.52Z'
LOGO = ('<svg class="logo" viewBox="0 0 26.31 22.5" fill="currentColor" aria-hidden="true">'
        f'<path class="logo-smile" d="{LOGO_SMILE}"/><path d="{LOGO_GLASSES}"/></svg>')
FAVICON = 'data:image/svg+xml,' + urllib.parse.quote(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#fff"/>'
    f'<g transform="translate(14.5,17) scale(1.33)" fill="#1f1f1f"><path d="{LOGO_SMILE}"/><path d="{LOGO_GLASSES}"/></g></svg>')

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

# Wix Studio: offizielles App-Icon (Favicon von wix.com/studio) — schwarze Kachel mit Gradient-Kugel
WIXSTUDIO = tile('<defs><linearGradient id="wxs" gradientUnits="userSpaceOnUse" x1="13.58" y1="3.37" x2="13.58" y2="36.2">'
                 '<stop stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#0051EE"/></linearGradient></defs>'
                 '<circle cx="13.58" cy="14" r="10.63" fill="url(#wxs)"/>', '#000000')

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
    ('Wix Studio',           WIXSTUDIO),
    ('Framer',               si_tile('framer', '#0F0F0F', '#FFFFFF', scale=0.62)),
    ('Pitch',                PITCH),
]

# ---------- Inhalte ----------
# Texte ohne Gedankenstriche (nur Bis-Striche in Zeiträumen). Bereiche heißen wie auf der Website.
# Expertise: das Wichtigste zuerst, immer zwei Pills pro Zeile (je zwei aufeinanderfolgende bilden ein Paar).
# Ein Paar muss in die schmalste Seitenspalte passen (PDF 204 px, Tablet 256 px), am breitesten ist
# Art Direction + Creative Direction.
COMMON = dict(
    linkedin='linkedin.com/in/edgar-heinz/', site='edgarheinz.com',
    mail='hi@edgarheinz.com', phone='+49 176 7021 4158',
    addr='Am Schilfpark 12g<br>21029 Hamburg, Germany',
)

EN = dict(
    lang='en', home='../', de_href='../', en_href='./', canonical='https://cv.edgarheinz.com/en/',
    title='Resume | Edgar Heinz',
    pdf_label='Save as PDF', pdf_short='PDF', pdf_file='../Edgar-Heinz-Resume.pdf',
    theme_label='Dark mode', lang_label='Language', logo_label='To the portfolio',
    meta='Edgar Heinz, Senior Visual Designer from Hamburg. Resume: brand design, art direction, web design, and vibe coding.',
    hi="Hi, I&rsquo;m", role='Senior Visual Designer',
    h_exp='Professional experience', h_contact='Contact', h_expertise='Expertise', h_skills='Skills',
    h_lang='Languages', h_edu='Education',
    expertise=['Art Direction','Creative Direction','Brand Design','Web Design','Packaging','Print Design','Advertising','Event Design',
               'Illustration','Presentations','Motion Design','Video','Social Media','Vibe Coding'],
    langs=[('German','Native'),('English','Fluent'),('Russian','Basic')],
    edu=[('Bachelor of Arts','Communication Design','University of Applied Sciences<br>Hamburg, Germany','2011 – 2016'),
         ('A-Levels','', 'Otto-Hahn-Gymnasium<br>Geesthacht, Germany','2001 – 2010')],
    cta_tag='Available for new projects', cta_a="Let&rsquo;s", cta_b='Connect',
    cta_text='Got a project in mind or just a question? Drop me a line.',
    cta_mail='Get in touch', cta_site='View portfolio',
    jobs=[
        ('November 2026 – today','Freelance Designer','Self-employed',
         "As a freelance designer, I support companies with everything that makes their brand visible: from brand identity and website to packaging, print, and campaigns. One point of contact for everything, with websites and tools built through vibe coding if needed."),
        ('June 2026 – September 2026','Senior Brand Designer','at awork',
         "As Brand Lead, I owned awork&rsquo;s visual identity and drove its continuous evolution, keeping the brand distinctive and recognisable in a crowded SaaS market. I set the art and creative direction across all touchpoints, from ads, web, and sales materials to events and content, and raised the bar for a cohesive, credible brand appearance. With clear guidelines, templates, and hands-on enablement, I empowered the team to create on-brand independently: fast and without design bottlenecks."),
        ('December 2023 – May 2026','Design Lead','at halpy',
         "As Design Lead, I was responsible for creative and art direction across all touchpoints: print, digital, and web. I built digital products hands-on through vibe coding (app features, widgets, and more), shot and edited video content, and shaped halpy&rsquo;s social media presence. From first concept to final asset, I owned the company&rsquo;s entire visual output."),
        ('January 2021 – December 2023','Senior Communication Designer','at THINKS Design GmbH',
         "As a senior communication designer, I led a small team of working students and interns and coordinated internal as well as external projects, from planning and task distribution to design execution, client meetings, and the complete client communication. I was also responsible for the branding and packaging design of STRYVE, the company&rsquo;s in-house brand, and redesigned and maintained the THINKS Design website."),
        ('April 2017 – December 2020','Communication Designer','at Wunder Mobility',
         "As the first designer in the marketing team, my primary task was to develop a holistic branding and a corresponding guideline for a uniform, authentic, and consistent brand appearance. By introducing an illustration style that was used from then on in apps, websites, ads, and animations, I gave Wunder a distinctive, recognisable look. Beyond that, I was responsible for event design, advertising, web design, merchandise, animations, and presentations, with a growing focus on web design."),
        ('March 2016 – July 2017','Startup foundation','for Stickerbuddy',
         "To build a second foothold, I founded a start-up together with two friends. I took on conceptual work on the development and refinement of the business concept as well as all design-related tasks, such as creating the visual identity."),
        ('September 2015 – April 2017','Image editing &amp; retouching','at TAM Fashion (mini job)',
         "In a mini job, I handled image editing and retouching for TAM Fashion."),
        ('October 2011 – April 2017','After-school care worker','for the AWO at the Katharinenschule Hafencity',
         "During my studies, I worked for the AWO on a freelance basis in the after-school care of the Katharinenschule in Hamburg&rsquo;s Hafencity: supporting children (grades 1–4) through lunch, games, and homework, and later running my own courses for smaller groups, including &ldquo;Lego architecture&rdquo;, streetball, and drawing."),
        ('February 2013 – July 2013','Internship Art Direction','at Jung von Matt/Fleet',
         "During my internship in the creative department of Jung von Matt/Fleet, I developed and visually implemented compelling advertising ideas for well-known clients such as Sixt, GE, Edeka, Zalando, and Daimler. Working closely with the art directors, the creative director, and the management, I gained valuable agency experience."),
    ],
)

DE = dict(
    lang='de', home='./', de_href='./', en_href='en/', canonical='https://cv.edgarheinz.com/',
    title='Lebenslauf | Edgar Heinz',
    pdf_label='Als PDF speichern', pdf_short='PDF', pdf_file='Edgar-Heinz-Lebenslauf.pdf',
    theme_label='Dunkles Design', lang_label='Sprache', logo_label='Zum Portfolio',
    meta='Edgar Heinz, Senior Visual Designer aus Hamburg. Lebenslauf: Brand Design, Art Direction, Webdesign und Vibe Coding.',
    hi='Hi, ich bin', role='Senior Visual Designer',
    h_exp='Berufserfahrung', h_contact='Kontakt', h_expertise='Expertise', h_skills='Skills',
    h_lang='Sprachen', h_edu='Ausbildung',
    expertise=['Art Direction','Creative Direction','Brand Design','Webdesign','Packaging','Printdesign','Werbung','Eventdesign',
               'Illustration','Präsentationen','Motion Design','Video','Social Media','Vibe Coding'],
    langs=[('Deutsch','Muttersprache'),('Englisch','Fließend'),('Russisch','Grundkenntnisse')],
    edu=[('Bachelor of Arts','Kommunikationsdesign','Hochschule für Angewandte<br>Wissenschaften Hamburg','2011 – 2016'),
         ('Abitur','','Otto-Hahn-Gymnasium<br>Geesthacht','2001 – 2010')],
    cta_tag='Offen für neue Projekte', cta_a='Lass uns', cta_b='sprechen',
    cta_text='Du hast ein Projekt im Kopf oder einfach eine Frage? Schreib mir.',
    cta_mail='Kontakt aufnehmen', cta_site='Zum Portfolio',
    jobs=[
        ('November 2026 – heute','Freiberuflicher Designer','Selbstständig',
         "Als freiberuflicher Designer begleite ich Unternehmen bei allem, was ihre Marke sichtbar macht: vom Markenauftritt über die Website bis zu Verpackung, Print und Kampagnen. Ein Ansprechpartner für alles, auf Wunsch auch mit Websites und Tools per Vibe Coding."),
        ('Juni 2026 – September 2026','Senior Brand Designer','bei awork',
         "Als Brand Lead verantwortete ich die visuelle Identität von awork und entwickelte sie kontinuierlich weiter, damit die Marke in einem dicht besetzten SaaS-Markt unverwechselbar und wiedererkennbar bleibt. Ich gab die Art- und Creative Direction über alle Touchpoints vor, von Ads, Web und Sales-Materialien bis zu Events und Content, und sorgte für einen konsistenten, glaubwürdigen Markenauftritt. Mit klaren Guidelines, Templates und Hands-on-Enablement befähigte ich das Team, eigenständig on-brand zu arbeiten: schnell und ohne Design-Bottlenecks."),
        ('Dezember 2023 – Mai 2026','Design Lead','bei halpy',
         "Als Design Lead verantwortete ich die Creative- und Art Direction über alle Touchpoints: Print, Digital und Web. Per Vibe Coding habe ich digitale Produkte wie App-Features und Widgets hands-on gebaut, Videos gedreht und geschnitten und den Social-Media-Auftritt von halpy geprägt. Vom ersten Konzept bis zum finalen Asset lag der gesamte visuelle Output des Unternehmens in meiner Hand."),
        ('Januar 2021 – Dezember 2023','Senior Communication Designer','bei THINKS Design GmbH',
         "Als Senior Communication Designer habe ich ein kleines Team aus Werkstudenten und Praktikanten geführt und interne wie externe Projekte koordiniert, von Planung und Aufgabenverteilung über Design und Umsetzung bis zu Meetings und der kompletten Kundenkommunikation. Zusätzlich verantwortete ich Branding und Packaging Design der hauseigenen Marke STRYVE und habe die Website von THINKS Design neu gestaltet und betreut."),
        ('April 2017 – Dezember 2020','Communication Designer','bei Wunder Mobility',
         "Als erster Designer im Marketing-Team war es meine Hauptaufgabe, ein ganzheitliches Branding samt Guideline für einen einheitlichen, authentischen und konsistenten Markenauftritt zu entwickeln. Mit der Einführung eines Illustrationsstils, der fortan in Apps, Websites, Ads und Animationen im Einsatz war, habe ich Wunder einen unverwechselbaren Look gegeben. Darüber hinaus verantwortete ich Eventdesign, Werbung, Webdesign, Merchandise, Animationen und Präsentationen, mit wachsendem Schwerpunkt auf Webdesign."),
        ('März 2016 – Juli 2017','Startup-Gründung','Stickerbuddy',
         "Um ein zweites Standbein aufzubauen, habe ich gemeinsam mit zwei Freunden ein Start-up gegründet. Ich übernahm konzeptionelle Aufgaben bei der Entwicklung und Schärfung des Geschäftskonzepts sowie alle designrelevanten Aufgaben, etwa die Gestaltung der visuellen Identität."),
        ('September 2015 – April 2017','Bildbearbeitung &amp; Retusche','bei TAM Fashion (Minijob)',
         "Im Minijob habe ich für TAM Fashion Bildbearbeitung und Retusche übernommen."),
        ('Oktober 2011 – April 2017','Honorarkraft','bei der AWO an der Katharinenschule Hafencity',
         "Während meines Studiums habe ich bei der AWO in der Nachmittagsbetreuung der Katharinenschule in der Hamburger Hafencity gearbeitet: von der Begleitung der Kinder (Klasse 1–4) bei Mittagessen, Spielen und Hausaufgaben bis zu eigenen Kursen für kleinere Gruppen, darunter &bdquo;Lego-Architektur&ldquo;, Streetball und Zeichnen."),
        ('Februar 2013 – Juli 2013','Praktikum Art Direction','bei Jung von Matt/Fleet',
         "Im Rahmen meines Praktikums in der Kreation von Jung von Matt/Fleet habe ich für namhafte Kunden wie Sixt, GE, Edeka, Zalando und Daimler aussagekräftige Werbeideen entwickelt und visuell umgesetzt. In enger Zusammenarbeit mit den Art Directors, dem Creative Director und der Geschäftsführung konnte ich wertvolle Agenturerfahrung sammeln."),
    ],
)

# ---------- Gestaltung: Farben, Schrift, Flächen und Bausteine wie auf edgarheinz.com ----------
CSS = '''
@font-face{
  font-family:"Plus Jakarta Sans";
  font-style:normal;
  font-weight:200 800;
  font-display:swap;
  src:url(data:font/woff2;base64,FONT_B64) format("woff2");
}
:root{
  --bg:#e8e8e8; --ink:#000; --body:rgba(0,0,0,.72); --muted:rgba(0,0,0,.5); --faint:rgba(0,0,0,.25); --hairline:rgba(0,0,0,.1);
  --accent:#ff3700; --accent-tint:#ffe8e0;
  --surface:#fff; --card:#f4f4f4;
  --solid:#000; --on-solid:#fff; --solid-hover:#3d3d3d;
  --edge:rgba(0,0,0,.06); --halo:rgba(255,255,255,.25); --logo:#1f1f1f;
  --bg-glow:#f8f8f8; --beam:1; --noise:.05; --noise-filter:none;
  --font:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --gutter:clamp(24px,8.33vw,120px); --max:1200px;
  --ring:0 0 0 8px var(--halo),12px 16px 16px rgba(0,0,0,.1);
  --btn-drop:.57px .57px 1.76px -.42px rgba(0,0,0,.18),1.45px 1.45px 4.5px -.83px rgba(0,0,0,.18),2.9px 2.9px 9.01px -1.25px rgba(0,0,0,.18),5.49px 5.49px 17.09px -1.67px rgba(0,0,0,.18),10.92px 10.92px 33.97px -2.08px rgba(0,0,0,.18),24px 24px 74.67px -2.5px rgba(0,0,0,.18);
  --btn-glow:inset 0 -16px 48px 0 #000;
  --btn-shadow:var(--btn-drop),var(--btn-glow);
  --ease:cubic-bezier(.22,1,.36,1);
}
/* Dunkles Design: hell ist Standard, gedruckt wird immer hell */
@media screen{
  :root[data-theme="dark"]{
    color-scheme:dark;
    --bg:#121212; --ink:#f4f4f4; --body:rgba(255,255,255,.75); --muted:rgba(255,255,255,.55); --faint:rgba(255,255,255,.22); --hairline:rgba(255,255,255,.1);
    --accent-tint:#3b1a0f;
    --surface:#2a2a2a; --card:#1e1e1e;
    --solid:#fff; --on-solid:#000; --solid-hover:#d6d6d6;
    --edge:rgba(255,255,255,.08); --halo:rgba(255,255,255,.05); --logo:#fff;
    --bg-glow:#1f1f1f; --beam:.05; --noise:.07; --noise-filter:invert(1);
    --ring:0 0 0 8px var(--halo),12px 16px 16px rgba(0,0,0,.3);
    --btn-shadow:var(--btn-drop);
  }
  :root[data-theme="dark"] .page-bg{
    height:100vh;
    background:radial-gradient(100% 100% at 0% 0%,#3d3d3d 0%,var(--bg) 100%);
    -webkit-mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
    mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
  }
  :root[data-theme="dark"] .page-bg .beams{-webkit-mask-image:none;mask-image:none;}
  /* der Abschluss kehrt sich um: am Ende der dunklen Seite steht eine helle Fläche */
  :root[data-theme="dark"] .dark-panel{
    --panel:#e8e8e8; --panel-ink:#000; --panel-muted:rgba(0,0,0,.5); --panel-line:rgba(0,0,0,.25);
    --panel-glow:#fff; --panel-beam:1; --panel-noise:.05; --panel-noise-filter:none; --panel-wrap:#fff;
    --solid:#000; --on-solid:#fff; --solid-hover:#3d3d3d; --btn-shadow:var(--btn-drop),var(--btn-glow);
  }
}
*,*::before,*::after{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;background:var(--bg);}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:400 16px/1.7 var(--font); word-spacing:.06em;
  -webkit-font-smoothing:antialiased; overflow-x:clip;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3,p,ul{margin:0;padding:0;}
ul{list-style:none;}
img{display:block;max-width:100%;}
svg{display:block;width:100%;height:100%;}
a{color:inherit;text-decoration:none;}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;}
::selection{background:var(--accent);color:#fff;}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;}
.muted{color:var(--muted);}

/* ---------- Hintergrund: Körnung und schräge Lichtstreifen ---------- */
.noise{
  position:fixed; inset:0; z-index:0; opacity:var(--noise); filter:var(--noise-filter); pointer-events:none;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='256'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0'/%3E%3C/filter%3E%3Crect width='256' height='256' filter='url(%23n)'/%3E%3C/svg%3E");
}
.page-bg{
  position:absolute; inset:0 0 auto 0; height:1800px; z-index:0; overflow:hidden; pointer-events:none;
  background:linear-gradient(225deg,var(--bg-glow) 0%,var(--bg) 70%);
  -webkit-mask-image:linear-gradient(#000 0%,#000 50%,transparent 100%);
  mask-image:linear-gradient(#000 0%,#000 50%,transparent 100%);
}
.beams span{
  position:absolute; top:-209px; left:calc(var(--x) - var(--w) / 2); width:var(--w); height:1269px;
  background:linear-gradient(#fff 0%,#fff 84%,rgba(255,255,255,0) 100%);
  transform:skewX(45deg); opacity:var(--beam);
  -webkit-mask-image:var(--m); mask-image:var(--m);
}
.beams span:nth-child(1){--x:33.6%;--w:591px;--m:linear-gradient(90deg,transparent 0%,#000 20%,transparent 36.2%,#000 55.4%,rgba(0,0,0,.13) 67.1%,#000 78.2%,transparent 97.3%);}
.beams span:nth-child(2){--x:-1.5%;--w:582px;--m:linear-gradient(90deg,transparent 11.4%,#000 25.6%,rgba(0,0,0,.55) 41.7%,rgba(0,0,0,.13) 67.1%,#000 78.2%,transparent 97.3%);}
.beams span:nth-child(3){--x:33.7%;--w:441px;background:linear-gradient(#fff 0%,#fff 67%,rgba(255,255,255,0) 100%);--m:linear-gradient(90deg,transparent 9.8%,#000 20%,rgba(0,0,0,.55) 28.6%,rgba(0,0,0,.42) 40.1%,#000 48.6%,rgba(0,0,0,.27) 54.5%,rgba(0,0,0,.13) 78.6%,#000 88.6%,transparent 97.3%);}
.beams span:nth-child(4){--x:50.1%;--w:684px;--m:linear-gradient(90deg,transparent 0%,#000 17.7%,rgba(0,0,0,.55) 26.6%,#000 35.2%,transparent 47.7%,rgba(0,0,0,.13) 69.2%,#000 79.1%,transparent 97.3%);}
.beams span:nth-child(5){--x:49.1%;--w:426px;--m:linear-gradient(90deg,transparent 0%,#000 20%,rgba(0,0,0,.55) 27.6%,#000 42.3%,transparent 48.6%,rgba(0,0,0,.13) 67.1%,#000 75%,#000 82.4%,rgba(0,0,0,.47) 88.7%,transparent 97.3%);}
@media (max-width:809px){
  .beams span:nth-child(1){--x:113.8%;--w:438px;}
  .beams span:nth-child(2){--x:87.7%;--w:432px;}
  .beams span:nth-child(3){--x:113.8%;--w:327px;}
  .beams span:nth-child(4){--x:125.9%;--w:507px;}
  .beams span:nth-child(5){--x:125.1%;--w:316px;}
}
.page-bg .beams{
  position:absolute; inset:0 0 auto 0; height:200vh;
  -webkit-mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
  mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
}

/* ---------- Kopfleiste ---------- */
.nav{position:fixed;inset:0 0 auto 0;z-index:20;padding-inline:var(--gutter);pointer-events:none;}
.nav-inner{display:flex;align-items:center;justify-content:space-between;max-width:var(--max);height:80px;margin-inline:auto;}
.nav-inner > *{pointer-events:auto;}
.wordmark{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--surface);color:var(--logo);}
.wordmark .logo{width:24px;height:auto;overflow:visible;}
.logo-smile{transform-box:fill-box;transform-origin:center;transition:transform .5s var(--ease);}
.wordmark:hover .logo-smile{transform:scaleX(1.14) translateY(1px);}
.nav-right{display:flex;align-items:center;gap:8px;}
.lang{display:flex;gap:2px;height:44px;padding:4px;border-radius:22px;background:var(--surface);}
.lang a{display:grid;place-items:center;min-width:40px;padding-inline:10px;border-radius:18px;font-size:13px;font-weight:600;line-height:1;color:var(--muted);word-spacing:0;transition:background .2s,color .2s;}
.lang a:hover{color:var(--ink);}
.lang a[aria-current="true"]{background:var(--solid);color:var(--on-solid);}
.theme-btn{position:relative;width:44px;height:44px;border-radius:50%;background:var(--surface);}
.theme-btn svg{position:absolute;inset:12px;width:20px;height:20px;transition:opacity .3s,transform .5s var(--ease);}
.theme-btn .i-sun,[data-theme="dark"] .theme-btn .i-moon{opacity:0;transform:rotate(-90deg) scale(.5);}
[data-theme="dark"] .theme-btn .i-sun{opacity:1;transform:none;}

/* ---------- Buttons ---------- */
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  padding:12px 20px 12px 24px;border-radius:154px;background:var(--solid);color:var(--on-solid);
  font-weight:500;line-height:1.7;white-space:nowrap;box-shadow:var(--btn-shadow);transition:background .3s;
}
.btn:hover{background:var(--solid-hover);}
.btn svg{width:20px;height:20px;opacity:.5;transition:transform .35s var(--ease),opacity .2s;}
.btn:hover svg{opacity:1;transform:translateX(3px);}
.btn--nav{height:44px;padding:0 16px 0 20px;font-size:14px;box-shadow:none;}
.btn--nav svg{width:18px;height:18px;opacity:.7;}
.btn--nav:hover svg{transform:translateY(2px);}
.btn--nav .short{display:none;}
.btn--outline{background:transparent;color:var(--panel-ink);box-shadow:inset 0 0 0 1px var(--panel-line);}
.btn--outline:hover{background:var(--panel-ink);color:var(--panel);}

/* ---------- Typo ---------- */
.display{font:600 clamp(44px,7.5vw,108px)/1.15 var(--font);letter-spacing:-.06em;}
.tag{
  display:flex;align-items:center;justify-content:center;gap:24px;padding-inline:24px;
  font:500 18px/1.2 var(--font);word-spacing:0;color:var(--muted);white-space:nowrap;
}
.tag::before,.tag::after{content:"";flex:0 1 69px;min-width:24px;height:1px;opacity:.5;background:linear-gradient(90deg,rgba(84,84,84,0),var(--muted));}
.tag::after{transform:scaleX(-1);}
.tag--light{color:var(--panel-muted);}
.tag--light::before,.tag--light::after{background:linear-gradient(90deg,rgba(84,84,84,0),var(--panel-ink));}

/* ---------- Kopf: Name, Edgar schaut über die Kante der Karte ---------- */
main{position:relative;z-index:1;padding-inline:var(--gutter);}
.container{position:relative;width:100%;max-width:var(--max);margin-inline:auto;}
.hero{padding-top:150px;}
/* Raster aus zwei Spalten mit Platz für den Kopf dazwischen: Die Lücke ist so breit wie der Kopf samt
   Ohren (1,52 × Schriftgröße) plus Luft, und der Block ist so weit nach links gerückt, dass „Edgar" und
   „Heinz" gleich weit von den Ohren entfernt stehen (der Vorname ist breiter als der Nachname).
   Optischer Ausgleich: Das „r" ist unten offen und wirkt dadurch weiter weg als das „H", deshalb steht
   „Edgar" 0,1 × Schriftgröße näher am Kopf (Lücke 1,67 statt 1,77, Versatz −0,053 statt −0,103).
   Die Rolle zählt nicht zur Spaltenbreite. „Hi" und Rolle schließen bündig mit den Buchstaben darunter
   bzw. darüber ab: Die großen Buchstaben haben mehr Vorbreite als die kleinen. */
.namewrap{
  --name:104px;
  display:grid;grid-template-columns:auto auto;column-gap:calc(var(--name) * 1.67);
  position:relative;left:calc(var(--name) * -.053);
  width:fit-content;margin:0 auto;font:inherit;
}
.namewrap .n{font:600 var(--name)/1 var(--font);letter-spacing:-.06em;word-spacing:0;white-space:nowrap;}
.hi,.role{font-size:24px;font-weight:500;line-height:1.3;letter-spacing:-.02em;color:var(--muted);}
/* n und z stehen bei dieser Laufweite zu eng */
.n2 .z{margin-left:.04em;}
.hi{grid-area:1/1;margin-bottom:2px;margin-left:calc(var(--name) * .077 - .08em);}
.n1{grid-area:2/1;}
.n2{grid-area:2/2;}
/* rechtsbündig mit dem z: Breite 0, der Text läuft nach links über */
.role{grid-area:3/2;justify-self:end;display:flex;justify-content:flex-end;width:0;margin-top:8px;margin-right:calc(var(--name) * -.043 + .03em);white-space:nowrap;}
/* Die Tischkante im Bild liegt auf der Oberkante der Karte; die Bildbreite folgt der Schriftgröße */
.sheet-wrap{position:relative;margin-top:34px;--name:104px;}
.figure{
  position:absolute;left:50%;bottom:100%;z-index:2;width:calc(var(--name) * 5.77);height:auto;max-width:none;
  transform:translate(-50%,17.64%);pointer-events:none;
}
.sheet{
  /* deckend, damit die Lichtstreifen hinter der Karte bleiben */
  padding:64px 60px 72px;border-radius:24px;background:var(--card);box-shadow:var(--ring);
}
.columns{display:grid;grid-template-columns:280px minmax(0,1fr);gap:72px;align-items:start;}

/* ---------- Seitenspalte ---------- */
.side{display:flex;flex-direction:column;gap:44px;}
/* Überschriften der Seitenspalte: kleiner als „Berufserfahrung" (24 zu 32 px), aber mit demselben Abstand
   von der Grundlinie zur Linie; die erste ist so weit heruntergerückt, dass Grundlinie und Linie auf
   einer Höhe mit der Hauptspalte liegen */
.side h2{font-size:24px;font-weight:600;line-height:1.3;letter-spacing:-.03em;padding-bottom:26px;margin-bottom:20px;border-bottom:1px solid var(--hairline);}
.contact-box h2{padding-top:8.5px;}
.contact{display:flex;flex-direction:column;gap:12px;}
.contact li{display:flex;align-items:center;gap:14px;font-size:14px;line-height:1.5;}
.contact i{flex:none;display:grid;place-items:center;width:36px;height:36px;padding:9px;border-radius:50%;background:var(--accent-tint);color:var(--accent);transition:background .35s var(--ease),color .35s var(--ease),transform .35s var(--ease);}
.contact li:hover i{background:var(--accent);color:#fff;transform:rotate(-8deg) scale(1.06);}
.contact a{transition:color .2s;}
/* immer zwei Pills pro Zeile; nur wenn ein Paar auf ganz kleinen Handys nicht passt, bricht es um */
.pills{display:flex;flex-direction:column;align-items:flex-start;gap:6px;}
.pills .pair{display:flex;flex-wrap:wrap;gap:6px;}
.pills .pair > span{padding:5px 14px;border-radius:143px;background:var(--surface);font-size:13px;line-height:20px;white-space:nowrap;}
.skills{display:flex;flex-direction:column;gap:10px;}
.skills li{display:flex;align-items:center;gap:12px;font-size:14px;line-height:1.5;}
.skills svg{width:26px;height:26px;flex:none;border-radius:6px;box-shadow:0 0 0 1px var(--edge);}
.rows li{display:flex;justify-content:space-between;gap:16px;padding-block:10px;border-bottom:1px solid var(--hairline);font-size:14px;line-height:1.5;}
.rows li:first-child{padding-top:0;}
.rows li:last-child{border-bottom:0;padding-bottom:0;}
.rows .lvl{color:var(--muted);}
.edu .item + .item{margin-top:18px;padding-top:18px;border-top:1px solid var(--hairline);}
.edu h3{font-size:16px;font-weight:600;line-height:1.4;letter-spacing:-.01em;}
.edu .sub{font-size:14px;line-height:1.5;}
.edu .inst{margin-top:6px;font-size:13px;line-height:1.5;color:var(--muted);}
.edu .years{margin-top:6px;font-size:13px;font-weight:500;line-height:1.5;}

/* ---------- Stationen ---------- */
.jobs > h2{font-size:32px;font-weight:600;line-height:1.3;letter-spacing:-.03em;margin-bottom:24px;}
.job{display:grid;grid-template-columns:150px minmax(0,1fr);gap:0 24px;padding-block:30px;border-top:1px solid var(--hairline);break-inside:avoid;}
.job:last-child{padding-bottom:0;}
.job .dates{padding-top:6px;font-size:14px;font-weight:500;line-height:1.5;color:var(--muted);word-spacing:0;}
.job .dates span{white-space:nowrap;}
.job h3{font-size:22px;font-weight:600;line-height:1.35;letter-spacing:-.02em;}
.job .company{font-weight:500;color:var(--muted);}
.job p{margin-top:12px;font-size:15px;line-height:1.7;color:var(--body);}

/* ---------- Abschluss: dunkle Fläche wie auf der Website ---------- */
.footer{position:relative;z-index:1;padding:8px;margin-top:140px;}
.dark-panel{
  position:relative;display:flex;flex-direction:column;gap:80px;padding:100px calc(var(--gutter) - 8px) 60px;border-radius:24px;
  --panel:#000; --panel-ink:#fff; --panel-muted:rgba(255,255,255,.5); --panel-line:rgba(255,255,255,.25);
  --panel-glow:#2e2e2e; --panel-beam:.05; --panel-noise:.12; --panel-noise-filter:invert(1); --panel-wrap:rgba(255,255,255,.3);
  background:var(--panel);color:var(--panel-ink);overflow:clip;
}
.dark-bg{
  position:absolute;inset:0;overflow:hidden;
  background:radial-gradient(100% 100% at 0% 0%,var(--panel-glow) 0%,var(--panel) 100%);
  -webkit-mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
  mask-image:radial-gradient(125% 100% at 0% 0%,#000 0%,rgba(0,0,0,.22) 88%,transparent 100%);
}
.dark-bg .beams span{opacity:var(--panel-beam);}
.dark-panel .noise{position:absolute;opacity:var(--panel-noise);filter:var(--panel-noise-filter);}
.cta{position:relative;display:flex;flex-direction:column;align-items:center;gap:36px;text-align:center;}
.cta .display span{display:block;}
.cta .display span + span{color:var(--panel-muted);}
.cta p{max-width:620px;font-size:20px;font-weight:600;line-height:1.5;letter-spacing:-.02em;}
.cta-btns{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:12px;}
.btn-wrap{display:inline-flex;padding:8px;border-radius:90px;background:var(--panel-wrap);}
.footer-bottom{position:relative;display:flex;align-items:center;justify-content:space-between;gap:36px;width:100%;max-width:var(--max);margin-inline:auto;}
.copyright{padding:8px 16px;border-block:1px solid var(--panel-line);}
.socials{display:flex;gap:36px;}
.social{display:grid;place-items:center;width:44px;height:44px;padding:12px;border-radius:50%;border:1px solid var(--panel-line);transition:background .2s,color .2s;}
.social:hover{background:var(--panel-ink);color:var(--panel);}

/* ---------- Auftritt beim Laden ---------- */
@media screen and (prefers-reduced-motion:no-preference){
  .namewrap,.sheet{animation:rise .9s var(--ease) both;}
  .sheet{animation-delay:.1s;}
  .figure{animation:peek 1s var(--ease) .3s both;}
}
@keyframes rise{from{opacity:0;transform:translateY(24px);}}
@keyframes peek{from{opacity:0;transform:translate(-50%,24%);}}

/* ---------- Tablet ---------- */
@media screen and (max-width:1199px){
  .sheet{padding:48px 40px 56px;}
  .columns{grid-template-columns:256px minmax(0,1fr);gap:48px;}
  .contact li{gap:10px;font-size:13.5px;}
  .job{display:block;}
  .job .dates{padding:0 0 4px;}
  .footer{margin-top:100px;}
}
@media screen and (max-width:960px){
  .namewrap,.sheet-wrap{--name:84px;}
  .hi,.role{font-size:20px;}
}

/* ---------- Phone: eine Spalte, Kontakt zuerst, dann die Stationen, dann der Rest ---------- */
@media screen and (max-width:809px){
  .nav-inner{height:68px;}
  .hero{padding-top:108px;}
  .tag{font-size:16px;}
  .namewrap,.sheet-wrap{--name:46px;}
  .hi,.role{font-size:15px;}
  /* die Rolle bricht unter dem Nachnamen auf zwei Zeilen um */
  .role{display:block;min-width:100%;margin-top:4px;white-space:normal;text-align:right;line-height:1.25;}
  .sheet-wrap{margin-top:18px;}
  .sheet{padding:40px 24px 44px;}
  .columns{display:flex;flex-direction:column;gap:44px;}
  .side{display:contents;}
  .side > *{order:3;}
  .side > .contact-box{order:1;}
  .jobs{order:2;}
  .jobs > h2{font-size:26px;margin-bottom:20px;}
  .side h2{font-size:22px;padding:0 0 16px;}
  /* etwas schmalere Pills, damit Art Direction + Creative Direction ab 360 px in eine Zeile passen */
  .pills .pair > span{padding-inline:12px;}
  .job{padding-block:24px;}
  .job h3{font-size:20px;}
  .footer{margin-top:72px;}
  .dark-panel{gap:56px;padding:72px 16px 32px;}
  .cta p{font-size:17px;}
  .footer-bottom{gap:16px;}
  .socials{gap:12px;}
}
/* zwischen Phone und Tablet passt die Rolle wieder in eine Zeile */
@media screen and (min-width:560px) and (max-width:809px){
  .namewrap,.sheet-wrap{--name:68px;}
  .hi,.role{font-size:17px;}
  .role{display:flex;min-width:0;white-space:nowrap;line-height:1.3;}
  .sheet-wrap{margin-top:26px;}
}
@media screen and (max-width:420px){
  .btn--nav{padding:0 14px 0 16px;}
  .btn--nav .long{display:none;}
  .btn--nav .short{display:inline;}
}
@media screen and (max-width:360px){
  .namewrap,.sheet-wrap{--name:40px;}
  .pills .pair > span{padding-inline:10px;font-size:11.5px;}
  .hi,.role{font-size:14px;}
}

/* ---------- Druck und PDF: A4, hell, zwei Spalten ---------- */
/* randlos, damit das Grau die ganze Seite füllt (Seitenränder blieben in Chrome weiß) */
@page{size:A4;margin:0;}
@media print{
  :root{--bg:#f6f6f6;}
  .nav,.footer,.noise,.page-bg{display:none;}
  body{font-size:13px;word-spacing:.04em;}
  main{padding-inline:34px;}
  .hero{padding-top:42px;}
  .namewrap,.sheet-wrap{--name:66px;}
  .hi,.role{font-size:16px;}
  .role{margin-top:4px;}
  .sheet-wrap{margin-top:22px;}
  /* statt der Karte nur ihre Oberkante: eine Karte über drei Seiten bricht unschön um */
  .sheet{padding:0;border-radius:0;background:none;box-shadow:none;border-top:1px solid var(--faint);}
  .columns{grid-template-columns:204px minmax(0,1fr);gap:32px;padding-top:4px;}
  /* Abstände als durchsichtige Ränder: sie bleiben am Seitenanfang erhalten, Außenabstände nicht */
  .side{display:block;}
  .side > *{break-inside:avoid;border-top:22px solid transparent;}
  .side h2{font-size:18px;padding:0 0 11.4px;margin-bottom:12px;}
  .contact-box h2{padding-top:2.4px;}
  .contact{gap:8px;}
  .contact li{gap:10px;font-size:11.5px;}
  .contact i{width:26px;height:26px;padding:6.5px;}
  .pills,.pills .pair{gap:4px;}
  .pills .pair > span{padding:3px 9px;font-size:11px;line-height:16px;box-shadow:0 0 0 1px var(--edge);}
  .skills{gap:7px;}
  .skills li{gap:9px;font-size:11.5px;}
  .skills svg{width:20px;height:20px;border-radius:5px;}
  .rows li{padding-block:6px;font-size:11.5px;}
  .edu .item + .item{margin-top:12px;padding-top:12px;}
  .edu h3{font-size:13px;}
  .edu .sub{font-size:11.5px;}
  .edu .inst,.edu .years{margin-top:4px;font-size:11px;}
  .jobs > h2{font-size:24px;margin:18px 0 0;padding-bottom:10px;border-bottom:1px solid var(--hairline);}
  /* die Trennlinie hängt unter der Station, damit oben auf einer neuen Seite keine Linie steht */
  .job{display:block;padding:0;border-top:22px solid transparent;}
  .job:first-of-type{border-top-width:18px;}
  .job:not(:last-child)::after{content:"";display:block;margin-top:18px;border-top:1px solid var(--hairline);}
  .job .dates{padding:0 0 2px;font-size:11.5px;}
  .job h3{font-size:17px;}
  .job .company{font-size:13px;}
  .job p{margin-top:7px;font-size:12px;line-height:1.58;}
}
'''.replace('FONT_B64', FONT_B64)

# Dunkles Design schon vor dem ersten Zeichnen setzen, damit nichts hell aufblitzt. Hell ist Standard;
# der Schlüssel heißt "cv-mode", weil die alte Fassung (dunkel als Standard) "cv-theme" belegt hat.
HEAD_SCRIPT = '''try{if(localStorage.getItem("cv-mode")==="dark")document.documentElement.dataset.theme="dark";}catch(e){}'''

SCRIPT = '''
(function(){
  var r=document.documentElement, b=document.getElementById("themeToggle");
  function dark(){return r.dataset.theme==="dark";}
  b.setAttribute("aria-pressed",String(dark()));
  b.addEventListener("click",function(){
    var d=!dark();
    if(d){r.dataset.theme="dark";}else{delete r.dataset.theme;}
    b.setAttribute("aria-pressed",String(d));
    try{localStorage.setItem("cv-mode",d?"dark":"light");}catch(e){}
  });
})();
'''

BEAMS = '<div class="beams"><span></span><span></span><span></span><span></span><span></span></div>'

def dates_html(d):
    a, b = d.split(' – ')
    return f'<span>{a} –</span> <span>{b}</span>'

def render(c):
    ex = c['expertise']
    exp_items = ''.join('<div class="pair">' + ''.join(f'<span role="listitem">{e}</span>' for e in ex[i:i+2]) + '</div>'
                        for i in range(0, len(ex), 2))
    skill_items = ''.join(f'<li>{svg}<span>{n}</span></li>' for n, svg in SKILLS)
    lang_items = ''.join(f'<li><span>{l}</span><span class="lvl">{v}</span></li>' for l, v in c['langs'])
    edu_items = ''.join(
        f'<div class="item"><h3>{t}</h3>' + (f'<div class="sub">{s}</div>' if s else '') +
        f'<div class="inst">{i}</div><div class="years">{y}</div></div>'
        for t, s, i, y in c['edu'])
    job_items = ''.join(
        f'<article class="job"><div class="dates">{dates_html(d)}</div><div>'
        f'<h3>{t}</h3><div class="company">{co}</div><p>{txt}</p></div></article>'
        for d, t, co, txt in c['jobs'])
    cur = lambda l: ' aria-current="true"' if c['lang'] == l else ''

    return f'''<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{c['meta']}">
<link rel="canonical" href="{c['canonical']}">
<link rel="alternate" hreflang="de" href="https://cv.edgarheinz.com/">
<link rel="alternate" hreflang="en" href="https://cv.edgarheinz.com/en/">
<link rel="icon" href="{FAVICON}">
<title>{c['title']}</title>
<script>{HEAD_SCRIPT}</script>
<style>{CSS}</style>
</head>
<body>
<div class="noise" aria-hidden="true"></div>
<div class="page-bg" aria-hidden="true">{BEAMS}</div>

<header class="nav">
  <div class="nav-inner">
    <a class="wordmark" href="https://edgarheinz.com" aria-label="{c['logo_label']}" title="{c['logo_label']}">{LOGO}</a>
    <div class="nav-right">
      <div class="lang" role="group" aria-label="{c['lang_label']}">
        <a href="{c['de_href']}" lang="de"{cur('de')}>DE</a>
        <a href="{c['en_href']}" lang="en"{cur('en')}>EN</a>
      </div>
      <button class="theme-btn" id="themeToggle" type="button" aria-label="{c['theme_label']}" aria-pressed="false"><span class="i-moon">{ICON['moon']}</span><span class="i-sun">{ICON['sun']}</span></button>
      <a class="btn btn--nav" href="{c['pdf_file']}" download><span class="long">{c['pdf_label']}</span><span class="short">{c['pdf_short']}</span>{ICON['download']}</a>
    </div>
  </div>
</header>

<main>
  <div class="container">
    <header class="hero">
      <h1 class="namewrap">
        <span class="hi">{c['hi']} </span>
        <span class="n n1">Edgar </span>
        <span class="n n2">Hein<span class="z">z</span></span>
        <span class="role"> {c['role']}</span>
      </h1>
    </header>
    <div class="sheet-wrap">
      <img class="figure" src="data:image/webp;base64,{FIGURE_B64}" width="1300" height="601" alt="Edgar Heinz">
      <div class="sheet">
        <div class="columns">
          <aside class="side">
            <section class="contact-box">
              <h2>{c['h_contact']}</h2>
              <ul class="contact">
                <li><i>{ICON['linkedin']}</i><a href="https://www.linkedin.com/in/edgar-heinz/">{COMMON['linkedin']}</a></li>
                <li><i>{ICON['globe']}</i><a href="https://edgarheinz.com">{COMMON['site']}</a></li>
                <li><i>{ICON['mail']}</i><a href="mailto:{COMMON['mail']}">{COMMON['mail']}</a></li>
                <li><i>{ICON['phone']}</i><a href="tel:+4917670214158">{COMMON['phone']}</a></li>
                <li><i>{ICON['house']}</i><span>{COMMON['addr']}</span></li>
              </ul>
            </section>
            <section>
              <h2>{c['h_expertise']}</h2>
              <div class="pills" role="list">{exp_items}</div>
            </section>
            <section>
              <h2>{c['h_skills']}</h2>
              <ul class="skills">{skill_items}</ul>
            </section>
            <section>
              <h2>{c['h_lang']}</h2>
              <ul class="rows">{lang_items}</ul>
            </section>
            <section class="edu">
              <h2>{c['h_edu']}</h2>
              {edu_items}
            </section>
          </aside>
          <section class="jobs">
            <h2>{c['h_exp']}</h2>
            {job_items}
          </section>
        </div>
      </div>
    </div>
  </div>
</main>

<footer class="footer">
  <div class="dark-panel">
    <div class="dark-bg" aria-hidden="true">{BEAMS}</div>
    <div class="noise" aria-hidden="true"></div>
    <div class="cta">
      <div class="tag tag--light">{c['cta_tag']}</div>
      <h2 class="display"><span>{c['cta_a']}</span><span>{c['cta_b']}</span></h2>
      <p>{c['cta_text']}</p>
      <div class="cta-btns">
        <div class="btn-wrap"><a class="btn" href="mailto:{COMMON['mail']}">{c['cta_mail']}{ICON['arrow']}</a></div>
        <a class="btn btn--outline" href="https://edgarheinz.com">{c['cta_site']}{ICON['arrow']}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span class="copyright">© Edgar Heinz, 2026</span>
      <div class="socials">
        <a class="social" href="mailto:{COMMON['mail']}" aria-label="E-Mail">{ICON['mail']}</a>
        <a class="social" href="https://www.linkedin.com/in/edgar-heinz/" target="_blank" rel="noopener" aria-label="LinkedIn">{ICON['linkedin']}</a>
      </div>
    </div>
  </div>
</footer>
<script>{SCRIPT}</script>
</body>
</html>'''

OUT = os.path.join(HERE, 'docs')
os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(render(DE))
open(os.path.join(OUT, 'en', 'index.html'), 'w', encoding='utf-8').write(render(EN))
print('written to docs/')

# ---------- PDFs: die Druckansicht der beiden Seiten, per Headless-Chrome ----------
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if '--pdf' in sys.argv:
    for page, name in (('index.html', 'Edgar-Heinz-Lebenslauf.pdf'), ('en/index.html', 'Edgar-Heinz-Resume.pdf')):
        target = os.path.join(OUT, name)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={target}', 'file://' + os.path.join(OUT, page)],
                       check=True, capture_output=True)
        # dieselbe Datei liegt zusätzlich im Projektordner
        open(os.path.join(HERE, name), 'wb').write(open(target, 'rb').read())
        print('pdf:', name)
