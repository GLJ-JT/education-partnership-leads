#!/usr/bin/env python3
import json
from pathlib import Path


DATA = Path("lead-output/combined-uk-turkey-spain-italy-leads-map-data.json")
OUTPUTS = [
    Path("lead-output/combined-uk-turkey-spain-italy-leads-map.html"),
    Path("lead-output/combined-uk-turkey-spain-italy-leads-dashboard-map.html"),
]


def main():
    leads = json.loads(DATA.read_text(encoding="utf-8"))
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Education Partnership Leads Command Center</title>
  <style>
    :root {{
      --bg: #071018;
      --panel: #0c1622;
      --panel-2: #101d2b;
      --text: #e6f3f7;
      --muted: #88a3ad;
      --line: rgba(136, 163, 173, .24);
      --cyan: #33d6d0;
      --blue: #5aa7ff;
      --green: #3ee29c;
      --yellow: #f7c955;
      --red: #ff6b8a;
      --shadow: 0 18px 55px rgba(0, 0, 0, .28);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background:
        linear-gradient(90deg, rgba(51, 214, 208, .06) 1px, transparent 1px),
        linear-gradient(rgba(51, 214, 208, .04) 1px, transparent 1px),
        var(--bg);
      background-size: 36px 36px;
      overflow: hidden;
    }}
    button, input, select, textarea {{ font: inherit; }}
    button {{ cursor: pointer; }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .app {{ height: 100vh; display: grid; grid-template-rows: auto 1fr; overflow: hidden; }}
    .top {{
      display: grid;
      grid-template-columns: minmax(270px, 1fr) auto minmax(320px, 1.2fr);
      gap: 16px;
      align-items: center;
      padding: 14px 18px;
      border-bottom: 1px solid var(--line);
      background: rgba(7, 16, 24, .92);
      backdrop-filter: blur(14px);
    }}
    h1 {{ margin: 0 0 4px; font-size: 20px; line-height: 1.15; letter-spacing: 0; }}
    .sub {{ color: var(--muted); font-size: 12px; }}
    .view-toggle {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      padding: 4px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, .04);
      min-width: 230px;
    }}
    .view-toggle button {{
      border: 0;
      color: var(--muted);
      background: transparent;
      border-radius: 6px;
      padding: 9px 14px;
    }}
    .view-toggle button.active {{
      color: #021014;
      background: linear-gradient(135deg, var(--cyan), var(--blue));
      font-weight: 800;
    }}
    .filters {{ display: grid; grid-template-columns: 1.5fr repeat(4, minmax(96px, .7fr)); gap: 8px; }}
    input, select, textarea {{
      width: 100%;
      min-width: 0;
      color: var(--text);
      background: rgba(255, 255, 255, .055);
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 9px 10px;
      outline: none;
    }}
    textarea {{ min-height: 82px; resize: vertical; }}
    input:focus, select:focus, textarea:focus {{ border-color: rgba(51, 214, 208, .72); box-shadow: 0 0 0 3px rgba(51, 214, 208, .12); }}
    .view {{ min-height: 0; display: none; }}
    .view.active {{ display: grid; }}
    .dashboard {{
      grid-template-columns: 390px minmax(0, 1fr);
      overflow: hidden;
    }}
    .rail, .side {{
      min-height: 0;
      background: rgba(12, 22, 34, .86);
      border-right: 1px solid var(--line);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .rail-head {{ padding: 12px; border-bottom: 1px solid var(--line); display: grid; gap: 10px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
    .metric {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,.045);
      border-radius: 8px;
      padding: 9px;
      min-width: 0;
    }}
    .metric b {{ display: block; font-size: 17px; }}
    .metric span {{ display: block; color: var(--muted); font-size: 10px; white-space: nowrap; }}
    .lead-list {{ flex: 1; min-height: 0; overflow: auto; padding: 8px; overscroll-behavior: contain; }}
    .lead-row {{
      width: 100%;
      display: grid;
      gap: 6px;
      text-align: left;
      color: inherit;
      background: transparent;
      border: 1px solid transparent;
      border-radius: 8px;
      padding: 10px;
    }}
    .lead-row:hover {{ background: rgba(255,255,255,.055); }}
    .lead-row.active {{ border-color: rgba(51,214,208,.72); background: rgba(51,214,208,.11); }}
    .lead-title {{ font-weight: 800; font-size: 13px; line-height: 1.3; }}
    .lead-meta {{ color: var(--muted); display: flex; flex-wrap: wrap; gap: 7px; font-size: 12px; }}
    .badges {{ display: flex; gap: 5px; flex-wrap: wrap; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      max-width: 100%;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 7px;
      font-size: 11px;
      color: var(--muted);
      background: rgba(255,255,255,.045);
    }}
    .badge.Keep, .badge.keep {{ color: var(--green); border-color: rgba(62,226,156,.45); background: rgba(62,226,156,.1); }}
    .badge.Review, .badge.review {{ color: var(--yellow); border-color: rgba(247,201,85,.45); background: rgba(247,201,85,.1); }}
    .badge.Remove, .badge.remove {{ color: var(--red); border-color: rgba(255,107,138,.45); background: rgba(255,107,138,.1); }}
    .detail-shell {{ min-height: 0; overflow: auto; }}
    .detail {{ max-width: 1220px; margin: 0 auto; padding: 18px; }}
    .detail-top {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; margin-bottom: 14px; }}
    h2 {{ margin: 0 0 7px; font-size: 27px; line-height: 1.14; letter-spacing: 0; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }}
    .btn {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,.06);
      color: var(--text);
      border-radius: 7px;
      padding: 8px 10px;
      text-decoration: none;
      font-size: 13px;
    }}
    .btn.primary {{ color: #001316; background: var(--cyan); border-color: var(--cyan); font-weight: 800; }}
    .detail-grid {{ display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(320px, .8fr); gap: 14px; }}
    section {{ border: 1px solid var(--line); border-radius: 8px; background: rgba(12, 22, 34, .88); box-shadow: var(--shadow); overflow: hidden; }}
    section h3 {{ margin: 0; padding: 13px 14px; font-size: 14px; border-bottom: 1px solid var(--line); }}
    .field-grid {{ display: grid; grid-template-columns: 145px 1fr; }}
    .field {{ display: contents; }}
    .field label {{ padding: 11px 14px; color: var(--muted); font-size: 12px; border-bottom: 1px solid var(--line); }}
    .field div {{ padding: 11px 14px; font-size: 13px; border-bottom: 1px solid var(--line); min-width: 0; overflow-wrap: anywhere; }}
    .stack {{ display: grid; gap: 14px; align-content: start; }}
    .status-box {{ padding: 12px 14px; display: grid; gap: 10px; }}
    .check {{ display: grid; grid-template-columns: 18px 1fr; gap: 9px; align-items: start; font-size: 13px; }}
    .check input {{ width: 16px; height: 16px; margin-top: 1px; accent-color: var(--cyan); }}
    .map-view {{ grid-template-columns: minmax(0, 1fr) 380px; min-height: 0; }}
    .map-stage {{ position: relative; min-width: 0; min-height: 0; overflow: hidden; background: #071326; }}
    canvas {{ width: 100%; height: 100%; display: block; touch-action: none; }}
    .map-card {{
      position: absolute;
      left: 16px;
      top: 16px;
      width: min(570px, calc(100% - 32px));
      background: rgba(7, 16, 24, .84);
      border: 1px solid rgba(51,214,208,.26);
      border-radius: 8px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(13px);
      padding: 12px;
      pointer-events: none;
    }}
    .map-card .metrics {{ margin-top: 10px; grid-template-columns: repeat(4, minmax(70px,1fr)); }}
    .zoom-box {{
      position: absolute;
      right: 16px;
      bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px;
      border: 1px solid rgba(51,214,208,.34);
      border-radius: 8px;
      background: rgba(7,16,24,.86);
      box-shadow: var(--shadow);
    }}
    .zoom-box button {{
      width: 42px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 7px;
      color: var(--text);
      background: rgba(255,255,255,.07);
      font-size: 20px;
      line-height: 1;
    }}
    .zoom-box strong {{ min-width: 42px; text-align: center; }}
    .map-panel {{ min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-left: 1px solid var(--line); background: rgba(12, 22, 34, .92); overflow: hidden; }}
    .map-detail {{ padding: 14px; border-bottom: 1px solid var(--line); max-height: 42vh; overflow: auto; }}
    .map-list {{ min-height: 0; overflow: auto; padding: 8px; }}
    .empty {{ padding: 48px; text-align: center; color: var(--muted); }}
    @media (max-width: 980px) {{
      body {{ overflow: auto; }}
      .app {{ height: auto; min-height: 100vh; overflow: visible; }}
      .top {{ grid-template-columns: 1fr; align-items: stretch; }}
      .filters {{ grid-template-columns: 1fr 1fr; }}
      .filters input {{ grid-column: 1 / -1; }}
      .dashboard, .map-view {{ grid-template-columns: 1fr; }}
      .rail {{ height: 52vh; min-height: 420px; border-right: 0; border-bottom: 1px solid var(--line); }}
      .detail-shell {{ overflow: visible; }}
      .detail-grid {{ grid-template-columns: 1fr; }}
      .map-stage {{ height: 60vh; min-height: 430px; }}
      .map-panel {{ border-left: 0; }}
      .field-grid {{ grid-template-columns: 1fr; }}
      .field label {{ border-bottom: 0; padding-bottom: 3px; }}
      .field div {{ padding-top: 0; }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <header class="top">
      <div>
        <h1>Education Partnership Leads Command Center</h1>
        <div class="sub">Combined UK, Turkey, Spain, and Italy lead dashboard with map navigation</div>
      </div>
      <div class="view-toggle" aria-label="View switcher">
        <button id="dashboardTab" class="active" type="button">Dashboard</button>
        <button id="mapTab" type="button">Map</button>
      </div>
      <div class="filters">
        <input id="search" type="search" placeholder="Search name, city, notes, email..." />
        <select id="fit">
          <option value="all">All fit</option>
          <option value="Keep">Keep</option>
          <option value="Review">Review</option>
          <option value="Remove">Remove</option>
        </select>
        <select id="country">
          <option value="all">All countries</option>
          <option value="GB">United Kingdom</option>
          <option value="TR">Turkey</option>
          <option value="ES">Spain</option>
          <option value="IT">Italy</option>
        </select>
        <select id="statusFilter">
          <option value="all">All statuses</option>
          <option value="new">New</option>
          <option value="research">Researching</option>
          <option value="contacted">Contacted</option>
          <option value="followup">Follow-up</option>
          <option value="partner">Partner fit</option>
          <option value="reject">Not fit</option>
        </select>
        <select id="qualityFilter">
          <option value="all">Any contact</option>
          <option value="decision">Has decision maker</option>
          <option value="linkedin">Has LinkedIn</option>
          <option value="email">Has email</option>
          <option value="phone">Has phone</option>
        </select>
      </div>
    </header>

    <section id="dashboardView" class="view dashboard active">
      <aside class="rail">
        <div class="rail-head">
          <div class="metrics">
            <div class="metric"><b id="dashShown">0</b><span>shown</span></div>
            <div class="metric"><b id="dashKeep">0</b><span>keep</span></div>
            <div class="metric"><b id="dashDone">0</b><span>done</span></div>
            <div class="metric"><b id="dashDm">0</b><span>verified DM</span></div>
          </div>
        </div>
        <div id="dashboardList" class="lead-list"></div>
      </aside>
      <main class="detail-shell">
        <div id="dashboardDetail" class="detail"></div>
      </main>
    </section>

    <section id="mapView" class="view map-view">
      <div class="map-stage">
        <canvas id="map"></canvas>
        <div class="map-card">
          <h2 style="font-size:18px;margin:0 0 4px;">Lead Map</h2>
          <div class="sub">Drag pan, use +/- buttons for zoom, click a point to inspect a lead</div>
          <div class="metrics">
            <div class="metric"><b id="mapShown">0</b><span>mapped</span></div>
            <div class="metric"><b id="mapKeep">0</b><span>keep</span></div>
            <div class="metric"><b id="mapReview">0</b><span>review</span></div>
            <div class="metric"><b id="mapRemove">0</b><span>remove</span></div>
          </div>
        </div>
        <div class="zoom-box">
          <button id="zoomOut" type="button" aria-label="Zoom out">-</button>
          <strong id="zoom">4.7</strong>
          <button id="zoomIn" type="button" aria-label="Zoom in">+</button>
        </div>
      </div>
      <aside class="map-panel">
        <div id="mapDetail" class="map-detail"></div>
        <div id="mapList" class="map-list"></div>
      </aside>
    </section>
  </div>
  <script>
    const LEADS = {json.dumps(leads, ensure_ascii=False)};
    const CHECKS = ['Review fit and notes', 'Open website', 'Check decision maker source', 'Open LinkedIn', 'Send cold email', 'Call main/company phone', 'Schedule follow-up'];
    const colors = {{ Keep: '#3ee29c', Review: '#f7c955', Remove: '#ff6b8a' }};
    const tileCache = new Map();
    const state = {{ selected: 0, view: 'dashboard', query: '', fit: 'all', country: 'all', status: 'all', quality: 'all', zoom: 4.7, centerLat: 43.8, centerLon: 8.5, drag: false, moved: false, lastX: 0, lastY: 0 }};
    const canvas = document.getElementById('map');
    const ctx = canvas.getContext('2d');
    const $ = id => document.getElementById(id);
    const safe = v => (v || '').toString().trim();
    const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
    const storeKey = (i, suffix) => `leadDash:v2:${{i}}:${{suffix}}`;
    function esc(value) {{
      return safe(value).replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]));
    }}
    function statusOf(i) {{ return localStorage.getItem(storeKey(i, 'status')) || 'new'; }}
    function statusLabel(value) {{ return ({{ new: 'New', research: 'Researching', contacted: 'Contacted', followup: 'Follow-up', partner: 'Partner fit', reject: 'Not fit' }})[value] || value; }}
    function progressOf(i) {{ return CHECKS.filter((_, c) => localStorage.getItem(storeKey(i, `check:${{c}}`)) === '1').length; }}
    function firstUrl(value) {{ return safe(value).split(';').map(v => v.trim()).filter(Boolean)[0] || ''; }}
    function link(value, label) {{
      const url = firstUrl(value);
      return url ? `<a href="${{esc(url)}}" target="_blank" rel="noreferrer">${{esc(label || url)}}</a>` : '<span class="sub">Blank</span>';
    }}
    function allLinks(value) {{
      return safe(value).split(';').map(v => v.trim()).filter(Boolean).map(v => `<a href="${{esc(v)}}" target="_blank" rel="noreferrer">${{esc(v)}}</a>`).join('<br>') || '<span class="sub">Blank</span>';
    }}
    function displayUrl(value) {{
      const url = firstUrl(value);
      if (!url) return '';
      try {{
        const parsed = new URL(url);
        return parsed.hostname.replace(/^www\\./, '') + parsed.pathname.replace(/\\/$/, '');
      }} catch {{
        return url.replace(/^https?:\\/\\/(www\\.)?/, '').replace(/\\/$/, '');
      }}
    }}
    function passesCommon(lead, i, requireGeo) {{
      if (requireGeo && (lead.lat === null || lead.lon === null || lead.lat === undefined || lead.lon === undefined)) return false;
      if (state.fit !== 'all' && lead.quality_recommendation !== state.fit) return false;
      if (state.country !== 'all' && lead.country !== state.country) return false;
      if (state.status !== 'all' && statusOf(i) !== state.status) return false;
      if (state.quality === 'decision' && !safe(lead.decision_maker_name)) return false;
      if (state.quality === 'linkedin' && !safe(lead.linkedin_company_url + lead.linkedin_person_url)) return false;
      if (state.quality === 'email' && !safe(lead.email + lead.decision_maker_email)) return false;
      if (state.quality === 'phone' && !safe(lead.phone + lead.decision_maker_phone)) return false;
      if (state.query && !Object.values(lead).join(' ').toLowerCase().includes(state.query)) return false;
      return true;
    }}
    function rows(requireGeo = false) {{
      return LEADS.map((lead, i) => ({{ lead, i }})).filter(({{ lead, i }}) => passesCommon(lead, i, requireGeo));
    }}
    function badge(label, klass = '') {{ return label ? `<span class="badge ${{klass}}">${{esc(label)}}</span>` : ''; }}
    function renderLeadButton(lead, i, mapMode = false) {{
      const badges = [
        badge(lead.quality_recommendation, lead.quality_recommendation || ''),
        safe(lead.email) ? badge('email', 'keep') : '',
        safe(lead.phone) ? badge('phone', 'keep') : '',
        safe(lead.decision_maker_name) ? badge('verified DM', 'keep') : badge('no DM', 'review'),
        safe(lead.linkedin_company_url + lead.linkedin_person_url) ? badge('LinkedIn', 'keep') : ''
      ].join('');
      return `<button class="lead-row ${{i === state.selected ? 'active' : ''}}" onclick="selectLead(${{i}}, ${{mapMode ? 'true' : 'false'}})">
        <div class="lead-title">${{esc(lead.business_name)}}</div>
        <div class="lead-meta"><span>${{esc(lead.city || 'No city')}}</span><span>${{esc(lead.country || '')}}</span><span>score ${{esc(lead.score || 0)}}</span><span>${{esc(statusLabel(statusOf(i)))}}</span><span>${{progressOf(i)}}/${{CHECKS.length}}</span></div>
        <div class="badges">${{badges}}</div>
      </button>`;
    }}
    function field(label, html) {{ return `<div class="field"><label>${{esc(label)}}</label><div>${{html || '<span class="sub">Blank</span>'}}</div></div>`; }}
    function renderDetail(targetId, compact = false) {{
      const lead = LEADS[state.selected];
      if (!lead) {{ $(targetId).innerHTML = '<div class="empty">Select a lead.</div>'; return; }}
      const checks = CHECKS.map((text, c) => `<label class="check"><input type="checkbox" ${{localStorage.getItem(storeKey(state.selected, `check:${{c}}`)) === '1' ? 'checked' : ''}} onchange="setCheck(${{state.selected}}, ${{c}}, this.checked)"><span>${{esc(text)}}</span></label>`).join('');
      const actions = `<div class="actions">
        ${{lead.website ? `<a class="btn primary" href="${{esc(firstUrl(lead.website))}}" target="_blank" rel="noreferrer">Website</a>` : ''}}
        ${{lead.google_maps_url ? `<a class="btn" href="${{esc(firstUrl(lead.google_maps_url))}}" target="_blank" rel="noreferrer">Maps</a>` : ''}}
        ${{firstUrl(lead.linkedin_company_url || lead.linkedin_person_url) ? `<a class="btn" href="${{esc(firstUrl(lead.linkedin_company_url || lead.linkedin_person_url))}}" target="_blank" rel="noreferrer">LinkedIn</a>` : ''}}
        ${{lead.email ? `<a class="btn" href="mailto:${{esc(firstUrl(lead.email))}}">Email</a>` : ''}}
      </div>`;
      const profile = `<section><h3>Lead Profile</h3><div class="field-grid">
        ${{field('Website', link(lead.website, displayUrl(lead.website) || 'Open website'))}}
        ${{field('Email', esc(lead.email))}}
        ${{field('Phone', esc(lead.phone))}}
        ${{field('Instagram', allLinks(lead.instagram))}}
        ${{field('Company LinkedIn', allLinks(lead.linkedin_company_url))}}
        ${{field('Person LinkedIn', allLinks(lead.linkedin_person_url))}}
        ${{field('Notes', esc(lead.notes))}}
      </div></section>`;
      const audit = `<section><h3>Quality Audit</h3><div class="field-grid">
        ${{field('Recommendation', badge(lead.quality_recommendation, lead.quality_recommendation || ''))}}
        ${{field('Grade', esc(lead.quality_grade))}}
        ${{field('Market role', esc(lead.market_role))}}
        ${{field('Reason', esc(lead.quality_reason))}}
      </div></section>`;
      const dm = `<section><h3>Verified Decision Maker</h3><div class="field-grid">
        ${{field('Name', esc(lead.decision_maker_name))}}
        ${{field('Title', esc(lead.decision_maker_title))}}
        ${{field('Email', esc(lead.decision_maker_email))}}
        ${{field('Phone route', esc(lead.decision_maker_phone))}}
        ${{field('Source', link(lead.decision_source_url, lead.decision_source_type || lead.decision_source_url))}}
        ${{field('Confidence', esc(lead.decision_confidence))}}
      </div></section>`;
      const status = `<section><h3>Outreach Status</h3><div class="status-box">
        <select onchange="setStatus(${{state.selected}}, this.value)">${{['new','research','contacted','followup','partner','reject'].map(s => `<option value="${{s}}" ${{s === statusOf(state.selected) ? 'selected' : ''}}>${{statusLabel(s)}}</option>`).join('')}}</select>
        ${{checks}}
        <textarea placeholder="Call notes, objections, follow-up date..." oninput="setNote(${{state.selected}}, this.value)">${{esc(localStorage.getItem(storeKey(state.selected, 'note')) || '')}}</textarea>
      </div></section>`;
      const top = `<div class="detail-top"><div><h2>${{esc(lead.business_name)}}</h2><div class="sub">${{esc(lead.city || '')}} ${{esc(lead.country || '')}} · score ${{esc(lead.score || 0)}} · ${{esc(lead.market_role || '')}}</div><div class="badges" style="margin-top:9px;">${{badge(lead.quality_recommendation, lead.quality_recommendation || '')}}${{badge(lead.quality_grade)}}${{badge(lead.decision_confidence || 'no verified DM')}}</div></div>${{actions}}</div>`;
      if (compact) {{
        $(targetId).innerHTML = `${{top}}${{audit}}${{dm}}`;
      }} else {{
        $(targetId).innerHTML = `${{top}}<div class="detail-grid">${{profile}}<div class="stack">${{audit}}${{status}}${{dm}}</div></div>`;
      }}
    }}
    function renderDashboard() {{
      const visible = rows(false);
      if (!visible.some(r => r.i === state.selected)) state.selected = visible.length ? visible[0].i : -1;
      $('dashShown').textContent = visible.length;
      $('dashKeep').textContent = visible.filter(r => r.lead.quality_recommendation === 'Keep').length;
      $('dashDone').textContent = LEADS.reduce((n, _, i) => n + (progressOf(i) === CHECKS.length ? 1 : 0), 0);
      $('dashDm').textContent = LEADS.filter(l => safe(l.decision_maker_name)).length;
      $('dashboardList').innerHTML = visible.map(({{ lead, i }}) => renderLeadButton(lead, i, false)).join('') || '<div class="empty">No leads match these filters.</div>';
      renderDetail('dashboardDetail', false);
    }}
    function renderMapPanel() {{
      const visible = rows(true);
      if (!visible.some(r => r.i === state.selected) && visible.length) state.selected = visible[0].i;
      $('mapShown').textContent = visible.length;
      $('mapKeep').textContent = visible.filter(r => r.lead.quality_recommendation === 'Keep').length;
      $('mapReview').textContent = visible.filter(r => r.lead.quality_recommendation === 'Review').length;
      $('mapRemove').textContent = visible.filter(r => r.lead.quality_recommendation === 'Remove').length;
      $('mapList').innerHTML = visible.map(({{ lead, i }}) => renderLeadButton(lead, i, true)).join('') || '<div class="empty">No mapped leads match these filters.</div>';
      renderDetail('mapDetail', true);
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
      const x0 = Math.floor(startX / 256), x1 = Math.floor((center.x + w / 2) / 256);
      const y0 = Math.floor(startY / 256), y1 = Math.floor((center.y + h / 2) / 256);
      ctx.fillStyle = '#071326';
      ctx.fillRect(0, 0, w, h);
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {{
        const img = getTile(z, x, y);
        const px = Math.round(x * 256 - startX);
        const py = Math.round(y * 256 - startY);
        if (img && img.complete && img.naturalWidth) ctx.drawImage(img, px, py, 256, 256);
        else {{
          ctx.fillStyle = '#0d213b';
          ctx.fillRect(px, py, 256, 256);
          ctx.strokeStyle = 'rgba(51,214,208,.09)';
          ctx.strokeRect(px, py, 256, 256);
        }}
      }}
      ctx.fillStyle = 'rgba(2, 6, 23, .18)';
      ctx.fillRect(0, 0, w, h);
    }}
    function mapPoint(lat, lon, w, h) {{
      const z = Math.floor(clamp(state.zoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, z);
      const p = lonLatToWorld(lon, lat, z);
      return {{ x: w / 2 + p.x - center.x, y: h / 2 + p.y - center.y }};
    }}
    function drawPoints(w, h) {{
      for (const entry of rows(true)) {{
        const p = mapPoint(entry.lead.lat, entry.lead.lon, w, h);
        if (p.x < -30 || p.x > w + 30 || p.y < -30 || p.y > h + 30) continue;
        const active = entry.i === state.selected;
        ctx.strokeStyle = colors[entry.lead.quality_recommendation] || '#33d6d0';
        ctx.globalAlpha = active ? .42 : .2;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(p.x, p.y, active ? 18 : 11, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.fillStyle = colors[entry.lead.quality_recommendation] || '#33d6d0';
        ctx.strokeStyle = active ? '#fff' : 'rgba(226,245,255,.75)';
        ctx.lineWidth = active ? 3 : 1.5;
        ctx.beginPath();
        ctx.arc(p.x, p.y, active ? 7 : 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }}
    }}
    function draw() {{
      if (state.view !== 'map') return;
      const w = canvas.clientWidth, h = canvas.clientHeight;
      if (!w || !h) return;
      ctx.clearRect(0, 0, w, h);
      drawTiles(w, h);
      drawPoints(w, h);
      $('zoom').textContent = state.zoom.toFixed(1);
    }}
    function resize() {{
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }}
    function selectLead(i, fly) {{
      state.selected = i;
      const lead = LEADS[i];
      if (fly && lead && lead.lat !== null && lead.lat !== undefined) {{
        state.centerLat = lead.lat;
        state.centerLon = lead.lon;
        state.zoom = Math.max(state.zoom, 8.2);
      }}
      renderDashboard();
      renderMapPanel();
      draw();
    }}
    function pointAt(x, y) {{
      let best = null;
      const w = canvas.clientWidth, h = canvas.clientHeight;
      for (const entry of rows(true)) {{
        const p = mapPoint(entry.lead.lat, entry.lead.lon, w, h);
        const d = Math.hypot(p.x - x, p.y - y);
        if (d < 15 && (!best || d < best.d)) best = {{ ...entry, d }};
      }}
      if (best) selectLead(best.i, false);
    }}
    function zoomAround(anchor, delta) {{
      const oldZ = Math.floor(clamp(state.zoom, 3, 14));
      const center = lonLatToWorld(state.centerLon, state.centerLat, oldZ);
      const before = worldToLonLat(center.x + anchor.x - canvas.clientWidth / 2, center.y + anchor.y - canvas.clientHeight / 2, oldZ);
      state.zoom = clamp(state.zoom + delta, 3, 14);
      const newZ = Math.floor(clamp(state.zoom, 3, 14));
      const afterWorld = lonLatToWorld(before.lon, before.lat, newZ);
      const next = worldToLonLat(afterWorld.x - (anchor.x - canvas.clientWidth / 2), afterWorld.y - (anchor.y - canvas.clientHeight / 2), newZ);
      state.centerLon = next.lon;
      state.centerLat = clamp(next.lat, -82, 82);
      draw();
    }}
    function setView(view) {{
      state.view = view;
      $('dashboardView').classList.toggle('active', view === 'dashboard');
      $('mapView').classList.toggle('active', view === 'map');
      $('dashboardTab').classList.toggle('active', view === 'dashboard');
      $('mapTab').classList.toggle('active', view === 'map');
      if (view === 'map') requestAnimationFrame(resize);
    }}
    function setStatus(i, value) {{ localStorage.setItem(storeKey(i, 'status'), value); renderDashboard(); renderMapPanel(); }}
    function setCheck(i, c, checked) {{ localStorage.setItem(storeKey(i, `check:${{c}}`), checked ? '1' : '0'); renderDashboard(); renderMapPanel(); }}
    function setNote(i, value) {{ localStorage.setItem(storeKey(i, 'note'), value); }}
    function refreshAll() {{ renderDashboard(); renderMapPanel(); draw(); }}
    $('dashboardTab').addEventListener('click', () => setView('dashboard'));
    $('mapTab').addEventListener('click', () => setView('map'));
    $('search').addEventListener('input', e => {{ state.query = e.target.value.toLowerCase(); refreshAll(); }});
    $('fit').addEventListener('change', e => {{ state.fit = e.target.value; refreshAll(); }});
    $('country').addEventListener('change', e => {{ state.country = e.target.value; refreshAll(); }});
    $('statusFilter').addEventListener('change', e => {{ state.status = e.target.value; refreshAll(); }});
    $('qualityFilter').addEventListener('change', e => {{ state.quality = e.target.value; refreshAll(); }});
    $('zoomIn').addEventListener('click', () => zoomAround({{ x: canvas.clientWidth / 2, y: canvas.clientHeight / 2 }}, .7));
    $('zoomOut').addEventListener('click', () => zoomAround({{ x: canvas.clientWidth / 2, y: canvas.clientHeight / 2 }}, -.7));
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
      draw();
    }});
    canvas.addEventListener('pointerup', e => {{ state.drag = false; if (!state.moved) pointAt(e.offsetX, e.offsetY); }});
    window.addEventListener('resize', resize);
    renderDashboard();
    renderMapPanel();
  </script>
</body>
</html>
"""
    for path in OUTPUTS:
        path.write_text(html, encoding="utf-8")
        print(path)
    print(f"leads={len(leads)} mapped={sum(1 for lead in leads if lead.get('lat') is not None and lead.get('lon') is not None)}")


if __name__ == "__main__":
    main()
