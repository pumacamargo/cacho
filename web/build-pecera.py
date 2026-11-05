#!/usr/bin/env python3
"""Genera la 'pecera 3D' del wiki (mapa navegable en 3D) -> web/mapa-pecera.html

Lee las fichas reales (entities/ y operations/) y las coloca en capas dentro de un
cilindro de cristal: persona arriba, luego categorías, proyectos, runbooks y la
plataforma al fondo. Se puede orbitar alrededor, hacer zoom y entrar a la pecera.

Uso:  python3 web/build-pecera.py
"""
import os, re, json, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = "https://github.com/pumacamargo/cacho/blob/main"

CATS = ["categoria-backpack", "categoria-cliff", "categoria-macanishi",
        "categoria-moon", "categoria-sandbox", "categoria-tts"]
SISTEMAS = ["hermes-agent", "hermes-agentes", "cacho", "ttchop", "ttchop-automatizaciones", "ttchop-webapps"]
VIDEO = ["ttchop-video-paths", "ttchop-video-generation", "recrear-video-creadores-edits",
         "ttchop-raw-asset-manual-edit", "ttchop-filmcraft-video-tests",
         "traduccion-video-pumasvoice-sincronizada", "ttchop-music-generation", "ttchop-carousel-creation"]
DATOS = ["estudio-creadores-fuentes-datos", "separar-videos-nas-por-cortes", "transcripcion-curso-gerardo-santiago"]
ACCESOS = ["acceso-ftps-lemon-sushi", "acceso-nas-polaris", "acceso-remoto-pumadeskasus", "diagnostico-espacio-disco-vps"]
CLIFF_GHOSTS = ["Apex", "Papa", "Tacosdepulpo", "Chava"]


