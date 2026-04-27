#!/usr/bin/env python3
import json
from pathlib import Path


INPUT = Path("lead-output/education-partnership-leads-50-quality-audit.json")
OUTPUT = Path("lead-output/education-partnership-leads-earth-map.html")


COORDS = {
    ("Aberdeen", "GB"): (57.1497, -2.0943),
    ("Bank", "GB"): (49.9167, -6.3167),
    ("Bishop's Stortford", "GB"): (51.8720, 0.1630),
    ("Blackpool", "GB"): (53.8175, -3.0357),
    ("Bridge of Weir", "GB"): (55.8550, -4.5780),
    ("Brighton", "GB"): (50.8225, -0.1372),
    ("Bristol", "GB"): (51.4545, -2.5879),
    ("Burgess Hill", "GB"): (50.9580, -0.1330),
    ("Egham", "GB"): (51.4316, -0.5524),
    ("Isle of Skye", "GB"): (57.2736, -6.2155),
    ("Isle of South Uist", "GB"): (57.3330, -7.3330),
    ("Isles of Scilly", "GB"): (49.9277, -6.3275),
    ("Liverpool", "GB"): (53.4084, -2.9916),
    ("London", "GB"): (51.5072, -0.1276),
    ("Malvern", "GB"): (52.1116, -2.3265),
    ("Manchester", "GB"): (53.4808, -2.2426),
    ("Menstrie", "GB"): (56.1510, -3.8540),
    ("Newcastle upon Tyne", "GB"): (54.9783, -1.6178),
    ("Oxford", "GB"): (51.7520, -1.2577),
    ("Penzance", "GB"): (50.1188, -5.5376),
    ("Shrewsbury", "GB"): (52.7073, -2.7553),
    ("Stourbridge", "GB"): (52.4561, -2.1479),
    ("Telford", "GB"): (52.6784, -2.4453),
    ("Ventnor", "GB"): (50.5940, -1.2070),
    ("Warrington", "GB"): (53.3900, -2.5960),
    ("Westcliff-on-Sea", "GB"): (51.5440, 0.6910),
    ("Başakşehir", "TR"): (41.0930, 28.8020),
    ("Beyoğlu", "TR"): (41.0370, 28.9770),
    ("Eceabat", "TR"): (40.1840, 26.3570),
    ("Edremit", "TR"): (39.5960, 27.0240),
    ("Fatih", "TR"): (41.0180, 28.9490),
    ("Kepez", "TR"): (36.9120, 30.7090),
    ("Kâhta", "TR"): (37.7850, 38.6230),
    ("Maçka", "TR"): (40.8100, 39.6130),
    ("Selçuklu", "TR"): (37.9440, 32.5100),
    ("Çanakkale Merkez", "TR"): (40.1553, 26.4142),
}


def clean_email(value):
    parts = []
    for part in (value or "").replace("%20", "").split(";"):
        part = part.strip()
        if part and part.lower() not in [existing.lower() for existing in parts]:
            parts.append(part)
    return "; ".join(parts)


def with_coords(row):
    item = dict(row)
    lat, lon = COORDS.get((item.get("city", ""), item.get("country", "")), (None, None))
    item["email"] = clean_email(item.get("email", ""))
    item["lat"] = lat
    item["lon"] = lon
    return item


