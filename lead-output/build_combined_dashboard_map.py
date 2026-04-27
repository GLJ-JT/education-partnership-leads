#!/usr/bin/env python3
import json
from pathlib import Path


WORLDWIDE_DATA = Path("lead-output/combined-worldwide-education-partnership-leads-map-data.json")
BASE_DATA = Path("lead-output/combined-uk-turkey-spain-italy-leads-map-data.json")
DATA = WORLDWIDE_DATA if WORLDWIDE_DATA.exists() else BASE_DATA
OUTPUTS = [
    Path("lead-output/combined-uk-turkey-spain-italy-leads-map.html"),
    Path("lead-output/combined-uk-turkey-spain-italy-leads-dashboard-map.html"),
]


def main():
    leads = json.loads(DATA.read_text(encoding="utf-8"))
    country_names = {
        "AE": "United Arab Emirates",
        "AR": "Argentina",
        "AU": "Australia",
        "BR": "Brazil",
        "CA": "Canada",
        "CN": "China",
        "CO": "Colombia",
        "DE": "Germany",
        "ES": "Spain",
        "FR": "France",
        "GB": "United Kingdom",
        "ID": "Indonesia",
        "IE": "Ireland",
        "IN": "India",
        "INT": "International",
        "IT": "Italy",
        "JP": "Japan",
        "KR": "South Korea",
        "MX": "Mexico",
        "MY": "Malaysia",
        "NL": "Netherlands",
        "NG": "Nigeria",
        "PK": "Pakistan",
        "PL": "Poland",
        "SA": "Saudi Arabia",
        "SG": "Singapore",
        "TH": "Thailand",
        "TR": "Turkey",
        "VN": "Vietnam",
        "ZA": "South Africa",
    }
    countries = sorted({lead.get("country") for lead in leads if lead.get("country")})
    country_options = "\n".join(
        f'          <option value="{code}">{country_names.get(code, code)}</option>'
        for code in countries
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Education Partnership Leads Command Center</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    :root {{
      --bg: #f6f7fb;
      --panel: #ffffff;
      --panel-2: #f7f8fb;
      --text: #181b34;
      --muted: #676879;
      --line: #dfe3eb;
      --cyan: #0073ea;
      --blue: #579bfc;
      --green: #00c875;
      --yellow: #fdab3d;
      --red: #e2445c;
      --purple: #a25ddc;
      --shadow: 0 10px 28px rgba(29, 30, 43, .08);
      --control: #ffffff;
      --toggle-bg: #eef1f7;
      --hover-bg: #f0f6ff;
      --active-bg: #eaf3ff;
      --chip-bg: #f7f8fb;
      --map-bg: #e8edf5;
      --tile-filter: saturate(.92) contrast(.98);
      --top-shadow: 0 1px 2px rgba(29, 30, 43, .04);
    }}
    body[data-theme="dark"] {{
      --bg: #111827;
      --panel: #1f2937;
      --panel-2: #273244;
      --text: #f4f7fb;
      --muted: #a9b4c3;
      --line: #374151;
      --cyan: #579bfc;
      --blue: #7fb3ff;
      --green: #00c875;
      --yellow: #fdab3d;
      --red: #ff5f77;
      --shadow: 0 14px 34px rgba(0, 0, 0, .28);
      --control: #151e2d;
      --toggle-bg: #151e2d;
      --hover-bg: #243149;
      --active-bg: #12345f;
      --chip-bg: #273244;
      --map-bg: #172033;
      --tile-filter: invert(1) hue-rotate(180deg) saturate(.72) brightness(.82) contrast(.9);
      --top-shadow: 0 1px 0 rgba(255, 255, 255, .04);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background: var(--bg);
      overflow: hidden;
    }}
    button, input, select, textarea {{ font: inherit; }}
    button {{ cursor: pointer; }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .app {{ height: 100vh; display: grid; grid-template-rows: auto 1fr; overflow: hidden; }}
    .top {{
      display: grid;
      grid-template-columns: minmax(260px, .85fr) auto minmax(540px, 1.55fr);
      gap: 16px;
      align-items: center;
      padding: 14px 20px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--top-shadow);
    }}
    h1 {{ margin: 0 0 4px; font-size: 20px; line-height: 1.15; letter-spacing: 0; }}
    .sub {{ color: var(--muted); font-size: 12px; }}
    .view-toggle {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      padding: 4px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--toggle-bg);
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
      color: #fff;
      background: var(--cyan);
      font-weight: 800;
    }}
    .theme-toggle {{
      width: 42px;
      min-width: 42px;
      height: 42px;
      display: inline-grid;
      place-items: center;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--text);
      background: var(--control);
      font-size: 16px;
    }}
    .toolbar {{ display: grid; grid-template-columns: auto auto; gap: 12px; align-items: center; }}
    .filters {{ display: grid; grid-template-columns: minmax(220px, 1.4fr) repeat(4, minmax(112px, .7fr)); gap: 8px; }}
    input, select, textarea {{
      width: 100%;
      min-width: 0;
      color: var(--text);
      background: var(--control);
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 9px 10px;
      outline: none;
    }}
    textarea {{ min-height: 82px; resize: vertical; }}
    input:focus, select:focus, textarea:focus {{ border-color: var(--cyan); box-shadow: 0 0 0 3px rgba(0, 115, 234, .12); }}
    .view {{ min-height: 0; display: none; }}
    .view.active {{ display: grid; }}
    .dashboard {{
      grid-template-columns: 390px minmax(0, 1fr);
      overflow: hidden;
    }}
    .rail, .side {{
      min-height: 0;
      background: var(--panel);
      border-right: 1px solid var(--line);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .rail-head {{ padding: 12px; border-bottom: 1px solid var(--line); display: grid; gap: 10px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
    .metric {{
      border: 1px solid var(--line);
      background: var(--panel-2);
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
    .lead-row:hover {{ background: var(--hover-bg); }}
    .lead-row.active {{ border-color: rgba(0,115,234,.45); background: var(--active-bg); }}
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
      background: var(--chip-bg);
    }}
    .badge.Keep, .badge.keep {{ color: #037f4c; border-color: rgba(0,200,117,.28); background: rgba(0,200,117,.12); }}
    .badge.Review, .badge.review {{ color: #9d5d00; border-color: rgba(253,171,61,.34); background: rgba(253,171,61,.14); }}
    .badge.Remove, .badge.remove {{ color: #bb3354; border-color: rgba(226,68,92,.28); background: rgba(226,68,92,.12); }}
    .detail-shell {{ min-height: 0; overflow: auto; }}
    .detail {{ max-width: 1220px; margin: 0 auto; padding: 18px; }}
    .detail-top {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; margin-bottom: 14px; }}
    h2 {{ margin: 0 0 7px; font-size: 27px; line-height: 1.14; letter-spacing: 0; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }}
    .btn {{
      border: 1px solid var(--line);
      background: var(--control);
      color: var(--text);
      border-radius: 7px;
      padding: 8px 10px;
      text-decoration: none;
      font-size: 13px;
    }}
    .btn.primary {{ color: #fff; background: var(--cyan); border-color: var(--cyan); font-weight: 800; }}
    .detail-grid {{ display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(320px, .8fr); gap: 14px; }}
    section {{ border: 1px solid var(--line); border-radius: 8px; background: var(--panel); box-shadow: var(--shadow); overflow: hidden; }}
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
    .map-stage {{ position: relative; min-width: 0; min-height: 0; overflow: hidden; background: var(--map-bg); }}
    #map {{ width: 100%; height: 100%; min-height: 0; background: var(--map-bg); cursor: grab; }}
    #map:active {{ cursor: grabbing; }}
    .leaflet-container {{ background: var(--map-bg); font-family: inherit; }}
    .leaflet-control-attribution {{ display: none; }}
    .leaflet-tile {{ filter: var(--tile-filter); }}
    .lead-marker {{
      width: 15px;
      height: 15px;
      border-radius: 999px;
      border: 2px solid var(--panel);
      box-shadow: 0 0 0 5px rgba(0, 115, 234, .14), 0 6px 16px rgba(29, 30, 43, .18);
      transform: translate(-50%, -50%);
    }}
    .lead-marker.Keep {{ background: var(--green); box-shadow: 0 0 0 5px rgba(0, 200, 117, .14), 0 6px 16px rgba(29, 30, 43, .18); }}
    .lead-marker.Review {{ background: var(--yellow); box-shadow: 0 0 0 5px rgba(253, 171, 61, .18), 0 6px 16px rgba(29, 30, 43, .18); }}
    .lead-marker.Remove {{ background: var(--red); box-shadow: 0 0 0 5px rgba(226, 68, 92, .14), 0 6px 16px rgba(29, 30, 43, .18); }}
    .lead-marker.active {{
      width: 21px;
      height: 21px;
      border-width: 3px;
      box-shadow: 0 0 0 10px rgba(0, 115, 234, .18), 0 9px 22px rgba(29, 30, 43, .22);
    }}
    .lead-tooltip {{
      color: var(--text);
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 0;
      white-space: normal;
      width: 260px;
    }}
    .lead-tooltip::before {{ display: none; }}
    .lead-tip {{ display: grid; gap: 7px; padding: 10px 11px; }}
    .lead-tip strong {{ display: block; font-size: 13px; line-height: 1.25; }}
    .lead-tip-meta {{ display: flex; gap: 6px; flex-wrap: wrap; color: var(--muted); font-size: 11px; }}
    .lead-tip-role {{ color: #323338; font-size: 11px; line-height: 1.35; }}
    .lead-tip-signals {{ display: flex; gap: 5px; flex-wrap: wrap; }}
    .lead-tip-signals span {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 6px;
      color: var(--muted);
      background: var(--chip-bg);
      font-size: 10px;
    }}
    .map-card {{
      position: absolute;
      left: 16px;
      top: 16px;
      width: min(570px, calc(100% - 32px));
      background: color-mix(in srgb, var(--panel) 94%, transparent);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
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
      border: 1px solid var(--line);
      border-radius: 8px;
      background: color-mix(in srgb, var(--panel) 94%, transparent);
      box-shadow: var(--shadow);
    }}
    .zoom-box button {{
      width: 42px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 7px;
      color: var(--text);
      background: var(--control);
      font-size: 20px;
      line-height: 1;
    }}
    .zoom-box strong {{ min-width: 42px; text-align: center; }}
    .map-panel {{ min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-left: 1px solid var(--line); background: var(--panel); overflow: hidden; }}
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
        <h1>Education Partnership Leads</h1>
        <div class="sub">Worldwide education partnership lead dashboard with map navigation</div>
      </div>
      <div class="toolbar">
        <div class="view-toggle" aria-label="View switcher">
          <button id="dashboardTab" class="active" type="button">Dashboard</button>
          <button id="mapTab" type="button">Map</button>
        </div>
        <button id="themeToggle" class="theme-toggle" type="button" aria-label="Switch to dark mode" title="Switch theme">◐</button>
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
{country_options}
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
        <div id="map"></div>
        <div class="map-card">
          <h2 style="font-size:18px;margin:0 0 4px;">Lead Map</h2>
          <div class="sub">Leaflet map · smooth trackpad zoom · drag pan · click a point to inspect a lead</div>
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
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const LEADS = {json.dumps(leads, ensure_ascii=False)};
    const CHECKS = ['Review fit and notes', 'Open website', 'Check decision maker source', 'Open LinkedIn', 'Send cold email', 'Call main/company phone', 'Schedule follow-up'];
    const colors = {{ Keep: '#3ee29c', Review: '#f7c955', Remove: '#ff6b8a' }};
    const state = {{ selected: 0, view: 'dashboard', query: '', fit: 'all', country: 'all', status: 'all', quality: 'all', zoom: 2.45, centerLat: 28, centerLon: 18 }};
    const themeKey = 'leadDash:theme';
    function applyTheme(theme) {{
      document.body.dataset.theme = theme;
      localStorage.setItem(themeKey, theme);
      const dark = theme === 'dark';
      $('themeToggle').textContent = dark ? '☀' : '◐';
      $('themeToggle').setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    }}
    const map = L.map('map', {{
      zoomControl: false,
      attributionControl: false,
      scrollWheelZoom: true,
      wheelDebounceTime: 12,
      wheelPxPerZoomLevel: 170,
      zoomSnap: 0.25,
      zoomDelta: 0.5,
      inertia: true,
      inertiaDeceleration: 2600,
      easeLinearity: 0.2,
      preferCanvas: true
    }}).setView([state.centerLat, state.centerLon], state.zoom);
    L.tileLayer('https://basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 18,
      minZoom: 3,
      crossOrigin: true
    }}).addTo(map);
    const markerLayer = L.layerGroup().addTo(map);
    const markerByLead = new Map();
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
    function markerIcon(lead, active) {{
      return L.divIcon({{
        className: '',
        html: `<div class="lead-marker ${{esc(lead.quality_recommendation)}} ${{active ? 'active' : ''}}"></div>`,
        iconSize: [active ? 21 : 15, active ? 21 : 15],
        iconAnchor: [0, 0]
      }});
    }}
    function tooltipHtml(lead) {{
      const signals = [
        safe(lead.email) ? '<span>email</span>' : '',
        safe(lead.phone) ? '<span>phone</span>' : '',
        safe(lead.decision_maker_name) ? '<span>verified DM</span>' : '',
        safe(lead.linkedin_company_url + lead.linkedin_person_url) ? '<span>LinkedIn</span>' : ''
      ].join('');
      return `<div class="lead-tip">
        <strong>${{esc(lead.business_name)}}</strong>
        <div class="lead-tip-meta">
          <span>${{esc(lead.city || 'No city')}}</span>
          <span>${{esc(lead.country || '')}}</span>
          <span>${{esc(lead.quality_recommendation || 'Unaudited')}}</span>
          <span>score ${{esc(lead.score || 0)}}</span>
        </div>
        <div class="lead-tip-role">${{esc(lead.market_role || lead.quality_reason || '')}}</div>
        ${{signals ? `<div class="lead-tip-signals">${{signals}}</div>` : ''}}
      </div>`;
    }}
    function updateZoomReadout() {{
      state.zoom = map.getZoom();
      const center = map.getCenter();
      state.centerLat = center.lat;
      state.centerLon = center.lng;
      $('zoom').textContent = state.zoom.toFixed(1);
    }}
    function renderMarkers() {{
      markerLayer.clearLayers();
      markerByLead.clear();
      for (const entry of rows(true)) {{
        const marker = L.marker([entry.lead.lat, entry.lead.lon], {{
          icon: markerIcon(entry.lead, entry.i === state.selected),
          keyboard: false,
          riseOnHover: true,
          title: entry.lead.business_name || ''
        }});
        marker.bindTooltip(tooltipHtml(entry.lead), {{
          className: 'lead-tooltip',
          direction: 'top',
          offset: [0, -13],
          opacity: 1,
          sticky: true
        }});
        marker.on('click', () => selectLead(entry.i, false));
        marker.addTo(markerLayer);
        markerByLead.set(entry.i, marker);
      }}
      updateZoomReadout();
    }}
    function resize() {{
      map.invalidateSize({{ animate: false }});
      updateZoomReadout();
    }}
    function selectLead(i, fly) {{
      state.selected = i;
      const lead = LEADS[i];
      if (fly && lead && lead.lat !== null && lead.lat !== undefined) {{
        state.centerLat = lead.lat;
        state.centerLon = lead.lon;
        map.flyTo([lead.lat, lead.lon], Math.max(map.getZoom(), 8.2), {{ duration: 0.65, easeLinearity: 0.2 }});
      }}
      renderDashboard();
      renderMapPanel();
      renderMarkers();
      if (state.view === 'map') {{
        const openSelected = () => {{
          const marker = markerByLead.get(i);
          if (marker) marker.openTooltip();
        }};
        if (fly) setTimeout(openSelected, 700);
        else requestAnimationFrame(openSelected);
      }}
    }}
    function setView(view) {{
      state.view = view;
      $('dashboardView').classList.toggle('active', view === 'dashboard');
      $('mapView').classList.toggle('active', view === 'map');
      $('dashboardTab').classList.toggle('active', view === 'dashboard');
      $('mapTab').classList.toggle('active', view === 'map');
      if (view === 'map') requestAnimationFrame(() => {{ resize(); renderMarkers(); }});
    }}
    function setStatus(i, value) {{ localStorage.setItem(storeKey(i, 'status'), value); renderDashboard(); renderMapPanel(); }}
    function setCheck(i, c, checked) {{ localStorage.setItem(storeKey(i, `check:${{c}}`), checked ? '1' : '0'); renderDashboard(); renderMapPanel(); }}
    function setNote(i, value) {{ localStorage.setItem(storeKey(i, 'note'), value); }}
    function refreshAll() {{ renderDashboard(); renderMapPanel(); renderMarkers(); }}
    $('dashboardTab').addEventListener('click', () => setView('dashboard'));
    $('mapTab').addEventListener('click', () => setView('map'));
    $('themeToggle').addEventListener('click', () => applyTheme(document.body.dataset.theme === 'dark' ? 'light' : 'dark'));
    $('search').addEventListener('input', e => {{ state.query = e.target.value.toLowerCase(); refreshAll(); }});
    $('fit').addEventListener('change', e => {{ state.fit = e.target.value; refreshAll(); }});
    $('country').addEventListener('change', e => {{ state.country = e.target.value; refreshAll(); }});
    $('statusFilter').addEventListener('change', e => {{ state.status = e.target.value; refreshAll(); }});
    $('qualityFilter').addEventListener('change', e => {{ state.quality = e.target.value; refreshAll(); }});
    $('zoomIn').addEventListener('click', () => map.setZoom(map.getZoom() + 0.5, {{ animate: true }}));
    $('zoomOut').addEventListener('click', () => map.setZoom(map.getZoom() - 0.5, {{ animate: true }}));
    map.on('zoom moveend', updateZoomReadout);
    map.on('zoomend moveend', renderMarkers);
    window.addEventListener('resize', resize);
    applyTheme(localStorage.getItem(themeKey) || 'light');
    renderDashboard();
    renderMapPanel();
    renderMarkers();
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