def read(pid, folder):
    p = os.path.join(ROOT, folder, pid + ".md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    fm, body = (m.group(1), t[m.end():]) if m else ("", t)
    d = {"id": pid, "folder": folder}
    for k in ("title", "type", "status"):
        mm = re.search(rf"^{k}:\s*(.+)$", fm, re.M)
        d[k] = mm.group(1).strip().strip("\"'") if mm else ""
    mm = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    d["tags"] = [x.strip() for x in mm.group(1).split(",") if x.strip()] if mm else []
    for ln in body.split("\n"):
        s = ln.strip()
        if s and not s.startswith(("#", ">", "---", "|", "-")):
            d["desc"] = re.sub(r"\*\*|`", "", re.sub(r"\[\[(.+?)\]\]", r"\1", s))[:240]
            break
    else:
        d["desc"] = ""
    mc = re.search(r"\[\[(categoria-\w+)\]\]", body)
    d["cat"] = mc.group(1).replace("categoria-", "") if mc else ""
    d["gh"] = f"{GH}/{folder}/{pid}.md"
    return d


pages = {}
for folder in ("entities", "operations"):
    for f in sorted(os.listdir(os.path.join(ROOT, folder))):
        if f.endswith(".md"):
            pages[f[:-3]] = read(f[:-3], folder)

nodes = []


def add(pid, area, ring, y, r, color, label=None, pid_gh=None):
    d = pages.get(pid)
    if not d:
        return
    nodes.append({"id": pid, "title": label or d["title"] or pid, "desc": d["desc"], "area": area,
                  "cat": d["cat"], "tags": d["tags"], "status": d["status"],
                  "gh": d["gh"], "ring": ring, "y": y, "r": r, "color": color})


# capa 1 (arriba, centro): Arturo
add("arturo", "persona", "top", 10.6, 0.0, "#4da3ff")
# capa 2: categorías
for i, c in enumerate(CATS):
    add(c, "categorias", "cats", 6.8, 4.9, "#c58bff")
# capa 3: proyectos (+ los 4 de Cliff, que aún no tienen ficha)
projects = [p for p, d in pages.items() if p.startswith("proyecto-")]
for p in projects:
    add(p, "proyectos", "proj", 2.6, 7.9, "#3ddc9a")
for name in CLIFF_GHOSTS:
    nodes.append({"id": "cliff-" + name.lower(), "title": name, "desc": "Proyecto de la categoría Cliff, aún sin ficha (categoría «en veremos»).",
                  "area": "proyectos", "cat": "cliff", "tags": ["pendiente"], "status": "pendiente",
                  "gh": "", "ring": "proj", "y": 2.6, "r": 7.9, "color": "#ffb84d"})
# capa 4: runbooks
for p in VIDEO:
    add(p, "operaciones", "oper", -2.6, 9.6, "#ffb84d")
for p in ACCESOS:
    add(p, "operaciones", "oper", -2.6, 9.6, "#ff9d4d")
for p in DATOS:
    add(p, "operaciones", "oper", -2.6, 9.6, "#ffcf6b")
# capa 5 (fondo): plataforma
for p in sorted([p for p in pages if p.startswith("hardware-")]):
    add(p, "plataforma", "plat", -7.0, 7.4, "#6ec8ff")
for p in SISTEMAS:
    add(p, "plataforma", "plat", -7.0, 7.4, "#6ec8ff")

# reparto angular uniforme + desfase vertical => espiral dentro de la pecera
from collections import defaultdict
import math
byring = defaultdict(list)
for n in nodes:
    byring[n["ring"]].append(n)
SPREAD = {"cats": 0.0, "proj": 3.2, "oper": 2.8, "plat": 2.2}
for ring, items in byring.items():
    if ring == "top":
        for n in items:
            n["ang"] = 0; n["dy"] = 0
        continue
    # ordenar para que la espiral quede agrupada por área/categoría
    items.sort(key=lambda n: (n.get("area", ""), n.get("cat", ""), n["title"]))
    step = 2 * math.pi / len(items)
    sp = SPREAD.get(ring, 0)
    for i, n in enumerate(items):
        n["ang"] = i * step
        n["dy"] = (i - (len(items) - 1) / 2) * (sp / max(1, len(items) - 1)) if sp else 0

# aristas categoría -> sus proyectos (para las líneas)
edges = []
catindex = {c.replace("categoria-", ""): c for c in CATS}
for n in nodes:
    if n["area"] == "proyectos" and n["cat"]:
        parent = catindex.get(n["cat"])
        if parent:
            edges.append([parent, n["id"]])

DATA = {"nodes": nodes, "edges": edges, "today": "2026-11-05"}

HTML = r"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>La pecera — wiki cacho en 3D</title>
<style>
 :root{--bg:#05070c;--tx:#e9ecf3;--dim:#93a0b4;--line:#28303f;--b:#4da3ff;--g:#3ddc9a;--o:#ffb84d}
 *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
 html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);color:var(--tx);
   font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
 #c{position:fixed;inset:0;display:block}
 #labels{position:fixed;inset:0;pointer-events:none}
 .lbl{position:absolute;transform:translate(-50%,-50%);pointer-events:auto;cursor:pointer;max-width:170px;overflow:hidden;text-overflow:ellipsis;
   font-size:11.5px;padding:2px 7px;border-radius:999px;white-space:nowrap;
   background:rgba(8,11,17,.62);border:1px solid rgba(120,140,180,.28);color:#dce6f5;
   transition:opacity .2s, background .2s, border-color .2s;backdrop-filter:blur(3px)}
 .lbl:hover{background:#1d2b45;border-color:var(--b)}
 .lbl.dim{opacity:.16}
 .lbl.off{opacity:0;pointer-events:none}
 .lbl.sel{background:#27406b;border-color:var(--b);color:#fff}
 .lbl small{color:var(--dim);font-size:10px;margin-left:4px}
 header{position:fixed;top:0;left:0;right:0;padding:10px 14px;pointer-events:none;
   background:linear-gradient(180deg,rgba(5,7,12,.92),rgba(5,7,12,0))}
 h1{font-size:16px;margin:0}
 header p{margin:2px 0 0;font-size:12px;color:var(--dim)}
 .ui{position:fixed;pointer-events:auto}
 #tools{left:12px;bottom:12px;display:flex;flex-direction:column;gap:8px;max-width:calc(100% - 24px)}
 .row{display:flex;gap:6px;flex-wrap:wrap}
 .btn{background:rgba(16,20,28,.9);border:1px solid var(--line);color:#dce6f5;border-radius:999px;
   padding:7px 12px;font-size:13px;cursor:pointer}
 .btn:hover{border-color:var(--b)}
 .btn.on{background:#27406b;border-color:var(--b);color:#fff}
 input[type=search]{background:rgba(16,20,28,.92);border:1px solid var(--line);color:var(--tx);
   border-radius:999px;padding:8px 12px;font-size:14px;width:190px;max-width:60vw}
 #legend{right:12px;bottom:12px;font-size:12px;color:var(--dim);text-align:right;line-height:1.7}
 .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
 #panel{left:0;right:0;bottom:0;background:rgba(12,16,23,.97);border-top:1px solid var(--line);
   padding:14px 16px calc(14px + env(safe-area-inset-bottom));transform:translateY(105%);transition:transform .25s}
 #panel.on{transform:none}
 @media(min-width:760px){#panel{left:auto;right:14px;bottom:14px;width:400px;border:1px solid var(--line);border-radius:14px}}
 #panel h2{margin:0 0 4px;font-size:16px}
 #panel .badge{display:inline-block;font-size:11px;color:var(--dim);border:1px solid var(--line);
   border-radius:999px;padding:1px 8px;margin:0 4px 6px 0}
 #panel p{margin:6px 0;font-size:14px;color:#dbe2ee}
 #panel .path{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--dim)}
 #panel a{color:var(--b)}
 #close{position:absolute;top:10px;right:12px;background:none;border:0;color:var(--dim);font-size:20px;cursor:pointer}
 #hint{position:fixed;left:50%;bottom:70px;transform:translateX(-50%);font-size:12.5px;color:var(--dim);
   background:rgba(8,11,17,.8);padding:6px 12px;border-radius:999px;border:1px solid var(--line);
   transition:opacity .4s;pointer-events:none}
</style>
</head><body>
<canvas id="c"></canvas><div id="labels"></div>
<header>
  <h1>🫙 La pecera · wiki <b>cacho</b> en 3D</h1>
  <p>Gira alrededor, haz zoom y entra a la pecera. Toca un nombre para leer su ficha.<br><a href="mapa-ecosistema.html" style="color:#4da3ff">versión plana (lista completa) ↗</a> · <a href="ttchop-mapa-documentacion.html" style="color:#4da3ff">mapa de video ↗</a></p>
</header>
<div id="hint">arrastra para girar · pellizca para zoom · acércate y aparecen los nombres</div>
<div class="ui" id="tools">
  <div class="row"><input type="search" id="q" placeholder="Buscar…"></div>
  <div class="row">
    <span class="btn on" data-f="">Todo</span>
    <span class="btn" data-f="persona">Persona</span>
    <span class="btn" data-f="categorias">Categorías</span>
    <span class="btn" data-f="proyectos">Proyectos</span>
    <span class="btn" data-f="operaciones">Runbooks</span>
    <span class="btn" data-f="plataforma">Plataforma</span>
  </div>
  <div class="row">
    <span class="btn" id="dive">⬇ Entrar a la pecera</span>
    <span class="btn on" id="spin">⟳ Girar solo</span>
    <span class="btn" id="lb">Etiquetas</span>
  </div>
</div>
<div class="ui" id="legend">
  <div><span class="dot" style="background:#4da3ff"></span>persona</div>
  <div><span class="dot" style="background:#c58bff"></span>categorías</div>
  <div><span class="dot" style="background:#3ddc9a"></span>proyectos</div>
  <div><span class="dot" style="background:#ffb84d"></span>runbooks</div>
  <div><span class="dot" style="background:#6ec8ff"></span>plataforma</div>
</div>
<div class="ui" id="panel">
  <button id="close">×</button>
  <h2 id="p-title"></h2>
  <div id="p-badges"></div>
  <p id="p-desc"></p>
  <p id="p-link"></p>
</div>

<script type="importmap">
{"imports":{"three":"./lib/three.module.js","three/addons/":"./lib/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/CSS2DRenderer.js';

const DATA = /*__DATA__*/;
const R = 11.0, TANK_H = 27, WATER_Y = -1.2;

const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:false});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05070c);
scene.fog = new THREE.Fog(0x05070c, 34, 92);

const labelRenderer = new CSS2DRenderer({element: document.getElementById('labels')});
labelRenderer.setSize(innerWidth, innerHeight);

const camera = new THREE.PerspectiveCamera(48, innerWidth/innerHeight, 0.1, 400);
camera.position.set(0, 3.5, 33);

const controls = new OrbitControls(camera, labelRenderer.domElement);
controls.target.set(0, 0.5, 0);
controls.enableDamping = true; controls.dampingFactor = 0.06;
controls.minDistance = 3; controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.54;   // no meterse bajo el piso
controls.minPolarAngle = Math.PI * 0.12;
controls.autoRotate = true; controls.autoRotateSpeed = 0.35;
controls.enablePan = false;

// ── luces
scene.add(new THREE.HemisphereLight(0x9fc8ff, 0x0a1020, 0.75));
const key = new THREE.PointLight(0xffffff, 60, 90); key.position.set(16, 22, 16); scene.add(key);
const rim = new THREE.PointLight(0x59a6ff, 40, 90); rim.position.set(-18, 8, -14); scene.add(rim);
const glow = new THREE.PointLight(0x6ec8ff, 18, 60); glow.position.set(0, -6, 0); scene.add(glow);

// ── cuarto y piso
const floor = new THREE.Mesh(
  new THREE.CircleGeometry(70, 72),
  new THREE.MeshStandardMaterial({color:0x0b1018, roughness:0.95, metalness:0.1}));
floor.rotation.x = -Math.PI/2; floor.position.y = -TANK_H/2 - 1.4; scene.add(floor);
const grid = new THREE.GridHelper(140, 70, 0x1b2740, 0x121b2c);
grid.position.y = floor.position.y + 0.02; scene.add(grid);

// ── la pecera (cristal)
const glassMat = new THREE.MeshPhysicalMaterial({color:0xbfe4ff, metalness:0, roughness:0.08,
  transparent:true, opacity:0.10, side:THREE.DoubleSide, transmission:0.0, clearcoat:1, clearcoatRoughness:0.05});
const glass = new THREE.Mesh(new THREE.CylinderGeometry(R, R, TANK_H, 72, 1, true), glassMat);
scene.add(glass);
const water = new THREE.Mesh(new THREE.CylinderGeometry(R-0.25, R-0.25, TANK_H*0.86, 64, 1, true),
  new THREE.MeshPhysicalMaterial({color:0x2f7bff, transparent:true, opacity:0.07, side:THREE.DoubleSide,
    roughness:0.25, metalness:0}));
water.position.y = WATER_Y - 0.6; scene.add(water);
const surf = new THREE.Mesh(new THREE.CircleGeometry(R-0.3, 64),
  new THREE.MeshPhysicalMaterial({color:0x8fd0ff, transparent:true, opacity:0.16, side:THREE.DoubleSide}));
surf.rotation.x = -Math.PI/2; surf.position.y = WATER_Y + TANK_H*0.43; scene.add(surf);
// aros y base
const ringMat = new THREE.MeshStandardMaterial({color:0x8fa8c8, metalness:0.9, roughness:0.35});
for (const y of [TANK_H/2, WATER_Y + TANK_H*0.43, -TANK_H/2]) {
  const t = new THREE.Mesh(new THREE.TorusGeometry(R, 0.09, 8, 72), ringMat);
  t.rotation.x = Math.PI/2; t.position.y = y; scene.add(t);
}
const base = new THREE.Mesh(new THREE.CylinderGeometry(R+1.1, R+1.6, 1.7, 64),
  new THREE.MeshStandardMaterial({color:0x161c26, metalness:0.6, roughness:0.5}));
base.position.y = -TANK_H/2 - 0.85; scene.add(base);

// ── nodos
const group = new THREE.Group(); scene.add(group);
const meshes = [], links = [];
const byId = {};
for (const n of DATA.nodes) {
  const rad = n.ring === 'top' ? 0.42 : (n.area === 'operaciones' ? 0.26 : 0.33);
  const geo = new THREE.SphereGeometry(rad, 20, 16);
  const col = new THREE.Color(n.color);
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
    color: col, emissive: col.clone().multiplyScalar(0.45), roughness:0.35, metalness:0.2}));
  const a = n.ang || 0;
  m.position.set(Math.cos(a)*n.r, n.y + (n.dy||0), Math.sin(a)*n.r);
  m.userData.id = n.id; group.add(m); meshes.push(m); byId[n.id] = m;

  const el = document.createElement('div');
  el.className = 'lbl'; el.dataset.id = n.id;
  el.innerHTML = n.title + (n.status === 'draft' ? '<small>borrador</small>' : '');
  el.addEventListener('click', () => select(n.id));
  n.el_shown = true;
  const L = new CSS2DObject(el); L.position.copy(m.position).y += rad + 0.55; group.add(L);
  n.el = el;
}
// líneas categoría -> proyectos
const pos = {};
for (const [a, b] of DATA.edges) {
  const ma = byId[a], mb = byId[b];
  if (!ma || !mb) continue;
  const mid = ma.position.clone().lerp(mb.position, 0.5); mid.y -= 0.6;
  const curve = new THREE.QuadraticBezierCurve3(ma.position.clone(), mid, mb.position.clone());
  const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(curve.getPoints(24)),
    new THREE.LineBasicMaterial({color:0x2f4c78, transparent:true, opacity:0.5}));
  group.add(line); links.push(line);
}

