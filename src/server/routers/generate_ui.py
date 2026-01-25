from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])

HTML = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>GenAI Desk</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Spline+Sans+Mono:wght@400;600&display=swap");
      :root {
        color-scheme: light;
        --bg: #f2eee8;
        --ink: #2a2520;
        --muted: #6a6156;
        --card: #fffdf9;
        --accent: #e27a52;
        --accent-2: #fff6ee;
        --accent-3: #d9c59b;
        --edge: #e2d7c9;
        --soft: #f6f1e9;
        --highlight: #f3ecdc;
        --shadow: 0 18px 40px rgba(30, 25, 18, 0.12);
        --sidebar-width: 300px;
        --app-gap: 20px;
        --font-display: "Zen Kaku Gothic New", "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
        --font-body: "Zen Kaku Gothic New", "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
        --font-mono: "Spline Sans Mono", "SFMono-Regular", "Consolas", monospace;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: var(--font-body);
        color: var(--ink);
        background:
          radial-gradient(800px 480px at -5% -10%, rgba(224, 204, 187, 0.55) 0%, transparent 60%),
          radial-gradient(900px 520px at 110% 10%, rgba(200, 214, 221, 0.5) 0%, transparent 55%),
          linear-gradient(160deg, #fffaf4 0%, #f2eee6 62%, #ece2d6 100%);
        padding: 32px 20px 180px;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
      }
      body::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image:
          linear-gradient(90deg, rgba(28, 25, 20, 0.04) 1px, transparent 1px),
          linear-gradient(0deg, rgba(28, 25, 20, 0.04) 1px, transparent 1px);
        background-size: 120px 120px;
        opacity: 0.25;
        pointer-events: none;
        z-index: 0;
      }
      body::after {
        content: "";
        position: fixed;
        inset: -10%;
        background-image:
          repeating-linear-gradient(45deg, rgba(28, 25, 20, 0.03) 0 1px, transparent 1px 3px),
          radial-gradient(600px 360px at 75% 20%, rgba(218, 206, 176, 0.28) 0%, transparent 70%);
        opacity: 0.28;
        pointer-events: none;
        z-index: 0;
      }
      .app {
        max-width: 1440px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
        gap: var(--app-gap);
        align-items: start;
        position: relative;
        z-index: 1;
      }
      header {
        grid-column: 1 / -1;
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 16px;
        padding: 6px 4px 8px;
      }
      .title-block {
        display: grid;
        gap: 6px;
      }
      .eyebrow {
        font-size: 11px;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        color: var(--muted);
      }
      h1 {
        margin: 0;
        font-family: var(--font-display);
        font-size: 34px;
        letter-spacing: 0.6px;
      }
      .sub {
        margin: 0;
        color: var(--muted);
        max-width: 520px;
        line-height: 1.6;
      }
      .header-actions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        justify-content: flex-end;
      }
      .header-chip {
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(28, 25, 20, 0.2);
        font-size: 11px;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(6px);
      }
      .panel {
        background: var(--card);
        border: 1px solid var(--edge);
        border-radius: 20px;
        padding: 22px 18px 18px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
      }
      .panel::before,
      .sidebar::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 6px;
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        opacity: 0.9;
      }
      .sidebar {
        background: rgba(255, 253, 247, 0.92);
        border: 1px solid var(--edge);
        border-radius: 22px;
        padding: 24px 16px 16px;
        box-shadow: var(--shadow);
        display: grid;
        gap: 14px;
        position: relative;
        overflow: hidden;
      }
      .sidebar-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
      }
      .sidebar-title {
        display: grid;
        gap: 2px;
      }
      .session-list {
        display: grid;
        gap: 10px;
      }
      .session-item {
        text-align: left;
        padding: 12px 12px 12px 14px;
        border-radius: 14px;
        border: 1px solid var(--edge);
        background: #fff;
        display: grid;
        gap: 6px;
        cursor: pointer;
        transition: transform 160ms ease, box-shadow 160ms ease;
      }
      .session-item:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(21, 18, 14, 0.12);
      }
      .session-item.active {
        border-color: var(--accent);
        box-shadow: 0 0 0 2px rgba(255, 106, 61, 0.25);
      }
      .session-title {
        font-size: 13px;
        color: var(--ink);
        font-weight: 600;
      }
      .session-meta {
        font-size: 11px;
        color: var(--muted);
      }
      .session-delete {
        justify-self: end;
        border-radius: 999px;
        border: 1px solid rgba(28, 25, 20, 0.18);
        background: transparent;
        color: var(--muted);
        font-size: 11px;
        padding: 4px 10px;
        cursor: pointer;
      }
      .session-delete:hover {
        border-color: var(--accent);
        color: var(--accent);
      }
      .main-grid {
        display: flex;
        flex-direction: column;
        gap: 18px;
        animation: rise 520ms ease-out both;
      }
      .output-panel { order: 1; }
      .input-panel {
        order: 2;
        position: sticky;
        bottom: 18px;
        z-index: 2;
      }
      .panel-title {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 12px;
      }
      .panel-title h2 {
        margin: 0;
        font-family: var(--font-display);
        font-size: 18px;
        letter-spacing: 0.3px;
      }
      .panel-note {
        font-size: 11px;
        color: var(--muted);
      }
      textarea {
        width: 100%;
        min-height: 120px;
        max-height: 260px;
        resize: vertical;
        border-radius: 16px;
        border: 1px solid #d7cdbc;
        padding: 14px;
        font-size: 14px;
        font-family: var(--font-mono);
        background: linear-gradient(180deg, #fff, #fdf7ef);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
      }
      textarea:focus {
        outline: 2px solid rgba(255, 106, 61, 0.35);
        border-color: var(--accent);
      }
      .controls {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 12px;
        align-items: center;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid var(--edge);
        font-size: 12px;
        color: var(--muted);
        background: #faf4ea;
      }
      select, button {
        border-radius: 14px;
        border: 1px solid #d7cdbc;
        padding: 10px 16px;
        font-size: 14px;
        font-family: var(--font-body);
      }
      button {
        background: var(--accent);
        color: #fff;
        border: none;
        font-weight: 600;
        letter-spacing: 0.2px;
        cursor: pointer;
        box-shadow: 0 12px 24px rgba(255, 106, 61, 0.25);
        transition: transform 150ms ease, box-shadow 150ms ease;
      }
      button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 28px rgba(255, 106, 61, 0.28);
      }
      button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }
      .ghost,
      .copy,
      .session-delete {
        background: transparent;
        color: var(--ink);
        border: 1px solid rgba(28, 25, 20, 0.2);
        box-shadow: none;
      }
      .ghost:hover,
      .copy:hover,
      .session-delete:hover {
        background: rgba(255, 255, 255, 0.7);
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(28, 25, 20, 0.1);
      }
      .status {
        font-size: 12px;
        color: var(--muted);
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .status.error { color: #b42318; }
      .output-stream {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding-bottom: 180px;
      }
      .output-empty {
        font-size: 13px;
        color: var(--muted);
        padding: 6px 2px 24px;
      }
      .output-message {
        border-radius: 18px;
        border: 1px solid #eadfce;
        padding: 16px;
        background: #fff;
        display: grid;
        gap: 12px;
        position: relative;
        overflow: visible;
        align-self: flex-start;
        max-width: 960px;
      }
      .output-message::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-3), transparent);
        opacity: 0.9;
      }
      .output-header {
        font-size: 12px;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .message-actions {
        display: inline-flex;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
      }
      .user-message {
        align-self: flex-end;
        max-width: 780px;
        padding: 14px 16px;
        border-radius: 18px 18px 6px 18px;
        background: #2f2a24;
        color: #fff;
        box-shadow: 0 16px 30px rgba(28, 25, 20, 0.2);
        border: 1px solid rgba(28, 25, 20, 0.2);
        display: grid;
        gap: 8px;
        white-space: pre-wrap;
      }
      .user-meta {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.24em;
        opacity: 0.75;
      }
      .tab-content {
        border-radius: 14px;
        border: 1px solid #eadfce;
        padding: 14px;
        background: linear-gradient(160deg, #fff7ef 0%, #f6efe3 100%);
        white-space: pre-wrap;
        min-height: 180px;
        line-height: 1.7;
      }
      .diff-highlight {
        background: #f6e6c8;
        border-radius: 6px;
        padding: 0 4px;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
      }
      .reasoning-details {
        border-radius: 12px;
        border: 1px solid #eadfce;
        padding: 10px 12px;
        background: #fffaf2;
      }
      .reasoning-details summary {
        cursor: pointer;
        font-size: 12px;
        color: var(--muted);
      }
      .reasoning-body {
        margin-top: 8px;
        font-size: 13px;
        color: var(--ink);
        white-space: pre-wrap;
        line-height: 1.6;
      }
      .edit-toggle {
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(28, 25, 20, 0.2);
        background: rgba(255, 255, 255, 0.7);
        font-size: 12px;
        color: var(--ink);
        cursor: pointer;
        box-shadow: none;
        font-weight: 600;
      }
      .edit-panel {
        border-radius: 14px;
        border: 1px dashed #eadfce;
        padding: 12px;
        background: #fffaf2;
        display: grid;
        gap: 10px;
      }
      .edit-panel.hidden { display: none; }
      .edit-panel textarea {
        min-height: 80px;
      }
      .edit-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
      }
      @keyframes rise {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @media (max-width: 1080px) {
        .app {
          grid-template-columns: 1fr;
        }
        .sidebar {
          order: 2;
        }
      }
    </style>
  </head>
  <body>
    <div class=\"app\">
      <header>
        <div class=\"title-block\">
          <div class=\"eyebrow\">Generative AI Workspace</div>
          <h1>GenAI Desk</h1>
          <p class=\"sub\">A lightweight UI for prompting, reviewing outputs, and keeping local sessions.</p>
        </div>
        <div class=\"header-actions\">
          <div class=\"header-chip\" id=\"statusChip\">idle</div>
        </div>
      </header>

      <aside class=\"sidebar\">
        <div class=\"sidebar-header\">
          <div class=\"sidebar-title\">
            <div class=\"eyebrow\">Sessions</div>
            <h2>History</h2>
          </div>
          <button id=\"newSession\" class=\"ghost\" type=\"button\">New</button>
        </div>
        <div class=\"session-list\" id=\"sessionList\"></div>
      </aside>

      <section class=\"main-grid\">
        <div class=\"panel input-panel\">
          <div class=\"panel-title\">
            <h2>Input</h2>
            <div class=\"panel-note\">Ctrl/Cmd + Enter to run</div>
          </div>
          <div class=\"controls\">
            <textarea id=\"composerInput\" placeholder=\"Describe your task or paste a prompt...\"></textarea>
            <div style=\"display:grid; gap:10px; justify-items:start;\">
              <button id=\"generateBtn\" type=\"button\">Generate</button>
              <div class=\"status\" id=\"statusText\"></div>
            </div>
          </div>
        </div>
        <div class=\"panel output-panel\">
          <div class=\"panel-title\">
            <h2>Output</h2>
            <div class=\"panel-note\">Latest results appear at the bottom.</div>
          </div>
          <div class=\"output-stream\" id=\"outputStream\">
            <div class=\"output-empty\" id=\"outputEmpty\">No outputs yet. Run a generation to start.</div>
          </div>
        </div>
      </section>
    </div>

    <script>
      const STORAGE_KEY = "genai_sessions_v1";
      const sessionListEl = document.getElementById("sessionList");
      const newSessionBtn = document.getElementById("newSession");
      const composerInputEl = document.getElementById("composerInput");
      const generateBtn = document.getElementById("generateBtn");
      const statusTextEl = document.getElementById("statusText");
      const statusChipEl = document.getElementById("statusChip");
      const outputStreamEl = document.getElementById("outputStream");
      const outputEmptyEl = document.getElementById("outputEmpty");
      let sessions = [];
      let activeSessionId = null;
      let loading = false;

      function makeId() {
        if (window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID();
        return `id_${Date.now()}_${Math.random().toString(16).slice(2)}`;
      }

      function loadSessions() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          sessions = raw ? JSON.parse(raw) : [];
        } catch {
          sessions = [];
        }
      }

      function saveSessions() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
      }

      function ensureSessions() {
        loadSessions();
        if (!sessions.length) {
          const session = {
            id: makeId(),
            title: "New session",
            input_text: "",
            output_stream: [],
            revision_history: []
          };
          sessions = [session];
        }
        activeSessionId = sessions[0].id;
        saveSessions();
      }

      function getActiveSession() {
        return sessions.find((s) => s.id === activeSessionId) || sessions[0];
      }

      function setStatus(message, isError = false) {
        statusTextEl.textContent = message || "";
        statusTextEl.classList.toggle("error", isError);
        statusChipEl.textContent = isError ? "error" : (message ? "busy" : "idle");
      }

      function setLoading(value) {
        loading = value;
        generateBtn.disabled = value;
      }


      function formatTime(value) {
        if (!value) return "";
        const parsed = new Date(value);
        if (Number.isNaN(parsed.getTime())) return value;
        return parsed.toLocaleTimeString();
      }

      function renderSessionList() {
        sessionListEl.innerHTML = "";
        sessions.forEach((session) => {
          const item = document.createElement("div");
          item.className = "session-item" + (session.id === activeSessionId ? " active" : "");
          const title = document.createElement("div");
          title.className = "session-title";
          title.textContent = session.title || "New session";
          const meta = document.createElement("div");
          meta.className = "session-meta";
          const lastAt = (session.output_stream || []).slice(-1)[0]?.at;
          meta.textContent = lastAt ? `Last: ${formatTime(lastAt)}` : "No activity";
          const del = document.createElement("button");
          del.type = "button";
          del.className = "session-delete";
          del.textContent = "Delete";
          del.addEventListener("click", (event) => {
            event.stopPropagation();
            deleteSession(session.id);
          });
          item.appendChild(title);
          item.appendChild(meta);
          item.appendChild(del);
          item.addEventListener("click", () => {
            activeSessionId = session.id;
            renderSessionList();
            renderSession();
          });
          sessionListEl.appendChild(item);
        });
      }

      function deleteSession(id) {
        sessions = sessions.filter((s) => s.id !== id);
        if (!sessions.length) {
          ensureSessions();
        }
        if (!sessions.find((s) => s.id === activeSessionId)) {
          activeSessionId = sessions[0].id;
        }
        saveSessions();
        renderSessionList();
        renderSession();
      }

      function createNewSession() {
        const session = {
          id: makeId(),
          title: "New session",
          input_text: "",
          output_stream: [],
          revision_history: []
        };
        sessions.unshift(session);
        activeSessionId = session.id;
        saveSessions();
        renderSessionList();
        renderSession();
      }

      function escapeHtml(text) {
        return text
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/\"/g, "&quot;")
          .replace(/'/g, "&#39;");
      }

      function applyDiffs(text, diffs) {
        if (!diffs || !diffs.length) return escapeHtml(text || "");
        const sorted = [...diffs].sort((a, b) => a.start - b.start);
        let result = "";
        let last = 0;
        sorted.forEach((diff) => {
          const start = Math.max(0, diff.start || 0);
          const end = Math.max(start, diff.end || start);
          result += escapeHtml(text.slice(last, start));
          const segment = escapeHtml(text.slice(start, end));
          const before = escapeHtml(diff.before || "");
          const after = escapeHtml(diff.after || "");
          const title = `Before: ${before}\nAfter: ${after}`;
          result += `<mark class=\"diff-highlight\" title=\"${title}\">${segment || ""}</mark>`;
          last = end;
        });
        result += escapeHtml(text.slice(last));
        return result;
      }


      function appendUserMessage(text, timestamp) {
        const message = document.createElement("div");
        message.className = "user-message";
        const meta = document.createElement("div");
        meta.className = "user-meta";
        meta.textContent = `Input - ${formatTime(timestamp)}`;
        const body = document.createElement("div");
        body.textContent = text;
        message.appendChild(meta);
        message.appendChild(body);
        outputStreamEl.appendChild(message);
      }

      function createEditPanel(getBaseText, sourceText, onSubmit) {
        const panel = document.createElement("div");
        panel.className = "edit-panel hidden";

        const textarea = document.createElement("textarea");
        textarea.placeholder = "Add a revision instruction...";

        const actions = document.createElement("div");
        actions.className = "edit-actions";
        const submit = document.createElement("button");
        submit.type = "button";
        submit.textContent = "Revise";
        submit.addEventListener("click", async () => {
          const instruction = textarea.value.trim();
          const baseText = getBaseText();
          const ok = await onSubmit({ instruction, baseText, sourceText });
          if (ok) {
            textarea.value = "";
            panel.classList.add("hidden");
          }
        });
        const cancel = document.createElement("button");
        cancel.type = "button";
        cancel.className = "ghost";
        cancel.textContent = "Cancel";
        cancel.addEventListener("click", () => {
          panel.classList.add("hidden");
        });

        actions.appendChild(submit);
        actions.appendChild(cancel);
        panel.appendChild(textarea);
        panel.appendChild(actions);
        return panel;
      }

      function appendOutputCard(entry) {
        const message = document.createElement("div");
        message.className = "output-message";

        const header = document.createElement("div");
        header.className = "output-header";
        header.textContent = `${entry.label} - ${formatTime(entry.at)}`;

        const actions = document.createElement("div");
        actions.className = "message-actions";

        const copyBtn = document.createElement("button");
        copyBtn.className = "copy ghost";
        copyBtn.type = "button";
        copyBtn.textContent = "Copy";
        copyBtn.addEventListener("click", async () => {
          try {
            await navigator.clipboard.writeText(entry.text || "");
            setStatus("Copied.");
          } catch {
            setStatus("Copy failed.", true);
          }
        });

        const editToggle = document.createElement("button");
        editToggle.type = "button";
        editToggle.className = "edit-toggle";
        editToggle.textContent = "Revise";

        const body = document.createElement("div");
        body.className = "tab-content";
        if (entry.diffs && entry.diffs.length) {
          body.innerHTML = applyDiffs(entry.text || "", entry.diffs);
        } else {
          body.textContent = entry.text || "";
        }

        const reasoningDetails = document.createElement("details");
        reasoningDetails.className = "reasoning-details";
        const summary = document.createElement("summary");
        summary.textContent = "Reasoning";
        const reasoningBody = document.createElement("div");
        reasoningBody.className = "reasoning-body";
        reasoningBody.textContent = entry.reasoning || "No reasoning provided.";
        reasoningDetails.appendChild(summary);
        reasoningDetails.appendChild(reasoningBody);

        const editPanel = createEditPanel(
          () => entry.text || "",
          entry.source || "",
          runRevision
        );

        editToggle.addEventListener("click", () => {
          editPanel.classList.toggle("hidden");
          if (!editPanel.classList.contains("hidden")) {
            const input = editPanel.querySelector("textarea");
            if (input) input.focus();
          }
        });

        actions.appendChild(copyBtn);
        actions.appendChild(editToggle);
        header.appendChild(actions);

        message.appendChild(header);
        message.appendChild(body);
        message.appendChild(reasoningDetails);
        message.appendChild(editPanel);
        outputStreamEl.appendChild(message);
      }

      function renderSession() {
        const session = getActiveSession();
        if (!session) return;
        outputStreamEl.innerHTML = "";
        const stream = session.output_stream || [];
        if (!stream.length) {
          outputStreamEl.appendChild(outputEmptyEl);
        }
        stream.forEach((entry) => {
          if (entry.kind === "user") {
            appendUserMessage(entry.text, entry.at);
          } else if (entry.kind === "generate" || entry.kind === "revision") {
            appendOutputCard(entry);
          }
        });
        composerInputEl.value = session.input_text || "";
      }

      function scrollToLatest() {
        window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
      }

      async function runGenerate() {
        const text = composerInputEl.value.trim();
        if (!text) {
          setStatus("Enter some input.", true);
          return;
        }

        setStatus("");
        setLoading(true);
        try {
          const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
          });

          if (!response.ok) {
            const detail = await response.text();
            throw new Error(detail || "Request failed");
          }

          const data = await response.json();
          const session = getActiveSession();
          if (!session) return;

          const now = new Date().toISOString();
          const label = (session.output_stream || []).filter((item) => item.kind === "generate").length
            ? `Generate ${((session.output_stream || []).filter((item) => item.kind === "generate").length + 1)}`
            : "Generate";

          session.output_stream = session.output_stream || [];
          session.output_stream.push({ kind: "user", text, at: now });
          session.output_stream.push({
            kind: "generate",
            label,
            at: now,
            text: data.text,
            reasoning: data.reasoning || "",
            source: text
          });
          session.input_text = text;

          if (!session.title || session.title === "New session") {
            const trimmed = text.replace(/\s+/g, " ").trim();
            session.title = trimmed ? trimmed.slice(0, 20) : "New session";
          }

          saveSessions();
          renderSessionList();
          renderSession();
          scrollToLatest();
        } catch (error) {
          setStatus(error.message || "Request failed", true);
        } finally {
          setLoading(false);
        }
      }

      async function runRevision({ instruction, baseText, sourceText }) {
        if (!instruction) {
          setStatus("Enter a revision instruction.", true);
          return false;
        }
        if (!baseText) {
          setStatus("No base output to revise.", true);
          return false;
        }
        if (!sourceText) {
          setStatus("No source input found.", true);
          return false;
        }

        const session = getActiveSession();
        if (!session) return false;
        const history = Array.isArray(session.revision_history) ? session.revision_history : [];

        setStatus("");
        setLoading(true);
        try {
          const response = await fetch("/generate/revise", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text: sourceText,
              instruction,
              base: baseText,
              history
            })
          });

          if (!response.ok) {
            const detail = await response.text();
            throw new Error(detail || "Request failed");
          }

          const data = await response.json();
          const now = new Date().toISOString();
          const revisionCount = (session.output_stream || []).filter((item) => item.kind === "revision").length;
          const label = `Revision ${revisionCount + 1}`;

          session.output_stream = session.output_stream || [];
          session.output_stream.push({
            kind: "revision",
            label,
            at: now,
            text: data.text,
            reasoning: data.reasoning || "",
            diffs: Array.isArray(data.diffs) ? data.diffs : [],
            source: sourceText
          });
          session.revision_history = [...history, instruction].slice(-10);

          saveSessions();
          renderSessionList();
          renderSession();
          scrollToLatest();
          return true;
        } catch (error) {
          setStatus(error.message || "Request failed", true);
          return false;
        } finally {
          setLoading(false);
        }
      }

      function bindShortcuts() {
        composerInputEl.addEventListener("keydown", (event) => {
          if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            event.preventDefault();
            runGenerate();
          }
        });
      }


      ensureSessions();
      bindShortcuts();
      renderSessionList();
      renderSession();

      newSessionBtn.addEventListener("click", createNewSession);
      generateBtn.addEventListener("click", runGenerate);
    </script>
  </body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def generate_page() -> HTMLResponse:
    return HTMLResponse(HTML)
