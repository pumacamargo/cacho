#!/usr/bin/env python3
"""Genera el mapa completo e interactivo del ecosistema (wiki cacho) -> HTML autónomo.

Uso:  python3 build-mapa.py            (desde la raíz del repo cacho)
Sale: web/mapa-ecosistema.html
Lee las fichas reales de entities/ y operations/: títulos, descripciones y tags,
así que el mapa no se desincroniza de la documentación.
"""
import os, re, html, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo cacho
GH = "https://github.com/pumacamargo/cacho/blob/main"

OPER_GROUPS = [
    ("Publicar, accesos y máquinas", ["acceso-ftps-lemon-sushi", "acceso-nas-polaris",
                                      "acceso-remoto-pumadeskasus", "diagnostico-espacio-disco-vps"]),
    ("Hacer y editar videos", ["ttchop-video-paths", "ttchop-video-generation", "recrear-video-creadores-edits",
                               "ttchop-raw-asset-manual-edit", "ttchop-filmcraft-video-tests",
                               "traduccion-video-pumasvoice-sincronizada", "ttchop-music-generation",
                               "ttchop-carousel-creation"]),
    ("Datos y estudio", ["estudio-creadores-fuentes-datos", "separar-videos-nas-por-cortes",
                         "transcripcion-curso-gerardo-santiago"]),
]
SISTEMAS = ["hermes-agent", "hermes-agentes", "cacho", "ttchop", "ttchop-automatizaciones", "ttchop-webapps"]
CATS = ["categoria-backpack", "categoria-cliff", "categoria-macanishi",
        "categoria-moon", "categoria-sandbox", "categoria-tts"]
CAT_ICON = {"categoria-backpack": "🎒", "categoria-cliff": "🎬", "categoria-macanishi": "👨‍👩‍👧",
            "categoria-moon": "📈", "categoria-sandbox": "🛠️", "categoria-tts": "🛒"}