// ── selección
const panel = document.getElementById('panel');
let sel = null;
function select(id) {
  const n = DATA.nodes.find(x => x.id === id); if (!n) return;
  sel = id;
  document.querySelectorAll('.lbl').forEach(e => { e.classList.toggle('sel', e.dataset.id === id); if (e.dataset.id === id) e.classList.remove('off'); });
  document.getElementById('p-title').textContent = n.title;
  const badges = [n.area, n.cat, n.status].filter(Boolean)
    .map(t => '<span class="badge">' + t + '</span>').join('');
  document.getElementById('p-badges').innerHTML = badges;
  document.getElementById('p-desc').textContent = n.desc || '';
  document.getElementById('p-link').innerHTML = n.gh
    ? '<a href="' + n.gh + '" target="_blank" rel="noopener">ver ficha completa ↗</a><br><span class="path">' + n.gh.split('/blob/main/')[1] + '</span>'
    : '<span class="path">sin ficha todavía</span>';
  panel.classList.add('on');
  // centrar la cámara en el nodo
  controls.target.lerp(byId[id].position, 0.85);
}
document.getElementById('close').onclick = () => { panel.classList.remove('on'); sel = null;
  document.querySelectorAll('.lbl').forEach(e => e.classList.remove('sel')); };

// ── filtros
let area = '', q = '';
function applyFilter() {
  const s = q.trim().toLowerCase();
  for (const n of DATA.nodes) {
    const ok = (!area || n.area === area) &&
      (!s || (n.title + ' ' + n.desc + ' ' + (n.tags||[]).join(' ')).toLowerCase().includes(s));
    const m = byId[n.id];
    m.visible = ok; n.el.classList.toggle('dim', !ok);
    m.material.opacity = 1;
  }
  for (const l of links) l.visible = (!area || area === 'proyectos' || area === 'categorias') && !s;
}
document.getElementById('q').addEventListener('input', e => { q = e.target.value; applyFilter(); });
document.querySelectorAll('.btn[data-f]').forEach(b => b.onclick = () => {
  document.querySelectorAll('.btn[data-f]').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); area = b.dataset.f; applyFilter();
});