def main():
    leads = [with_coords(row) for row in json.loads(INPUT.read_text(encoding="utf-8"))]
    data = json.dumps(leads, ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lead Map Command Center</title>
  <style>
    :root {{
      --bg: #020617;
      --glass: rgba(8, 18, 32, .76);
      --line: rgba(103, 232, 249, .26);
      --cyan: #67e8f9;
      --text: #e5f4ff;
      --muted: #9fb7ca;
      --keep: #2dd4bf;
      --review: #fbbf24;
      --remove: #fb7185;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      overflow: hidden;
      background: #020617;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .app {{ height: 100vh; display: grid; grid-template-columns: minmax(0, 1fr) 390px; }}
    .viewport {{ position: relative; min-width: 0; overflow: hidden; background: #071326; }}
    #map {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; cursor: grab; }}
    #map:active {{ cursor: grabbing; }}
    .scanlines {{
      pointer-events: none;
      position: absolute;
      inset: 0;
      background: linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px);
      background-size: 100% 4px;
      mix-blend-mode: screen;
      opacity: .14;
    }}
    .hud {{
      position: absolute;
      left: 20px;
      top: 18px;
      width: min(460px, calc(100% - 40px));
      display: grid;
      gap: 12px;
      pointer-events: none;
    }}
    .title, .controls, .readout {{
      pointer-events: auto;
      background: linear-gradient(135deg, rgba(8,18,32,.88), rgba(8,18,32,.62));
      border: 1px solid var(--line);
      border-radius: 10px;
      box-shadow: 0 0 28px rgba(34,211,238,.11);
      backdrop-filter: blur(10px);
    }}
    .title {{ padding: 14px; }}
    .title h1 {{ margin: 0 0 5px; font-size: 24px; line-height: 1.05; letter-spacing: 0; }}
    .title div {{ color: var(--muted); font-size: 13px; }}
    .controls {{ padding: 10px; display: grid; gap: 9px; }}
    input, select {{
      width: 100%;
      min-width: 0;
      color: var(--text);
      background: rgba(2,6,23,.78);
      border: 1px solid rgba(103,232,249,.28);
      border-radius: 8px;
      padding: 9px 10px;
      font: inherit;
      outline: none;
    }}
    input::placeholder {{ color: #7d91a6; }}
    .control-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
    .metric {{
      border: 1px solid rgba(103,232,249,.22);
      border-radius: 8px;
      background: rgba(2,6,23,.62);
      padding: 8px;
    }}
    .metric b {{ display: block; color: #fff; font-size: 17px; }}
    .metric span {{ color: var(--muted); font-size: 11px; }}
    .readout {{
      position: absolute;
      left: 20px;
      bottom: 18px;
      display: flex;
      gap: 12px;
      align-items: center;
      padding: 10px 12px;
      color: var(--muted);
      font-size: 12px;
    }}
    .readout strong {{ color: var(--cyan); }}
    .readout button {{
      width: 28px;
      height: 28px;
      border: 1px solid rgba(103,232,249,.35);
      border-radius: 7px;
      color: var(--text);
      background: rgba(2,6,23,.75);
      font: 700 18px/1 system-ui;
      cursor: pointer;
    }}
    .readout button:hover {{ border-color: var(--cyan); color: #fff; }}
    aside {{
      height: 100vh;
      overflow: hidden;
      display: grid;
      grid-template-rows: auto 1fr;
      background: linear-gradient(180deg, rgba(7,18,34,.95), rgba(4,10,20,.95));
      border-left: 1px solid var(--line);
      box-shadow: -22px 0 50px rgba(0,0,0,.44);
    }}
    .detail {{ padding: 18px; border-bottom: 1px solid var(--line); }}
    .detail h2 {{ margin: 0 0 6px; font-size: 22px; line-height: 1.12; letter-spacing: 0; color: #fff; }}
    .sub {{ color: var(--muted); font-size: 13px; }}
    .badge-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0 2px; }}
    .badge {{
      border: 1px solid rgba(103,232,249,.24);
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 11px;
      color: var(--muted);
      background: rgba(2,6,23,.62);
    }}
    .badge.Keep {{ color: #99f6e4; border-color: rgba(45,212,191,.55); }}
    .badge.Review {{ color: #fde68a; border-color: rgba(251,191,36,.55); }}
    .badge.Remove {{ color: #fecdd3; border-color: rgba(251,113,133,.55); }}
    .fields {{ margin-top: 14px; border: 1px solid var(--line); border-radius: 9px; overflow: hidden; }}
    .field {{ display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid rgba(103,232,249,.18); }}
    .field:last-child {{ border-bottom: 0; }}
    .field label {{ padding: 9px 10px; color: var(--muted); font-size: 12px; background: rgba(103,232,249,.06); }}
    .field div {{ padding: 9px 10px; font-size: 13px; overflow-wrap: anywhere; }}
    a {{ color: var(--cyan); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .list {{ min-height: 0; overflow: auto; padding: 10px; }}
    .lead {{
      width: 100%;
      text-align: left;
      border: 1px solid transparent;
      border-radius: 8px;
      background: transparent;
      color: inherit;
      padding: 10px;
      cursor: pointer;
      display: grid;
      gap: 5px;
    }}
    .lead:hover {{ background: rgba(103,232,249,.07); }}
    .lead.active {{ background: rgba(20,184,166,.12); border-color: rgba(45,212,191,.58); }}
    .lead strong {{ font-size: 13px; color: #fff; }}
    .lead span {{ color: var(--muted); font-size: 12px; }}
    @media (max-width: 980px) {{
      body {{ overflow: auto; }}
      .app {{ height: auto; grid-template-columns: 1fr; }}
      .viewport {{ height: 64vh; }}
      aside {{ height: auto; min-height: 560px; }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <div class="viewport">
      <canvas id="map"></canvas>
      <div class="scanlines"></div>
      <div class="hud">
        <div class="title">
          <h1>Lead Map Command Center</h1>
          <div>Flat map navigation · drag pan · use zoom buttons · click a lead point</div>
        </div>
        <div class="controls">
          <input id="search" type="search" placeholder="Search lead, city, market role..." />
          <div class="control-grid">
            <select id="fit">
              <option value="all">All fit grades</option>
              <option value="Keep">Keep</option>
              <option value="Review">Review</option>
              <option value="Remove">Remove</option>
            </select>
            <select id="country">
              <option value="all">All countries</option>
              <option value="GB">United Kingdom</option>
              <option value="TR">Turkey</option>
            </select>
          </div>
          <div class="metrics">
            <div class="metric"><b id="shown">50</b><span>shown</span></div>
            <div class="metric"><b id="keep">30</b><span>keep</span></div>
            <div class="metric"><b id="review">6</b><span>review</span></div>
            <div class="metric"><b id="remove">14</b><span>remove</span></div>
          </div>
        </div>
      </div>
      <div class="readout">
        <button id="zoomOut" type="button" aria-label="Zoom out">-</button>
        <strong id="zoom">5.0</strong>
        <button id="zoomIn" type="button" aria-label="Zoom in">+</button>
        <span>Dark basemap tiles</span>
      </div>
    </div>
    <aside>
      <div id="detail" class="detail"></div>
      <div id="list" class="list"></div>
    </aside>
  </div>
  <script>
    const LEADS = {data};
    const tileCache = new Map();
    const colors = {{ Keep: '#2dd4bf', Review: '#fbbf24', Remove: '#fb7185' }};
    const state = {{
      selected: 0,
      fit: 'all',
      country: 'all',
      query: '',
      zoom: 5.4,
      centerLat: 49.6,
      centerLon: 14.4,
      drag: false,
      moved: false,
      lastX: 0,
      lastY: 0
    }};
    const canvas = document.getElementById('map');
    const ctx = canvas.getContext('2d');
    function safe(v) {{ return (v || '').toString().trim(); }}
    function clamp(v, min, max) {{ return Math.max(min, Math.min(max, v)); }}
    function link(url, label) {{
      url = safe(url).split(';')[0].trim();
      if (!url) return '<span class="sub">Blank</span>';
      return `<a href="${{url}}" target="_blank" rel="noreferrer">${{label || url}}</a>`;
    }}
    function allLinks(value) {{
      return safe(value).split(';').map(v => v.trim()).filter(Boolean).map(v => `<a href="${{v}}" target="_blank" rel="noreferrer">${{v}}</a>`).join('<br>') || '<span class="sub">Blank</span>';
    }}
    function filtered() {{
      const q = state.query.toLowerCase();
      return LEADS.map((lead, i) => ({{ lead, i }})).filter(({{ lead }}) => {{
        if (lead.lat === null || lead.lon === null) return false;
        if (state.fit !== 'all' && lead.quality_recommendation !== state.fit) return false;
        if (state.country !== 'all' && lead.country !== state.country) return false;
        if (q && !Object.values(lead).join(' ').toLowerCase().includes(q)) return false;
        return true;
      }});
    }}
    function lonLatToWorld(lon, lat, z) {{
      const scale = 256 * Math.pow(2, z);
      const x = (lon + 180) / 360 * scale;
      const s = Math.sin(lat * Math.PI / 180);
      const y = (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) * scale;
      return {{ x, y }};
    }}
    function worldToLonLat(x, y, z) {{
      const scale = 256 * Math.pow(2, z);
      const lon = x / scale * 360 - 180;
      const n = Math.PI - 2 * Math.PI * y / scale;
      const lat = 180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n)));
      return {{ lon, lat }};
    }}
    function getTile(z, x, y) {{
      const max = Math.pow(2, z);
      x = ((x % max) + max) % max;
      if (y < 0 || y >= max) return null;
      const key = `${{z}}/${{x}}/${{y}}`;
      if (tileCache.has(key)) return tileCache.get(key);
      const img = new Image();
      img.src = `https://basemaps.cartocdn.com/dark_all/${{z}}/${{x}}/${{y}}.png`;
      img.onload = draw;
      tileCache.set(key, img);
      return img;
    }}
    function drawTiles(w, h) {{
      const z = Math.floor(clamp(state.zoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, z);
      const startX = center.x - w / 2;
      const startY = center.y - h / 2;
      const endX = center.x + w / 2;
      const endY = center.y + h / 2;
      const x0 = Math.floor(startX / 256), x1 = Math.floor(endX / 256);
      const y0 = Math.floor(startY / 256), y1 = Math.floor(endY / 256);
      ctx.fillStyle = '#071326';
      ctx.fillRect(0, 0, w, h);
      for (let y = y0; y <= y1; y++) {{
        for (let x = x0; x <= x1; x++) {{
          const img = getTile(z, x, y);
          const px = Math.round(x * 256 - startX);
          const py = Math.round(y * 256 - startY);
          if (img && img.complete && img.naturalWidth) {{
            ctx.drawImage(img, px, py, 256, 256);
          }} else {{
            ctx.fillStyle = '#0d213b';
            ctx.fillRect(px, py, 256, 256);
            ctx.strokeStyle = 'rgba(103,232,249,.09)';
            ctx.strokeRect(px, py, 256, 256);
          }}
        }}
      }}
      ctx.fillStyle = 'rgba(2, 6, 23, .2)';
      ctx.fillRect(0, 0, w, h);
    }}
    function mapPoint(lat, lon, w, h) {{
      const z = Math.floor(clamp(state.zoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, z);
      const p = lonLatToWorld(lon, lat, z);
      return {{ x: w / 2 + p.x - center.x, y: h / 2 + p.y - center.y }};
    }}
    function drawPoints(w, h) {{
      for (const entry of filtered()) {{
        const p = mapPoint(entry.lead.lat, entry.lead.lon, w, h);
        if (p.x < -30 || p.x > w + 30 || p.y < -30 || p.y > h + 30) continue;
        const active = entry.i === state.selected;
        ctx.strokeStyle = colors[entry.lead.quality_recommendation] || '#67e8f9';
        ctx.globalAlpha = active ? .42 : .2;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(p.x, p.y, active ? 18 : 11, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.fillStyle = colors[entry.lead.quality_recommendation] || '#67e8f9';
        ctx.strokeStyle = active ? '#ffffff' : 'rgba(226,245,255,.75)';
        ctx.lineWidth = active ? 3 : 1.5;
        ctx.beginPath();
        ctx.arc(p.x, p.y, active ? 7 : 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }}
    }}
    function draw() {{
      const w = canvas.clientWidth, h = canvas.clientHeight;
      ctx.clearRect(0, 0, w, h);
      drawTiles(w, h);
      drawPoints(w, h);
      document.getElementById('zoom').textContent = state.zoom.toFixed(1);
    }}
    function scheduleDraw() {{
      if (state.drawFrame) return;
      state.drawFrame = requestAnimationFrame(() => {{
        state.drawFrame = null;
        draw();
      }});
    }}
    function resize() {{
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }}
    function renderList() {{
      const rows = filtered();
      if (!rows.some(r => r.i === state.selected)) state.selected = rows.length ? rows[0].i : -1;
      document.getElementById('shown').textContent = rows.length;
      document.getElementById('keep').textContent = rows.filter(r => r.lead.quality_recommendation === 'Keep').length;
      document.getElementById('review').textContent = rows.filter(r => r.lead.quality_recommendation === 'Review').length;
      document.getElementById('remove').textContent = rows.filter(r => r.lead.quality_recommendation === 'Remove').length;
      document.getElementById('list').innerHTML = rows.map(({{ lead, i }}) => `<button class="lead ${{i === state.selected ? 'active' : ''}}" onclick="selectLead(${{i}}, true)">
        <strong>${{lead.business_name}}</strong>
        <span>${{lead.city}} ${{lead.country}} · ${{lead.quality_recommendation}} · ${{lead.market_role || ''}}</span>
      </button>`).join('') || '<div class="sub" style="padding:20px">No leads match these filters.</div>';
    }}
    function field(label, html) {{ return `<div class="field"><label>${{label}}</label><div>${{html || '<span class="sub">Blank</span>'}}</div></div>`; }}
    function renderDetail() {{
      const lead = LEADS[state.selected];
      if (!lead) {{ document.getElementById('detail').innerHTML = '<h2>No lead selected</h2>'; return; }}
      document.getElementById('detail').innerHTML = `<h2>${{lead.business_name}}</h2>
        <div class="sub">${{lead.city}} ${{lead.country}} · score ${{lead.score || 0}}</div>
        <div class="badge-row">
          <span class="badge ${{lead.quality_recommendation}}">${{lead.quality_recommendation}}</span>
          <span class="badge">${{lead.quality_grade || 'No grade'}}</span>
          <span class="badge">${{lead.market_role || 'No role'}}</span>
        </div>
        <div class="fields">
          ${{field('Reason', safe(lead.quality_reason))}}
          ${{field('Website', link(lead.website, 'Open website'))}}
          ${{field('Email', safe(lead.email))}}
          ${{field('Phone', safe(lead.phone))}}
          ${{field('LinkedIn', allLinks(lead.linkedin_company_url || lead.linkedin_person_url))}}
          ${{field('Decision', safe(lead.decision_maker_name))}}
          ${{field('Title', safe(lead.decision_maker_title))}}
          ${{field('Source', link(lead.decision_source_url, lead.decision_source_type))}}
        </div>`;
    }}
    function selectLead(i, fly) {{
      state.selected = i;
      const lead = LEADS[i];
      if (fly && lead && lead.lat !== null) {{
        state.centerLat = lead.lat;
        state.centerLon = lead.lon;
        state.zoom = Math.max(state.zoom, 8.2);
      }}
      renderList();
      renderDetail();
      draw();
    }}
    function pointAt(x, y) {{
      let best = null;
      const w = canvas.clientWidth, h = canvas.clientHeight;
      for (const entry of filtered()) {{
        const p = mapPoint(entry.lead.lat, entry.lead.lon, w, h);
        const d = Math.hypot(p.x - x, p.y - y);
        if (d < 15 && (!best || d < best.d)) best = {{ ...entry, d }};
      }}
      if (best) selectLead(best.i, false);
    }}
    function zoomAround(anchor, zoomDelta) {{
      if (!zoomDelta) return;
      const oldZoom = state.zoom;
      const oldZ = Math.floor(clamp(oldZoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, oldZ);
      const before = worldToLonLat(
        center.x + anchor.x - canvas.clientWidth / 2,
        center.y + anchor.y - canvas.clientHeight / 2,
        oldZ
      );
      state.zoom = clamp(oldZoom + zoomDelta, 3, 14);
      const newZ = Math.floor(clamp(state.zoom, 3, 14));
      const afterWorld = lonLatToWorld(before.lon, before.lat, newZ);
      const next = worldToLonLat(
        afterWorld.x - (anchor.x - canvas.clientWidth / 2),
        afterWorld.y - (anchor.y - canvas.clientHeight / 2),
        newZ
      );
      state.centerLon = next.lon;
      state.centerLat = clamp(next.lat, -82, 82);
    }}
    function buttonZoom(delta) {{
      zoomAround({{ x: canvas.clientWidth / 2, y: canvas.clientHeight / 2 }}, delta);
      draw();
    }}
    canvas.addEventListener('wheel', e => e.preventDefault(), {{ passive: false }});
    canvas.addEventListener('pointerdown', e => {{ state.drag = true; state.moved = false; state.lastX = e.clientX; state.lastY = e.clientY; canvas.setPointerCapture(e.pointerId); }});
    canvas.addEventListener('pointermove', e => {{
      if (!state.drag) return;
      const dx = e.clientX - state.lastX, dy = e.clientY - state.lastY;
      if (Math.abs(dx) + Math.abs(dy) > 3) state.moved = true;
      state.lastX = e.clientX; state.lastY = e.clientY;
      const z = Math.floor(clamp(state.zoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, z);
      const next = worldToLonLat(center.x - dx, center.y - dy, z);
      state.centerLon = next.lon;
      state.centerLat = clamp(next.lat, -82, 82);
      scheduleDraw();
    }});
    canvas.addEventListener('pointerup', e => {{ state.drag = false; if (!state.moved) pointAt(e.offsetX, e.offsetY); }});
    document.getElementById('search').addEventListener('input', e => {{ state.query = e.target.value; renderList(); renderDetail(); draw(); }});
    document.getElementById('fit').addEventListener('change', e => {{ state.fit = e.target.value; renderList(); renderDetail(); draw(); }});
    document.getElementById('country').addEventListener('change', e => {{ state.country = e.target.value; renderList(); renderDetail(); draw(); }});
    document.getElementById('zoomIn').addEventListener('click', () => buttonZoom(0.7));
    document.getElementById('zoomOut').addEventListener('click', () => buttonZoom(-0.7));
    window.addEventListener('resize', resize);
    renderList();
    renderDetail();
    resize();
  </script>
</body>
</html>
"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
