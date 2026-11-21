"""Generate the profile README SVG panels into assets/."""
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).resolve().parent.parent / "assets"
OR, BG, FG, MUT, LINE = "#FC4C02", "#050505", "#F5F5F5", "#8A8A8A", "#1C1C1C"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
W = 1000


def frame(h, body, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity="0.035"/></pattern>
<linearGradient id="og" x1="0" x2="1"><stop offset="0" stop-color="{OR}"/><stop offset="1" stop-color="#FF8A3D"/></linearGradient>
{defs}
</defs>
<rect width="{W}" height="{h}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{h}" rx="18" fill="url(#grid)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="18" fill="none" stroke="{LINE}"/>
{body}
</svg>
'''


def t(x, y, s, size=16, fill=FG, font=SANS, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{esc(s)}</text>'


def fade(i, step=0.12):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{i*step:.2f}s" dur="0.6s" fill="freeze"/>'


def g_fade(i, inner):
    return f'<g>{inner}</g>'


def pill(x, y, label, hot=False, size=13):
    w = len(label) * size * 0.6 + 24
    stroke = OR if hot else "#333"
    fill = "#1a0a03" if hot else "#0d0d0d"
    col = OR if hot else "#D0D0D0"
    return w, (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{fill}" stroke="{stroke}"/>'
               + t(x + 12, y + 19, label, size, col, MONO))


def pills(x, y, labels, hot=()):
    out = []
    for lab in labels:
        w, s = pill(x, y, lab, lab in hot)
        out.append(s)
        x += w + 8
    return "".join(out)


def header(num, title, y=46):
    return (t(40, y, f"{num:02d}", 13, OR, MONO, 700)
            + t(72, y, title.upper(), 13, FG, MONO, 700, 'letter-spacing="3"')
            + f'<line x1="{80 + len(title) * 10.4:.0f}" y1="{y-4}" x2="960" y2="{y-4}" stroke="{LINE}"/>')


# ---------------------------------------------------------------- hero
def hero():
    h = 440
    phrases = ["building data pipelines with Apache Airflow",
               "shipping AI agents that stop before you pay",
               "Télécom Paris · Data Science & Strategy"]
    n, dur, x0, y0, cw = len(phrases), 12, 64, 252, 22 * 0.6
    # each phrase: types in [s-0.10, s], holds to s+0.20, erases by s+0.23; phrase 0 is shown at t=0
    widths = [len(p) * cw * 1.08 + 8 for p in phrases]
    typing = []
    cur = []
    for i, wmax in enumerate(widths):
        st = i / n
        if i == 0:
            pts = [(0, wmax), (0.20, wmax), (0.23, 0), (0.90, 0), (1, wmax)]
        else:
            pts = [(0, 0), (st - 0.10, 0), (st, wmax), (st + 0.20, wmax), (st + 0.23, 0), (1, 0)]
        vals = ";".join(f"{v:.0f}" for _, v in pts)
        kt = ";".join(f"{k:.4f}" for k, _ in pts)
        typing.append(f'''<clipPath id="c{i}"><rect x="{x0}" y="{y0-24}" width="{pts[0][1]:.0f}" height="34"><animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect></clipPath>''')
        if i:
            cur += [(st - 0.10, 0), (st, wmax), (st + 0.20, wmax), (st + 0.23, 0)]
    cur = [(0, widths[0]), (0.20, widths[0]), (0.23, 0)] + cur + [(0.90, 0), (1, widths[0])]
    cur_kt = [k for k, _ in cur]
    cur_vals = [x0 + 4 + v for _, v in cur]
    defs = "".join(typing) + f'''
<radialGradient id="glow" cx="0.78" cy="0.45" r="0.55"><stop offset="0" stop-color="{OR}" stop-opacity="0.28"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></radialGradient>
<linearGradient id="elev" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OR}" stop-opacity="0.55"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="4"/></filter>'''
    route = "M600 300 C640 250 650 190 700 175 S780 205 805 150 S860 80 905 110 S935 190 890 230 S800 250 770 290 S700 330 650 320"
    elev = "M0 440 L0 400 C80 395 120 370 190 378 S300 400 360 372 S470 330 540 350 S640 395 720 360 S820 300 880 330 S960 380 1000 360 L1000 440 Z"
    body = f'''<rect width="{W}" height="{h}" rx="18" fill="url(#glow)"/>
<path d="{elev}" fill="url(#elev)" opacity="0.35"><animate attributeName="opacity" values="0.2;0.45;0.2" dur="6s" repeatCount="indefinite"/></path>
{t(64, 86, "// SOFTWARE ENGINEER · PARIS, FRANCE", 14, OR, MONO, 700, 'letter-spacing="2"')}
{t(60, 178, "Iba Demesy", 92, FG, SANS, 800, 'letter-spacing="-3"')}
<rect x="64" y="200" width="120" height="4" fill="url(#og)"/>
{t(x0 - 2, y0, ">", 22, OR, MONO, 700)}
''' + "".join(f'<g clip-path="url(#c{i})">{t(x0 + 22, y0, p, 22, "#E8E8E8", MONO)}</g>' for i, p in enumerate(phrases)) + f'''
<rect x="{cur_vals[0] + 18:.0f}" y="{y0 - 19}" width="11" height="24" fill="{OR}"><animate attributeName="x" values="{';'.join(f'{v + 18:.0f}' for v in cur_vals)}" keyTimes="{';'.join(f'{k:.4f}' for k in cur_kt)}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></rect>
<path d="{route}" fill="none" stroke="{OR}" stroke-opacity="0.18" stroke-width="10" stroke-linecap="round" filter="url(#blur)"/>
<path d="{route}" fill="none" stroke="#2a2a2a" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 8"/>
<path id="route" d="{route}" fill="none" stroke="url(#og)" stroke-width="4" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"><animate attributeName="stroke-dashoffset" values="1200;0;0" keyTimes="0;0.7;1" dur="5s" repeatCount="indefinite"/></path>
<circle r="16" fill="{OR}" opacity="0.25"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.7;1" calcMode="linear"><mpath href="#route"/></animateMotion><animate attributeName="r" values="10;18;10" dur="1.2s" repeatCount="indefinite"/></circle>
<circle r="6" fill="#fff" stroke="{OR}" stroke-width="3"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.7;1" calcMode="linear"><mpath href="#route"/></animateMotion></circle>
<circle cx="600" cy="300" r="5" fill="{OR}"/>{t(612, 318, "START", 11, OR, MONO, 700, 'letter-spacing="2"')}
{t(842, 66, "42.195 KM", 13, OR, MONO, 700, 'letter-spacing="2"')}
'''
    stats = [("550", "runners organised", "Ekiden du Platal"),
             ("3RD", "prize, drone swarm", "Swarm Rescue 25-26"),
             ("3", "agents in parallel", "RunAI v2")]
    for i, (big, l1, l2) in enumerate(stats):
        x = 64 + i * 180
        body += g_fade(i + 2, t(x, 334, big, 38, FG, SANS, 800) + t(x, 358, l1, 13, "#CFCFCF", SANS) + t(x, 376, l2.upper(), 10, MUT, MONO, 400, 'letter-spacing="1.5"'))
    body += f'<line x1="64" y1="300" x2="560" y2="300" stroke="{LINE}"/>'
    (OUT / "hero.svg").write_text(frame(h, body, defs))