def read(page_id, folder):
    """Lee una ficha y devuelve sus metadatos."""
    p = os.path.join(ROOT, folder, page_id + ".md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    fm, body = (m.group(1), t[m.end():]) if m else ("", t)
    d = {"id": page_id, "folder": folder}
    for k in ("title", "type", "status"):
        mm = re.search(rf"^{k}:\s*(.+)$", fm, re.M)
        d[k] = mm.group(1).strip().strip("\"'") if mm else ""
    mm = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    d["tags"] = [x.strip() for x in mm.group(1).split(",") if x.strip()] if mm else []
    desc = ""
    for ln in body.split("\n"):
        s = ln.strip()
        if s and not s.startswith(("#", ">", "---", "|", "-")):
            desc = re.sub(r"\[\[(.+?)\]\]", r"\1", s)
            break
    d["desc"] = re.sub(r"\*\*|`", "", desc)[:230]
    # categoría (para proyectos / categorías)
    mc = re.search(r"\[\[(categoria-\w+)\]\]", body)
    d["cat"] = mc.group(1) if mc else ""
    d["gh"] = f"{GH}/{folder}/{page_id}.md"
    return d


pages = {}
for folder in ("entities", "operations"):
    for f in sorted(os.listdir(os.path.join(ROOT, folder))):
        if f.endswith(".md"):
            pid = f[:-3]
            pages[pid] = read(pid, folder)


def card(pid, area, extra=""):
    d = pages.get(pid)
    if not d:
        return ""
    tags = " · ".join(d["tags"][:4])
    badge = {"entity": "ficha", "operation": "runbook"}.get(d["type"], d["type"] or "—")
    st = f'<span class="st st-{d["status"]}">{d["status"]}</span>' if d["status"] else ""
    return f"""<details class="card" data-area="{area}" data-text="{html.escape((d['title']+' '+d['desc']+' '+tags+' '+pid).lower(), quote=True)}">
<summary><b>{html.escape(d['title'] or pid)}</b><span class="badge">{badge}</span>{st}{extra}</summary>
<p class="desc">{html.escape(d['desc'])}</p>
<p class="meta">{html.escape(tags)}<br><a href="{d['gh']}" target="_blank" rel="noopener">ver ficha completa ↗</a> <span class="path">{d['folder']}/{pid}.md</span></p>
</details>"""


# ── proyectos por categoría
projects = {c: [] for c in CATS}
for pid, d in pages.items():
    if pid.startswith("proyecto-") and d["cat"] in projects:
        projects[d["cat"]].append(pid)

# ── diagrama: fila de categorías con sus proyectos
flow_cats = ""
for c in CATS:
    d = pages.get(c, {})
    names = [pages[p]["title"] if p in pages else p.replace("proyecto-", "").title() for p in projects[c]]
    if c == "categoria-cliff":
        names = ["Apex", "Papa", "Tacosdepulpo", "Chava"]
        note = ' <span class="wip">en veremos</span>'
    else:
        note = ""
    chips = "".join(f'<span class="pchip">{html.escape(n)}</span>' for n in names)
    flow_cats += (f'<div class="fcat"><div class="fcat-t">{CAT_ICON.get(c,"")} '
                  f'{html.escape((d.get("title") or c).replace("Categoría ",""))}{note}</div>'
                  f'<div class="fchips">{chips}</div></div>')

# ── plataforma
hardware = [p for p in pages if p.startswith("hardware-")]
syscards = "".join(card(p, "plataforma") for p in SISTEMAS if p in pages)
hwcards = "".join(card(p, "plataforma") for p in sorted(hardware))

# ── operaciones agrupadas
oper_html = ""
claimed = set()
for gname, ids in OPER_GROUPS:
    cards = "".join(card(i, "operaciones") for i in ids)
    claimed |= set(ids)
    oper_html += f'<h3 class="gsub">{html.escape(gname)}</h3><div class="grid">{cards}</div>'
rest = [p for p, d in pages.items() if d["folder"] == "operations" and p not in claimed]
if rest:
    oper_html += ('<h3 class="gsub">Otros</h3><div class="grid">' +
                  "".join(card(i, "operaciones") for i in rest) + "</div>")

# ── categorías y proyectos
cat_html = card("categorias-proyectos", "categorias")
for c in CATS:
    d = pages.get(c, {})
    cards = "".join(card(p, "proyectos") for p in projects[c])
    if c == "categoria-cliff":
        cards += ('<div class="card note"><b>Proyectos aún sin ficha</b>'
                  '<p class="desc">Apex · Papa · Tacosdepulpo · Chava — la categoría está «en veremos».</p></div>')
    cat_html += (f'<h3 class="gsub">{CAT_ICON.get(c,"")} {html.escape((d.get("title") or c))}</h3>'
                 f'<div class="grid">{card(c, "categorias")}{cards}</div>')

total = len(pages)
stamp = datetime.date.today().isoformat()

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapa del ecosistema — wiki cacho</title>
<style>
 :root{{--bg:#0c0e13;--card:#161a22;--card2:#1c212c;--tx:#e9ecf3;--dim:#93a0b4;--line:#28303f;
 --b:#4da3ff;--g:#3ddc9a;--o:#ffb84d;--p:#c58bff;--r:#ff7a90}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
 .wrap{{max-width:1000px;margin:0 auto;padding:20px 14px 70px}}
 h1{{font-size:23px;margin:0 0 4px}}
 h2{{font-size:19px;margin:36px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}}
 h3.gsub{{font-size:15px;margin:20px 0 8px;color:var(--dim);text-transform:uppercase;letter-spacing:.04em}}
 .sub{{color:var(--dim);font-size:14px;margin:2px 0}}
 .bar{{position:sticky;top:0;z-index:5;background:rgba(12,14,19,.96);border-bottom:1px solid var(--line);padding:10px 0;margin:14px 0}}
 input[type=search]{{width:100%;padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--tx);font-size:15px}}
 .chips{{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}}
 .fchip{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:5px 11px;font-size:13px;color:var(--dim);cursor:pointer}}
 .fchip.on{{background:#22314a;border-color:var(--b);color:#cfe6ff}}
 .count{{font-size:12.5px;color:var(--dim);margin-top:6px}}
 .flowbox{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;margin:10px 0}}
 .arow{{display:flex;flex-direction:column;align-items:center;gap:6px}}
 .node{{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:9px 14px;font-weight:600;font-size:14.5px}}
 .node.me{{border-color:var(--b);color:#cfe6ff}}
 .node.plat{{border-color:var(--g);color:#c9f6e3}}
 .arrow{{color:var(--dim);font-size:15px}}
 .fcats{{display:grid;gap:10px;grid-template-columns:1fr}}
 @media(min-width:680px){{.fcats{{grid-template-columns:1fr 1fr}}}}
 @media(min-width:920px){{.fcats{{grid-template-columns:repeat(3,1fr)}}}}
 .fcat{{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:10px 12px}}
 .fcat-t{{font-size:13.5px;font-weight:600;margin-bottom:7px}}
 .fchips{{display:flex;flex-wrap:wrap;gap:5px}}
 .pchip{{background:#232a37;border:1px solid var(--line);border-radius:8px;padding:3px 8px;font-size:12.5px;color:var(--tx)}}
 .wip{{color:var(--o);font-size:11px;margin-left:6px;font-weight:400}}
 .legendband{{display:grid;gap:10px;grid-template-columns:repeat(3,1fr);text-align:center;font-size:13px;color:var(--dim)}}
 .grid{{display:grid;gap:10px;grid-template-columns:1fr}}
 @media(min-width:760px){{.grid{{grid-template-columns:1fr 1fr}}}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 13px;margin:0}}
 .card[open]{{border-color:#33405a}}
 summary{{cursor:pointer;display:flex;flex-wrap:wrap;align-items:center;gap:7px;font-size:15px;list-style:none}}
 summary::-webkit-details-marker{{display:none}}
 summary::before{{content:"▸";color:var(--dim);font-size:12px}}
 .card[open] summary::before{{content:"▾"}}
 .badge{{background:#232a37;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:11px;color:var(--dim)}}
 .st{{font-size:11px;border-radius:999px;padding:1px 8px;border:1px solid var(--line)}}
 .st-active{{color:var(--g)}} .st-draft{{color:var(--o)}} .st-archived{{color:var(--dim)}}
 .desc{{font-size:14px;color:var(--tx);margin:8px 0 6px}}
 .meta{{font-size:12.5px;color:var(--dim);margin:0}}
 .path{{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;opacity:.75;margin-left:6px}}
 a{{color:var(--b)}}
 .note{{border-style:dashed}}
 .foot{{color:var(--dim);font-size:13px;margin-top:34px;border-top:1px solid var(--line);padding-top:12px}}
</style></head><body><div class="wrap">
<h1>Mapa del ecosistema</h1>
<p class="sub">Todo el wiki <b>cacho</b> en una página: {total} fichas — proyectos, plataforma y runbooks. · {stamp}</p>
<p class="sub">Este es el mapa <b>general</b>. El de <b>videos</b> es otro documento: <a href="ttchop-mapa-documentacion.html">mapa de documentación de video ↗</a> · versión <b>3D</b> navegable: <a href="mapa-pecera.html">🫙 la pecera ↗</a></p>

<div class="bar">
  <input type="search" id="q" placeholder="Buscar: proyecto, hardware, video, ftp…">
  <div class="chips">
    <span class="fchip on" data-f="">Todo</span>
    <span class="fchip" data-f="persona">Persona</span>
    <span class="fchip" data-f="categorias">Categorías</span>
    <span class="fchip" data-f="proyectos">Proyectos</span>
    <span class="fchip" data-f="plataforma">Plataforma</span>
    <span class="fchip" data-f="operaciones">Runbooks</span>
  </div>
  <div class="count" id="count"></div>
</div>

<h2>1 · El flujo</h2>
<div class="flowbox">
  <div class="arow"><div class="node me">👤 Arturo</div>{card("arturo","persona")}<div class="arrow">▼</div>
    <div class="node">6 categorías de proyectos</div><div class="arrow">▼</div></div>
  <div class="fcats">{flow_cats}</div>
  <div class="arow" style="margin-top:14px"><div class="arrow">▼ &nbsp;todo corre sobre&nbsp; ▼</div>
    <div class="legendband">
      <div class="node plat">Hardware</div><div class="node plat">Sistemas</div><div class="node plat">Operaciones</div>
    </div>
  </div>
</div>

<h2>2 · Categorías y proyectos</h2>
{cat_html}

<h2>3 · La plataforma</h2>
<h3 class="gsub">🖥️ Hardware (todo en Tailscale)</h3>
<div class="grid">{hwcards}</div>
<h3 class="gsub">⚙️ Sistemas y repositorios</h3>
<div class="grid">{syscards}</div>

<h2>4 · Operaciones (runbooks)</h2>
{oper_html}

<h2>5 · El repositorio</h2>
<div class="grid">
 <div class="card"><b>index.md — el catálogo</b><p class="desc">Toda página con un resumen de una línea. Es lo primero que se lee.</p></div>
 <div class="card"><b>log.md — la bitácora</b><p class="desc">Qué se hizo cada día, qué falló y qué se aprendió.</p></div>
 <div class="card"><b>Cómo se mantiene</b><p class="desc">Markdown versionado en git (repo público <code>pumacamargo/cacho</code>); cada cambio queda commiteado y pusheado (regla TTC-41).</p></div>
 <div class="card"><b>Para consultarlo completo</b><p class="desc">Ábrelo en Obsidian en la PC (los enlaces <code>[[…]]</code> funcionan) o pulsa cualquier ficha de este mapa para leerla en GitHub.</p></div>
</div>

<div class="foot">Generado desde el propio wiki (<code>web/build-mapa.py</code>) · las descripciones salen de cada ficha, no de un resumen a mano · nada se publica en TikTok sin el OK de Arturo.</div>
</div>
<script>
const q=document.getElementById('q'), chips=[...document.querySelectorAll('.fchip')], cnt=document.getElementById('count');
let area='';
function apply(){{
  const s=q.value.trim().toLowerCase(); let shown=0, all=0;
  document.querySelectorAll('.card[data-area]').forEach(c=>{{
    all++;
    const ok=(!area||c.dataset.area===area) && (!s||c.dataset.text.includes(s));
    c.style.display=ok?'':'none'; if(ok) shown++;
    const g=c.closest('.grid'); if(g) g.style.display=[...g.children].some(x=>x.style.display!=='none')?'':'none';
  }});
  document.querySelectorAll('h3.gsub').forEach(h=>{{
    const g=h.nextElementSibling; if(g&&g.classList.contains('grid')) h.style.display=g.style.display==='none'?'none':'';
  }});
  cnt.textContent=shown+' de '+all+' fichas visibles'+(area?' · área: '+area:'');
}}
q.addEventListener('input',apply);
chips.forEach(c=>c.addEventListener('click',()=>{{chips.forEach(x=>x.classList.remove('on'));c.classList.add('on');area=c.dataset.f;apply();}}));
apply();
</script></body></html>
"""
out = os.path.join(ROOT, "web", "mapa-ecosistema.html")
open(out, "w", encoding="utf-8").write(HTML)
print(f"OK -> {out} ({len(HTML)} bytes, {total} fichas)")
