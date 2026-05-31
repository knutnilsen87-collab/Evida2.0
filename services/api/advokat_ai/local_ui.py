from __future__ import annotations


def render_local_ui() -> str:
    return """<!doctype html>
<html lang="no">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evida2.0</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7f3;
      --panel: #ffffff;
      --panel-soft: #eef4f0;
      --text: #18211d;
      --muted: #66736d;
      --line: #d9e1dc;
      --brand: #0f6b58;
      --brand-dark: #084637;
      --accent: #b35a28;
      --danger: #b42318;
      --ok: #16864b;
      --shadow: 0 18px 45px rgba(24, 33, 29, 0.1);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    button, input, textarea, select {
      font: inherit;
    }

    button {
      min-height: 40px;
      border: 0;
      border-radius: 6px;
      background: var(--brand);
      color: white;
      padding: 0 14px;
      cursor: pointer;
      font-weight: 700;
    }

    button.secondary {
      background: #e7ede9;
      color: var(--brand-dark);
      border: 1px solid var(--line);
    }

    button:disabled {
      cursor: not-allowed;
      opacity: 0.55;
    }

    input, textarea, select {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px 12px;
      background: white;
      color: var(--text);
    }

    textarea { min-height: 84px; resize: vertical; }

    label {
      display: grid;
      gap: 6px;
      font-size: 13px;
      font-weight: 700;
      color: #34443c;
    }

    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }

    .topbar {
      background: #18211d;
      color: white;
      border-bottom: 1px solid rgba(255,255,255,0.12);
    }

    .topbar-inner {
      width: min(1440px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }

    .mark {
      width: 36px;
      height: 36px;
      border-radius: 7px;
      background: #eef4f0;
      color: var(--brand-dark);
      display: grid;
      place-items: center;
      font-weight: 900;
    }

    .brand h1 {
      margin: 0;
      font-size: 20px;
      line-height: 1.1;
      letter-spacing: 0;
    }

    .brand p {
      margin: 2px 0 0;
      color: #cbd8d1;
      font-size: 13px;
    }

    .status-strip {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      min-height: 30px;
      padding: 0 10px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.18);
      color: #f6faf7;
      font-size: 13px;
      white-space: nowrap;
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: #f0b429;
    }

    .dot.ok { background: #49d17d; }
    .dot.bad { background: #ff7b72; }

    main {
      width: min(1440px, calc(100% - 32px));
      margin: 0 auto;
      padding: 24px 0 32px;
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr) 360px;
      gap: 18px;
      align-items: start;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .panel-header {
      min-height: 52px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }

    .panel-header h2 {
      margin: 0;
      font-size: 16px;
      letter-spacing: 0;
    }

    .panel-body {
      padding: 16px;
      display: grid;
      gap: 14px;
    }

    .case-list {
      display: grid;
      gap: 8px;
    }

    .case-row {
      width: 100%;
      text-align: left;
      border: 1px solid var(--line);
      background: white;
      color: var(--text);
      border-radius: 6px;
      padding: 11px 12px;
      display: grid;
      gap: 3px;
    }

    .case-row.active {
      border-color: var(--brand);
      background: #edf7f2;
    }

    .case-row strong {
      display: block;
      overflow-wrap: anywhere;
    }

    .case-row span, .meta {
      color: var(--muted);
      font-size: 13px;
    }

    .workspace {
      display: grid;
      gap: 18px;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }

    .metric {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 13px;
      background: var(--panel-soft);
    }

    .metric strong {
      display: block;
      font-size: 24px;
      line-height: 1.1;
    }

    .metric span {
      color: var(--muted);
      font-size: 13px;
    }

    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tab {
      background: #edf1ee;
      color: var(--brand-dark);
      border: 1px solid var(--line);
    }

    .tab.active {
      background: var(--brand-dark);
      color: white;
    }

    .table {
      display: grid;
      border: 1px solid var(--line);
      border-radius: 6px;
      overflow: hidden;
    }

    .table-row {
      display: grid;
      grid-template-columns: minmax(0, 1.4fr) minmax(0, 0.8fr) minmax(0, 0.7fr);
      gap: 10px;
      padding: 11px 12px;
      border-bottom: 1px solid var(--line);
      align-items: center;
    }

    .table-row:last-child { border-bottom: 0; }
    .table-head { background: #f0f4f1; font-weight: 800; }

    .source-status {
      display: inline-flex;
      width: fit-content;
      border-radius: 999px;
      padding: 4px 8px;
      background: #fff3cd;
      color: #6f4e00;
      font-size: 12px;
      font-weight: 800;
    }

    .source-status.documented {
      background: #dff6e7;
      color: #0d6835;
    }

    .assistant {
      position: sticky;
      top: 18px;
    }

    .assistant-note {
      background: #fff8ef;
      border: 1px solid #f2d2ad;
      border-radius: 6px;
      padding: 13px;
      line-height: 1.45;
    }

    .actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .empty {
      border: 1px dashed #bac7c0;
      border-radius: 6px;
      padding: 18px;
      color: var(--muted);
      background: #fbfdfb;
    }

    .message {
      min-height: 20px;
      color: var(--muted);
      font-size: 13px;
    }

    .message.error { color: var(--danger); }
    .message.ok { color: var(--ok); }

    .fine-links {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      font-size: 13px;
    }

    .fine-links a {
      color: var(--brand-dark);
      font-weight: 800;
      text-decoration: none;
    }

    @media (max-width: 1120px) {
      main {
        grid-template-columns: 280px minmax(0, 1fr);
      }

      .assistant {
        grid-column: 1 / -1;
        position: static;
      }
    }

    @media (max-width: 760px) {
      .topbar-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 14px 0;
      }

      .status-strip {
        justify-content: flex-start;
      }

      main {
        width: min(100% - 20px, 720px);
        grid-template-columns: 1fr;
        padding-top: 12px;
      }

      .summary-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .table-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <div class="mark">E</div>
          <div>
            <h1>Evida2.0</h1>
            <p>Kontrollert juridisk saksarbeid</p>
          </div>
        </div>
        <div class="status-strip">
          <div class="pill"><span id="api-dot" class="dot"></span><span id="api-status">Kobler til API</span></div>
          <div class="pill"><span id="user-status">Laster bruker</span></div>
        </div>
      </div>
    </header>

    <main>
      <section class="panel">
        <div class="panel-header">
          <h2>Saker</h2>
          <button id="refresh-cases" class="secondary" type="button">Oppdater</button>
        </div>
        <div class="panel-body">
          <div class="case-list" id="case-list"></div>
          <form id="case-form" class="panel-body" style="padding:0">
            <label>Saksnavn
              <input id="case-title" required value="Ny Evida2.0-sak">
            </label>
            <label>Beskrivelse
              <textarea id="case-description">Opprettet fra lokal Evida2.0 UI.</textarea>
            </label>
            <button type="submit">Opprett sak</button>
            <div id="case-message" class="message"></div>
          </form>
        </div>
      </section>

      <section class="workspace">
        <section class="panel">
          <div class="panel-header">
            <h2 id="case-heading">Velg en sak</h2>
            <div class="fine-links">
              <a href="/docs" target="_blank" rel="noreferrer">API-dokumentasjon</a>
              <a href="/openapi.json" target="_blank" rel="noreferrer">OpenAPI</a>
            </div>
          </div>
          <div class="panel-body">
            <div class="summary-grid">
              <div class="metric"><strong id="metric-docs">0</strong><span>Dokumenter</span></div>
              <div class="metric"><strong id="metric-facts">0</strong><span>Fakta</span></div>
              <div class="metric"><strong id="metric-missing">0</strong><span>Mangler kilde</span></div>
              <div class="metric"><strong id="metric-next">-</strong><span>Neste steg</span></div>
            </div>
            <div class="tabs">
              <button id="tab-docs" class="tab active" type="button">Dokumenter</button>
              <button id="tab-facts" class="tab" type="button">Fakta</button>
            </div>
            <div id="content"></div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-header">
            <h2>Legg inn dokument</h2>
          </div>
          <form id="document-form" class="panel-body">
            <label>Filnavn
              <input id="doc-filename" value="grunnlag.pdf" required>
            </label>
            <label>Tekst for lokal test
              <textarea id="doc-text">Dette er et lokalt testdokument for Evida2.0.</textarea>
            </label>
            <button type="submit">Registrer dokument</button>
            <div id="document-message" class="message"></div>
          </form>
        </section>

        <section class="panel">
          <div class="panel-header">
            <h2>Legg inn faktum</h2>
          </div>
          <form id="fact-form" class="panel-body">
            <label>Faktatekst
              <textarea id="fact-text">Saken har et dokumentert grunnlag.</textarea>
            </label>
            <label>Kilde
              <select id="fact-source"></select>
            </label>
            <button type="submit">Opprett faktum</button>
            <div id="fact-message" class="message"></div>
          </form>
        </section>
      </section>

      <aside class="panel assistant">
        <div class="panel-header">
          <h2>Assistent</h2>
        </div>
        <div class="panel-body">
          <div class="assistant-note" id="assistant-note">
            Velg en sak for aa se neste trygge steg.
          </div>
          <div class="actions">
            <button id="ask-next" type="button">Hva gjor jeg naa?</button>
            <button id="reset-dev" class="secondary" type="button">Nullstill demo</button>
          </div>
          <div id="assistant-message" class="message"></div>
        </div>
      </aside>
    </main>
  </div>

  <script>
    const ownerId = "00000000-0000-0000-0000-000000000001";
    let cases = [];
    let selectedCaseId = null;
    let selectedTab = "documents";
    let documents = [];
    let facts = [];
    let sourceRefs = [];

    const els = {
      apiDot: document.getElementById("api-dot"),
      apiStatus: document.getElementById("api-status"),
      userStatus: document.getElementById("user-status"),
      caseList: document.getElementById("case-list"),
      caseForm: document.getElementById("case-form"),
      caseTitle: document.getElementById("case-title"),
      caseDescription: document.getElementById("case-description"),
      caseMessage: document.getElementById("case-message"),
      caseHeading: document.getElementById("case-heading"),
      metricDocs: document.getElementById("metric-docs"),
      metricFacts: document.getElementById("metric-facts"),
      metricMissing: document.getElementById("metric-missing"),
      metricNext: document.getElementById("metric-next"),
      content: document.getElementById("content"),
      tabDocs: document.getElementById("tab-docs"),
      tabFacts: document.getElementById("tab-facts"),
      documentForm: document.getElementById("document-form"),
      docFilename: document.getElementById("doc-filename"),
      docText: document.getElementById("doc-text"),
      documentMessage: document.getElementById("document-message"),
      factForm: document.getElementById("fact-form"),
      factText: document.getElementById("fact-text"),
      factSource: document.getElementById("fact-source"),
      factMessage: document.getElementById("fact-message"),
      assistantNote: document.getElementById("assistant-note"),
      assistantMessage: document.getElementById("assistant-message"),
      askNext: document.getElementById("ask-next"),
      resetDev: document.getElementById("reset-dev"),
      refreshCases: document.getElementById("refresh-cases")
    };

    async function api(path, options = {}) {
      const headers = {
        "Content-Type": "application/json",
        "x-user-id": ownerId,
        ...(options.headers || {})
      };
      const response = await fetch(path, { ...options, headers });
      const text = await response.text();
      let data = null;
      try { data = text ? JSON.parse(text) : null; } catch { data = text; }
      if (!response.ok) {
        const detail = data && data.detail ? data.detail : response.statusText;
        throw new Error(detail || `HTTP ${response.status}`);
      }
      return data;
    }

    function setMessage(el, text, type = "") {
      el.textContent = text;
      el.className = `message ${type}`;
    }

    async function checkHealth() {
      try {
        await api("/api/health", { headers: {} });
        els.apiDot.className = "dot ok";
        els.apiStatus.textContent = "API klar";
      } catch (error) {
        els.apiDot.className = "dot bad";
        els.apiStatus.textContent = "API ikke klar";
      }
    }

    async function loadUser() {
      try {
        const user = await api("/v1/me");
        els.userStatus.textContent = `${user.name || "Bruker"} - ${user.role || "rolle"}`;
      } catch (error) {
        els.userStatus.textContent = "Bruker ikke klar";
      }
    }

    async function loadCases(selectFirst = true) {
      cases = await api("/v1/cases");
      if (!selectedCaseId && selectFirst && cases.length) {
        selectedCaseId = cases[0].id;
      }
      renderCases();
      await loadSelectedCase();
    }

    function renderCases() {
      if (!cases.length) {
        els.caseList.innerHTML = '<div class="empty">Ingen saker enda.</div>';
        return;
      }
      els.caseList.innerHTML = cases.map(item => `
        <button type="button" class="case-row ${item.id === selectedCaseId ? "active" : ""}" data-case-id="${item.id}">
          <strong>${escapeHtml(item.title)}</strong>
          <span>${escapeHtml(item.status || "aktiv")} - ${escapeHtml(item.jurisdiction || "NO")}</span>
        </button>
      `).join("");
      document.querySelectorAll("[data-case-id]").forEach(button => {
        button.addEventListener("click", async () => {
          selectedCaseId = button.dataset.caseId;
          renderCases();
          await loadSelectedCase();
        });
      });
    }

    async function loadSelectedCase() {
      if (!selectedCaseId) {
        els.caseHeading.textContent = "Velg en sak";
        els.content.innerHTML = '<div class="empty">Opprett eller velg en sak for aa arbeide videre.</div>';
        return;
      }

      const selected = await api(`/v1/cases/${selectedCaseId}`);
      documents = await api(`/v1/cases/${selectedCaseId}/documents`);
      facts = await api(`/v1/cases/${selectedCaseId}/facts`);
      els.caseHeading.textContent = selected.title;
      els.metricDocs.textContent = documents.length;
      els.metricFacts.textContent = facts.length;
      els.metricMissing.textContent = facts.filter(fact => fact.source_status !== "documented").length;
      els.metricNext.textContent = selected.overview && selected.overview.next_action ? "1" : "-";
      els.assistantNote.textContent = selected.overview && selected.overview.next_action
        ? selected.overview.next_action
        : "Saken er klar for videre arbeid.";
      renderFactSourceOptions();
      renderContent();
    }

    function renderContent() {
      els.tabDocs.classList.toggle("active", selectedTab === "documents");
      els.tabFacts.classList.toggle("active", selectedTab === "facts");
      if (selectedTab === "documents") {
        renderDocuments();
      } else {
        renderFacts();
      }
    }

    function renderDocuments() {
      if (!documents.length) {
        els.content.innerHTML = '<div class="empty">Ingen dokumenter er registrert i saken.</div>';
        return;
      }
      els.content.innerHTML = `
        <div class="table">
          <div class="table-row table-head"><div>Dokument</div><div>Status</div><div>Storrelse</div></div>
          ${documents.map(doc => `
            <div class="table-row">
              <div>${escapeHtml(doc.filename)}</div>
              <div><span class="source-status documented">${escapeHtml(doc.user_status || doc.status)}</span></div>
              <div class="meta">${Number(doc.size_bytes || 0)} bytes</div>
            </div>
          `).join("")}
        </div>`;
    }

    function renderFacts() {
      if (!facts.length) {
        els.content.innerHTML = '<div class="empty">Ingen fakta er registrert i saken.</div>';
        return;
      }
      els.content.innerHTML = `
        <div class="table">
          <div class="table-row table-head"><div>Faktum</div><div>Kildestatus</div><div>Opprettet</div></div>
          ${facts.map(fact => `
            <div class="table-row">
              <div>${escapeHtml(fact.text)}</div>
              <div><span class="source-status ${fact.source_status === "documented" ? "documented" : ""}">${escapeHtml(fact.user_status || fact.source_status)}</span></div>
              <div class="meta">${escapeHtml((fact.created_at || "").slice(0, 10))}</div>
            </div>
          `).join("")}
        </div>`;
    }

    function renderFactSourceOptions() {
      if (!documents.length) {
        els.factSource.innerHTML = '<option value="">Ingen dokumentkilde</option>';
        return;
      }
      els.factSource.innerHTML = '<option value="">Opprett uten kilde</option>' + documents.map(doc => (
        `<option value="${doc.id}">${escapeHtml(doc.filename)}</option>`
      )).join("");
    }

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    els.caseForm.addEventListener("submit", async event => {
      event.preventDefault();
      setMessage(els.caseMessage, "Oppretter sak...");
      try {
        const created = await api("/v1/cases", {
          method: "POST",
          body: JSON.stringify({
            title: els.caseTitle.value,
            description: els.caseDescription.value,
            case_type: "civil",
            jurisdiction: "NO"
          })
        });
        selectedCaseId = created.id;
        setMessage(els.caseMessage, "Sak opprettet.", "ok");
        await loadCases(false);
      } catch (error) {
        setMessage(els.caseMessage, error.message, "error");
      }
    });

    els.documentForm.addEventListener("submit", async event => {
      event.preventDefault();
      if (!selectedCaseId) {
        setMessage(els.documentMessage, "Velg en sak forst.", "error");
        return;
      }
      setMessage(els.documentMessage, "Registrerer dokument...");
      try {
        const init = await api(`/v1/cases/${selectedCaseId}/documents:init-upload`, {
          method: "POST",
          body: JSON.stringify({
            filename: els.docFilename.value,
            mime_type: "application/pdf",
            size_bytes: new Blob([els.docText.value]).size
          })
        });
        await api(`/v1/cases/${selectedCaseId}/documents:complete-upload`, {
          method: "POST",
          body: JSON.stringify({
            upload_token: init.upload_token,
            text: els.docText.value
          })
        });
        selectedTab = "documents";
        setMessage(els.documentMessage, "Dokument registrert.", "ok");
        await loadSelectedCase();
      } catch (error) {
        setMessage(els.documentMessage, error.message, "error");
      }
    });

    els.factForm.addEventListener("submit", async event => {
      event.preventDefault();
      if (!selectedCaseId) {
        setMessage(els.factMessage, "Velg en sak forst.", "error");
        return;
      }
      setMessage(els.factMessage, "Oppretter faktum...");
      try {
        let sourceIds = [];
        if (els.factSource.value) {
          const source = await api(`/v1/cases/${selectedCaseId}/source-refs`, {
            method: "POST",
            body: JSON.stringify({
              document_id: els.factSource.value,
              bates_label: "EVIDA-LOCAL-0001",
              confidence: 0.98
            })
          });
          sourceIds = [source.id];
        }
        await api(`/v1/cases/${selectedCaseId}/facts`, {
          method: "POST",
          body: JSON.stringify({
            text: els.factText.value,
            source_ref_ids: sourceIds
          })
        });
        selectedTab = "facts";
        setMessage(els.factMessage, "Faktum opprettet.", "ok");
        await loadSelectedCase();
      } catch (error) {
        setMessage(els.factMessage, error.message, "error");
      }
    });

    els.tabDocs.addEventListener("click", () => {
      selectedTab = "documents";
      renderContent();
    });

    els.tabFacts.addEventListener("click", () => {
      selectedTab = "facts";
      renderContent();
    });

    els.refreshCases.addEventListener("click", () => loadCases(false));

    els.askNext.addEventListener("click", async () => {
      if (!selectedCaseId) {
        setMessage(els.assistantMessage, "Velg en sak forst.", "error");
        return;
      }
      setMessage(els.assistantMessage, "Spurter assistenten...");
      try {
        const response = await api("/v1/assistant/chat", {
          method: "POST",
          body: JSON.stringify({
            case_id: selectedCaseId,
            message: "Hva gjor jeg naa?",
            preferred_answer_level: "simple"
          })
        });
        els.assistantNote.textContent = response.answer;
        setMessage(els.assistantMessage, response.next_best_action ? response.next_best_action.label : "Svar mottatt.", "ok");
      } catch (error) {
        setMessage(els.assistantMessage, error.message, "error");
      }
    });

    els.resetDev.addEventListener("click", async () => {
      setMessage(els.assistantMessage, "Nullstiller demo...");
      try {
        await api("/api/dev/reset", { method: "POST" });
        selectedCaseId = null;
        await loadCases(true);
        setMessage(els.assistantMessage, "Demo nullstilt.", "ok");
      } catch (error) {
        setMessage(els.assistantMessage, error.message, "error");
      }
    });

    async function boot() {
      await checkHealth();
      await loadUser();
      try {
        await loadCases(true);
      } catch (error) {
        els.content.innerHTML = `<div class="empty">Kunne ikke laste saker: ${escapeHtml(error.message)}</div>`;
      }
    }

    boot();
  </script>
</body>
</html>"""