# ---------------------------------------------------------------- experience
def experience():
    h = 400
    body = header(1, "Experience")
    body += f'<line x1="56" y1="96" x2="56" y2="356" stroke="#262626" stroke-width="2"/>'
    body += f'''<circle cx="56" cy="104" r="7" fill="{OR}"/><circle cx="56" cy="104" r="7" fill="none" stroke="{OR}" stroke-width="2"><animate attributeName="r" values="7;20" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>'''
    body += g_fade(0, t(88, 112, "Software Engineer", 28, FG, SANS, 700)
                   + t(960, 112, "SEP 2026 — NOW", 13, OR, MONO, 700, 'text-anchor="end" letter-spacing="1.5"')
                   + t(88, 138, "xpln.ai  ·  Paris  ·  Full-time", 15, MUT)
                   + pills(88, 154, ["Apache Airflow", "Data pipelines", "Python", "SQL"], hot={"Apache Airflow"}))
    body += f'<circle cx="56" cy="232" r="6" fill="{BG}" stroke="#666" stroke-width="2"/>'
    lines = ["Owned a budget-control application: business requirements, specs, IT test strategy",
             "Adoption analytics with Piano Analytics and Microsoft Clarity; Power BI dashboards",
             "Level-3 production support, steering fixes with the development teams"]
    inner = (t(88, 240, "IS Analyst Intern", 24, FG, SANS, 700)
             + t(960, 240, "JAN — JUN 2026", 13, MUT, MONO, 700, 'text-anchor="end" letter-spacing="1.5"')
             + t(88, 264, "VINCI Construction IT  ·  Business Solutions & Adoption", 15, MUT))
    for i, l in enumerate(lines):
        y = 298 + i * 26
        inner += f'<rect x="90" y="{y-9}" width="8" height="2" fill="{OR}"/>' + t(110, y - 3, l, 14.5, "#CFCFCF")
    body += g_fade(2, inner)
    (OUT / "experience.svg").write_text(frame(h, body))