// ── entrar a la pecera
let tween = null;
function flyTo(to, target) { tween = {from: camera.position.clone(), to, tf: controls.target.clone(), tt: target, t: 0}; }
document.getElementById('dive').onclick = () => {
  controls.autoRotate = false; document.getElementById('spin').classList.remove('on');
  flyTo(new THREE.Vector3(0, -1.5, 6.5), new THREE.Vector3(0, 0.5, 0));
  document.getElementById('dive').classList.add('on');
  setTimeout(() => { controls.maxDistance = 26; controls.minDistance = 1.2; }, 900);
};
document.getElementById('spin').onclick = e => {
  controls.autoRotate = !controls.autoRotate; e.target.classList.toggle('on', controls.autoRotate);
  if (controls.autoRotate) { document.getElementById('dive').classList.remove('on');
    controls.maxDistance = 70; flyTo(new THREE.Vector3(0, 4, 34), new THREE.Vector3(0, 0.5, 0)); }
};
document.getElementById('lb').onclick = e => {
  const on = document.getElementById('labels').style.display !== 'none';
  document.getElementById('labels').style.display = on ? 'none' : '';
  e.target.classList.toggle('on', !on);
};

// ── picking
const ray = new THREE.Raycaster(), pt = new THREE.Vector2();
let down = null;
canvas.addEventListener('pointerdown', e => down = {x:e.clientX, y:e.clientY});
canvas.addEventListener('pointerup', e => {
  if (!down || Math.hypot(e.clientX-down.x, e.clientY-down.y) > 6) return;   // fue arrastre
  pt.set((e.clientX/innerWidth)*2-1, -(e.clientY/innerHeight)*2+1);
  ray.setFromCamera(pt, camera);
  const hit = ray.intersectObjects(meshes.filter(m => m.visible))[0];
  if (hit) select(hit.object.userData.id);
});

