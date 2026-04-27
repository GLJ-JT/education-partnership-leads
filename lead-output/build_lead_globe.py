#!/usr/bin/env python3
import json
from pathlib import Path


INPUT = Path("lead-output/education-partnership-leads-50-quality-audit.json")
OUTPUT = Path("lead-output/education-partnership-leads-globe.html")


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


def with_coords(row):
    lat, lon = COORDS.get((row.get("city", ""), row.get("country", "")), (None, None))
    item = dict(row)
    email_parts = []
    for part in item.get("email", "").replace("%20", "").split(";"):
        part = part.strip()
        if part and part.lower() not in [existing.lower() for existing in email_parts]:
            email_parts.append(part)
    item["email"] = "; ".join(email_parts)
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
  <title>Lead Globe</title>
  <style>
    :root {{
      --bg: #09111f;
      --panel: rgba(255,255,255,.94);
      --text: #17202a;
      --muted: #667085;
      --line: #d9e0ea;
      --keep: #14b8a6;
      --review: #f59e0b;
      --remove: #ef4444;
      --water: #0f2447;
      --land: #244d66;
      --grid: rgba(213, 226, 245, .22);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{ margin: 0; overflow: hidden; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at 50% 45%, #132b4d, var(--bg) 70%); color: var(--text); }}
    .app {{ height: 100vh; display: grid; grid-template-columns: minmax(0, 1fr) 390px; }}
    .stage {{ position: relative; min-width: 0; overflow: hidden; }}
    canvas {{ width: 100%; height: 100%; display: block; cursor: grab; }}
    canvas:active {{ cursor: grabbing; }}
    .hud {{ position: absolute; left: 22px; top: 20px; display: grid; gap: 12px; width: min(420px, calc(100% - 44px)); pointer-events: none; }}
    .title {{ color: #fff; text-shadow: 0 1px 18px rgba(0,0,0,.45); }}
    .title h1 {{ margin: 0 0 5px; font-size: 28px; line-height: 1.1; letter-spacing: 0; }}
    .title div {{ color: #cbd5e1; font-size: 13px; }}
    .filters {{ pointer-events: auto; background: rgba(255,255,255,.95); border: 1px solid rgba(255,255,255,.6); box-shadow: 0 10px 30px rgba(0,0,0,.22); border-radius: 8px; padding: 10px; display: grid; gap: 9px; }}
    input, select {{ width: 100%; border: 1px solid var(--line); border-radius: 7px; padding: 9px 10px; font: inherit; min-width: 0; background: #fff; }}
    .filter-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
    .metric {{ background: #f8fafc; border: 1px solid var(--line); border-radius: 7px; padding: 8px; }}
    .metric b {{ display: block; font-size: 17px; }}
    .metric span {{ font-size: 11px; color: var(--muted); }}
    aside {{ height: 100vh; overflow: hidden; display: grid; grid-template-rows: auto 1fr; background: var(--panel); border-left: 1px solid rgba(255,255,255,.5); box-shadow: -12px 0 32px rgba(0,0,0,.22); }}
    .detail {{ padding: 18px; border-bottom: 1px solid var(--line); }}
    .detail h2 {{ margin: 0 0 6px; font-size: 22px; line-height: 1.15; letter-spacing: 0; }}
    .sub {{ color: var(--muted); font-size: 13px; }}
    .badge-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0 2px; }}
    .badge {{ border-radius: 999px; padding: 3px 8px; font-size: 11px; border: 1px solid var(--line); background: #fff; color: var(--muted); }}
    .badge.Keep {{ color: #065f46; border-color: #99f6e4; background: #ecfdf5; }}
    .badge.Review {{ color: #854d0e; border-color: #fde68a; background: #fffbeb; }}
    .badge.Remove {{ color: #991b1b; border-color: #fecaca; background: #fef2f2; }}
    .fields {{ margin-top: 14px; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }}
    .field {{ display: grid; grid-template-columns: 115px 1fr; border-bottom: 1px solid var(--line); }}
    .field:last-child {{ border-bottom: 0; }}
    .field label {{ padding: 9px 10px; color: var(--muted); font-size: 12px; background: #f8fafc; }}
    .field div {{ padding: 9px 10px; font-size: 13px; overflow-wrap: anywhere; }}
    a {{ color: #1d4ed8; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .list {{ min-height: 0; overflow: auto; padding: 10px; }}
    .lead {{ width: 100%; border: 1px solid transparent; background: transparent; color: inherit; text-align: left; border-radius: 7px; padding: 10px; cursor: pointer; display: grid; gap: 5px; }}
    .lead:hover {{ background: #f1f5f9; }}
    .lead.active {{ background: #e8f7f5; border-color: #99d9d1; }}
    .lead strong {{ font-size: 13px; }}
    .lead span {{ color: var(--muted); font-size: 12px; }}
    .legend {{ position: absolute; left: 22px; bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; color: #dbeafe; font-size: 12px; background: rgba(8, 17, 33, .6); border: 1px solid rgba(255,255,255,.14); padding: 9px 10px; border-radius: 8px; }}
    .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }}
    .help {{ position: absolute; right: 18px; bottom: 18px; color: #cbd5e1; font-size: 12px; background: rgba(8, 17, 33, .55); padding: 8px 10px; border-radius: 8px; }}
    @media (max-width: 980px) {{
      body {{ overflow: auto; }}
      .app {{ height: auto; grid-template-columns: 1fr; }}
      .stage {{ height: 58vh; }}
      aside {{ height: auto; min-height: 520px; }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <div class="stage">
      <canvas id="globe"></canvas>
      <div class="hud">
        <div class="title">
          <h1>Lead Globe</h1>
          <div>UK/China camp prospecting view · drag to rotate · click a point</div>
        </div>
        <div class="filters">
          <input id="search" type="search" placeholder="Search lead, city, role..." />
          <div class="filter-grid">
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
      <div class="legend">
        <span><i class="dot" style="background:var(--keep)"></i>Keep</span>
        <span><i class="dot" style="background:var(--review)"></i>Review</span>
        <span><i class="dot" style="background:var(--remove)"></i>Remove</span>
      </div>
      <div class="help">Scroll list separately · points are approximate city locations</div>
    </div>
    <aside>
      <div id="detail" class="detail"></div>
      <div id="list" class="list"></div>
    </aside>
  </div>
  <script>
    const LEADS = {data};
    const state = {{ selected: 0, fit: 'all', country: 'all', query: '', yaw: -0.1, pitch: 0.1, dragging: false, lastX: 0, lastY: 0 }};
    const canvas = document.getElementById('globe');
    const ctx = canvas.getContext('2d');
    const colors = {{ Keep: '#14b8a6', Review: '#f59e0b', Remove: '#ef4444' }};
    const countryCenters = {{ GB: [54, -2], TR: [39, 35] }};

    function safe(v) {{ return (v || '').toString().trim(); }}
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
        if (state.fit !== 'all' && lead.quality_recommendation !== state.fit) return false;
        if (state.country !== 'all' && lead.country !== state.country) return false;
        if (q && !Object.values(lead).join(' ').toLowerCase().includes(q)) return false;
        return lead.lat !== null && lead.lon !== null;
      }});
    }}
    function llToVec(lat, lon) {{
      const phi = lat * Math.PI / 180;
      const lam = lon * Math.PI / 180;
      return [Math.cos(phi) * Math.sin(lam), Math.sin(phi), Math.cos(phi) * Math.cos(lam)];
    }}
    function rotate(vec) {{
      let [x, y, z] = vec;
      const cy = Math.cos(state.yaw), sy = Math.sin(state.yaw);
      const cp = Math.cos(state.pitch), sp = Math.sin(state.pitch);
      const x1 = cy * x + sy * z;
      const z1 = -sy * x + cy * z;
      const y1 = cp * y - sp * z1;
      const z2 = sp * y + cp * z1;
      return [x1, y1, z2];
    }}
    function project(lat, lon, radius, cx, cy) {{
      const [x, y, z] = rotate(llToVec(lat, lon));
      return {{ x: cx + x * radius, y: cy - y * radius, z }};
    }}
    function resize() {{
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }}
    function drawGraticule(radius, cx, cy) {{
      ctx.strokeStyle = 'rgba(213,226,245,.22)';
      ctx.lineWidth = 1;
      for (let lat = -60; lat <= 60; lat += 30) {{
        ctx.beginPath();
        for (let lon = -180; lon <= 180; lon += 4) {{
          const p = project(lat, lon, radius, cx, cy);
          if (p.z < -0.08) continue;
          if (lon === -180) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }}
        ctx.stroke();
      }}
      for (let lon = -180; lon < 180; lon += 30) {{
        ctx.beginPath();
        let started = false;
        for (let lat = -80; lat <= 80; lat += 4) {{
          const p = project(lat, lon, radius, cx, cy);
          if (p.z < -0.08) {{ started = false; continue; }}
          if (!started) {{ ctx.moveTo(p.x, p.y); started = true; }} else ctx.lineTo(p.x, p.y);
        }}
        ctx.stroke();
      }}
    }}
    function drawRegion(lat, lon, label, radius, cx, cy) {{
      const p = project(lat, lon, radius, cx, cy);
      if (p.z < -0.05) return;
      ctx.fillStyle = 'rgba(86, 141, 169, .85)';
      ctx.beginPath();
      ctx.arc(p.x, p.y, Math.max(18, radius * .06), 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#dbeafe';
      ctx.font = '12px system-ui';
      ctx.fillText(label, p.x + 16, p.y - 10);
    }}
    function draw() {{
      const w = canvas.clientWidth, h = canvas.clientHeight;
      ctx.clearRect(0, 0, w, h);
      const radius = Math.min(w, h) * .37;
      const cx = w * .48, cy = h * .53;
      const grad = ctx.createRadialGradient(cx - radius * .35, cy - radius * .45, radius * .05, cx, cy, radius);
      grad.addColorStop(0, '#2d5f88');
      grad.addColorStop(.7, '#102a50');
      grad.addColorStop(1, '#071326');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.fill();
      drawGraticule(radius, cx, cy);
      drawRegion(54, -2, 'UK', radius, cx, cy);
      drawRegion(39, 35, 'Turkey', radius, cx, cy);
      const points = filtered().map((entry) => {{
        const p = project(entry.lead.lat, entry.lead.lon, radius, cx, cy);
        return {{ ...entry, ...p }};
      }}).filter(p => p.z > -0.03).sort((a, b) => a.z - b.z);
      for (const p of points) {{
        const isActive = p.i === state.selected;
        ctx.fillStyle = colors[p.lead.quality_recommendation] || '#93c5fd';
        ctx.strokeStyle = isActive ? '#ffffff' : 'rgba(255,255,255,.65)';
        ctx.lineWidth = isActive ? 3 : 1.5;
        ctx.beginPath();
        ctx.arc(p.x, p.y, isActive ? 8 : 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }}
    }}
    function renderList() {{
      const rows = filtered();
      if (!rows.some(r => r.i === state.selected)) state.selected = rows.length ? rows[0].i : -1;
      document.getElementById('shown').textContent = rows.length;
      document.getElementById('keep').textContent = rows.filter(r => r.lead.quality_recommendation === 'Keep').length;
      document.getElementById('review').textContent = rows.filter(r => r.lead.quality_recommendation === 'Review').length;
      document.getElementById('remove').textContent = rows.filter(r => r.lead.quality_recommendation === 'Remove').length;
      document.getElementById('list').innerHTML = rows.map(({{ lead, i }}) => `<button class="lead ${{i === state.selected ? 'active' : ''}}" onclick="selectLead(${{i}})">
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
          ${{field('Decision maker', safe(lead.decision_maker_name))}}
          ${{field('Title', safe(lead.decision_maker_title))}}
          ${{field('Source', link(lead.decision_source_url, lead.decision_source_type))}}
        </div>`;
    }}
    function selectLead(i) {{ state.selected = i; renderList(); renderDetail(); draw(); }}
    function pickPoint(x, y) {{
      const w = canvas.clientWidth, h = canvas.clientHeight;
      const radius = Math.min(w, h) * .37;
      const cx = w * .48, cy = h * .53;
      let best = null;
      for (const entry of filtered()) {{
        const p = project(entry.lead.lat, entry.lead.lon, radius, cx, cy);
        if (p.z < -0.03) continue;
        const d = Math.hypot(p.x - x, p.y - y);
        if (d < 13 && (!best || d < best.d)) best = {{ ...entry, d }};
      }}
      if (best) selectLead(best.i);
    }}
    canvas.addEventListener('pointerdown', e => {{ state.dragging = true; state.lastX = e.clientX; state.lastY = e.clientY; canvas.setPointerCapture(e.pointerId); }});
    canvas.addEventListener('pointermove', e => {{
      if (!state.dragging) return;
      const dx = e.clientX - state.lastX, dy = e.clientY - state.lastY;
      state.yaw += dx * 0.006;
      state.pitch = Math.max(-1.2, Math.min(1.2, state.pitch + dy * 0.006));
      state.lastX = e.clientX; state.lastY = e.clientY;
      draw();
    }});
    canvas.addEventListener('pointerup', e => {{ state.dragging = false; pickPoint(e.offsetX, e.offsetY); }});
    document.getElementById('search').addEventListener('input', e => {{ state.query = e.target.value; renderList(); renderDetail(); draw(); }});
    document.getElementById('fit').addEventListener('change', e => {{ state.fit = e.target.value; renderList(); renderDetail(); draw(); }});
    document.getElementById('country').addEventListener('change', e => {{ state.country = e.target.value; renderList(); renderDetail(); draw(); }});
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