# ---------------------------------------------------------------- project
def project():
    h = 430
    body = header(2, "Featured project")
    body += f'<rect x="40" y="76" width="920" height="320" rx="14" fill="#0A0A0A" stroke="url(#og)" stroke-opacity="0.7"/>'
    body += g_fade(0, t(72, 132, "RunAI v2", 46, FG, SANS, 800, 'letter-spacing="-1.5"')
                   + t(72, 160, "RACE-TRIP ASSISTANT FOR RUNNERS", 12, OR, MONO, 700, 'letter-spacing="2"'))
    desc = ["Describe the race you want. RunAI finds real races",
            "with official dates, then three browser agents prepare",
            "registration, hotel and transport in parallel,",
            "and stop before any payment."]
    body += g_fade(1, "".join(t(72, 200 + i * 24, d, 16, "#CFCFCF") for i, d in enumerate(desc)))
    body += g_fade(2, pills(72, 310, ["Python", "FastAPI", "Pydantic", "pytest"])
                   + t(72, 370, "Started at the Computer Use Agents Hackathon · H Company x 42AI · Nov 2026", 12, MUT, MONO))
    # agent flow diagram
    fx = 560
    body += f'<rect x="{fx}" y="186" width="96" height="40" rx="8" fill="#111" stroke="#333"/>' + t(fx + 48, 211, "LINKUP", 12, FG, MONO, 700, 'text-anchor="middle"')
    body += t(fx + 48, 176, "sourced races", 11, MUT, MONO, 400, 'text-anchor="middle"')
    lanes = [("REGISTRATION", 130), ("HOTEL", 206), ("TRANSPORT", 282)]
    stop_x = 905
    for i, (lab, y) in enumerate(lanes):
        p = f"M{fx+96} 206 C{fx+140} 206 {fx+140} {y} {fx+180} {y} L{stop_x-40} {y}"
        body += f'<path id="l{i}" d="{p}" fill="none" stroke="#2a2a2a" stroke-width="2"/>'
        body += f'<path d="{p}" fill="none" stroke="{OR}" stroke-width="2" stroke-dasharray="400" stroke-dashoffset="400"><animate attributeName="stroke-dashoffset" values="400;0;0" keyTimes="0;0.6;1" dur="3.5s" begin="{i*0.25}s" repeatCount="indefinite"/></path>'
        body += f'<circle r="5" fill="#fff"><animateMotion dur="3.5s" begin="{i*0.25}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.6;1" calcMode="linear"><mpath href="#l{i}"/></animateMotion></circle>'
        body += t(fx + 190, y - 10, lab, 11, "#BDBDBD", MONO, 700, 'letter-spacing="1.5"')
    body += f'<rect x="{stop_x-38}" y="110" width="4" height="196" fill="{OR}"/>'
    body += t(stop_x - 20, 200, "STOP", 13, OR, MONO, 800, 'letter-spacing="2"') + t(stop_x - 20, 218, "before", 11, MUT, MONO) + t(stop_x - 20, 232, "payment", 11, MUT, MONO)
    body += t(928, 376, "github.com/IbaDemesy/runai-v2  →", 13, OR, MONO, 700, 'text-anchor="end"')
    (OUT / "project.svg").write_text(frame(h, body))