addEventListener('resize', () => {
  camera.aspect = innerWidth/innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight); labelRenderer.setSize(innerWidth, innerHeight);
});
setTimeout(() => document.getElementById('hint').style.opacity = 0, 6000);

(function loop() {
  requestAnimationFrame(loop);
  if (tween) {
    try {
      tween.t = Math.min(1, tween.t + 0.028);
      const e2 = tween.t < 0.5 ? 2*tween.t*tween.t : 1-Math.pow(-2*tween.t+2, 2)/2;
      camera.position.lerpVectors(tween.from, tween.to, e2);
      controls.target.lerpVectors(tween.tf, tween.tt, e2);
      if (tween.t >= 1) tween = null;
    } catch (err) { console.warn('tween', err); tween = null; }
  }
  // etiquetas: solo el lado de la cámara, y por niveles según qué tan cerca estés
  const dist = camera.position.distanceTo(controls.target);
  const level = dist > 30 ? 0 : (dist > 20 ? 1 : 2);   // 0: solo persona+categorías · 1: +proyectos · 2: todo
  const cambDir = camera.position.clone().setY(0);
  const inside = camera.position.length() < R*1.15;
  const okLevel = n => level === 0 ? (n.ring === 'top' || n.ring === 'cats')
                      : level === 1 ? (n.ring !== 'oper' && n.ring !== 'plat') : true;
  if (inside || cambDir.lengthSq() < 0.01) {
    for (const n of DATA.nodes) if (n.el) n.el.classList.toggle('off', !okLevel(n));
  } else {
    cambDir.normalize();
    for (const n of DATA.nodes) {
      const m = byId[n.id]; if (!m || !n.el) continue;
      const p = m.position.clone().setY(0).normalize();
      const near = m.position.length() < 0.01 || cambDir.dot(p) > -0.12;
      n.el.classList.toggle('off', !(near && okLevel(n)));
    }
  }
  controls.update();
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
})();
</script>
</body></html>
"""

out = os.path.join(ROOT, "web", "mapa-pecera.html")
open(out, "w", encoding="utf-8").write(HTML.replace("/*__DATA__*/", json.dumps(DATA, ensure_ascii=False)))
print(f"OK -> {out} · {len(nodes)} nodos · {len(edges)} aristas")