# ---------------------------------------------------------------- education
def education():
    h = 560
    body = header(3, "Education")
    rows = [("2023 — 2026", "Master of Engineering · Data Science & Strategy/Economics", "Télécom Paris, Institut Polytechnique de Paris", True),
            ("AUG — DEC 2025", "Exchange semester · Business & Economics", "Tecnológico de Monterrey, Mexico", False),
            ("2021 — 2023", "Classes préparatoires MPSI / MP*", "Lycée Chaptal, Paris", False),
            ("2021", "Baccalauréat · Mathematics, Physics & Computer Science", "La Salle Passy Buzenval", False),
            ("2017 — 2021", "US High School Diploma · French-American Dual Diploma", "Dual Diploma, online", False)]
    for i, (d, deg, school, hot) in enumerate(rows):
        y = 100 + i * 56
        inner = (t(40, y + 6, d, 12, OR if hot else MUT, MONO, 700, 'letter-spacing="1"')
                 + t(210, y, deg, 17 if hot else 16, FG, SANS, 700 if hot else 600)
                 + t(210, y + 22, school, 14, MUT))
        if i < len(rows) - 1:
            inner += f'<line x1="40" y1="{y+38}" x2="960" y2="{y+38}" stroke="{LINE}"/>'
        body += g_fade(i, inner)
    body += t(40, 410, "AT SCHOOL", 12, MUT, MONO, 700, 'letter-spacing="3"')
    cards = [(40, "3RD", "Swarm Rescue Challenge 2025-26", "10-drone fleet in Python, robust to", "loss of localisation, comms or drones"),
             (510, "550", "Ekiden du Platal · race director", "VP of the sports club, 8-person team,", "91 teams, 100+ volunteers, €20k budget")]
    for i, (x, big, ttl, l1, l2) in enumerate(cards):
        inner = (f'<rect x="{x}" y="426" width="450" height="104" rx="12" fill="#0B0B0B" stroke="#262626"/>'
                 + t(x + 24, 492, big, 44, OR, SANS, 800)
                 + t(x + 140, 462, ttl, 15, FG, SANS, 700)
                 + t(x + 140, 486, l1, 13, "#BDBDBD") + t(x + 140, 506, l2, 13, "#BDBDBD"))
        body += g_fade(i + 5, inner)
    (OUT / "education.svg").write_text(frame(h, body))


# ---------------------------------------------------------------- stack
def stack():
    h = 290
    body = header(4, "Stack")
    groups = [("DATA", ["Apache Airflow", "Python", "SQL", "PostgreSQL", "pandas", "NumPy", "Power BI"], {"Apache Airflow"}),
              ("AI & BACKEND", ["AI agents", "FastAPI", "Pydantic", "PyTorch", "scikit-learn", "httpx"], {"AI agents"}),
              ("TOOLS", ["Git", "GitHub Actions", "Docker", "Linux", "Java", "Raspberry Pi"], set())]
    for i, (g, labs, hot) in enumerate(groups):
        y = 84 + i * 52
        body += g_fade(i, t(40, y + 19, g, 12, MUT, MONO, 700, 'letter-spacing="2"') + pills(190, y, labs, hot))
    body += f'<line x1="40" y1="246" x2="960" y2="246" stroke="{LINE}"/>'
    body += t(40, 272, "LANGUAGES", 12, MUT, MONO, 700, 'letter-spacing="2"') + "".join(t(190 + i * 200, 272, l, 14, FG, MONO) for i, l in enumerate(["French · native", "English · C1", "Spanish · B1"]))
    (OUT / "stack.svg").write_text(frame(h, body))


def button(name, label, w=300):
    h = 56
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="28" fill="{BG}" stroke="{OR}" stroke-width="1.5"/>
<circle cx="30" cy="28" r="5" fill="{OR}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
{t(48, 33, label, 14, FG, MONO, 700, 'letter-spacing="1"')}
{t(w - 26, 34, "→", 18, OR, MONO, 700, 'text-anchor="end"')}
</svg>
'''
    (OUT / f"btn-{name}.svg").write_text(s)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    hero(); experience(); project(); education(); stack()
    button("linkedin", "LINKEDIN")
    button("runai", "RUNAI V2")
    button("school", "SCHOOL PROJECTS")
