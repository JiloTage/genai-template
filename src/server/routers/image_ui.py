from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["image-ui"])

HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Image Studio</title>
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
      .session-item.static { cursor: default; }
      .session-item.static:hover {
        transform: none;
        box-shadow: none;
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
      .field-stack {
        display: grid;
        gap: 14px;
      }
      .field {
        display: grid;
        gap: 6px;
      }
      .field-label {
        font-size: 12px;
        font-weight: 600;
        color: var(--ink);
      }
      .field-hint {
        font-size: 11px;
        color: var(--muted);
      }
      input[type="file"] {
        width: 100%;
        font-size: 12px;
        border-radius: 14px;
        border: 1px solid #d7cdbc;
        padding: 10px 12px;
        background: #fff;
        font-family: var(--font-body);
      }
      .payload-details {
        border-radius: 12px;
        border: 1px solid #eadfce;
        padding: 10px 12px;
        background: #fffaf2;
        display: grid;
        gap: 10px;
      }
      .payload-details summary {
        cursor: pointer;
        font-size: 12px;
        color: var(--muted);
      }
      .payload-details textarea {
        min-height: 80px;
      }
      .payload {
        border-radius: 12px;
        border: 1px solid #eadfce;
        padding: 10px;
        background: #fffaf2;
        font-family: var(--font-mono);
        font-size: 12px;
        white-space: pre-wrap;
      }
      .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
      }
      .image-grid img {
        width: 100%;
        border-radius: 14px;
        border: 1px solid #eadfce;
        display: block;
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
    <div class="app">
      <header>
        <div class="title-block">
          <div class="eyebrow">Generative AI Workspace</div>
          <h1>Image Studio</h1>
          <p class="sub">Upload images or provide URLs, then send an edit prompt to nano-banana.</p>
        </div>
        <div class="header-actions">
          <div class="header-chip" id="statusChip">idle</div>
        </div>
      </header>

      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="sidebar-title">
            <div class="eyebrow">Image Flow</div>
            <h2>Checklist</h2>
          </div>
        </div>
        <div class="session-list">
          <div class="session-item static">
            <div class="session-title">Prompt first</div>
            <div class="session-meta">Describe the edit, style, or transformation.</div>
          </div>
          <div class="session-item static">
            <div class="session-title">Provide images</div>
            <div class="session-meta">Paste URLs or upload files to use as input.</div>
          </div>
          <div class="session-item static">
            <div class="session-title">Optional arguments</div>
            <div class="session-meta">Add JSON options such as num_images.</div>
          </div>
        </div>
      </aside>

      <section class="main-grid">
        <div class="panel output-panel">
          <div class="panel-title">
            <h2>Output</h2>
            <div class="panel-note">Latest results appear at the bottom.</div>
          </div>
          <div class="output-stream" id="outputStream">
            <div class="output-empty" id="outputEmpty">No outputs yet. Run an image edit to start.</div>
          </div>
        </div>

        <div class="panel input-panel">
          <div class="panel-title">
            <h2>Input</h2>
            <div class="panel-note">Ctrl/Cmd + Enter to run</div>
          </div>
          <div class="field-stack">
            <label class="field">
              <span class="field-label">Prompt</span>
              <textarea id="promptInput" placeholder="Describe the edit or transformation..."></textarea>
            </label>
            <label class="field">
              <span class="field-label">Image URLs</span>
              <textarea id="urlInput" placeholder="https://... (one per line or comma-separated)"></textarea>
              <span class="field-hint">Use URLs or leave empty if uploading files.</span>
            </label>
            <label class="field">
              <span class="field-label">Upload images</span>
              <input id="fileInput" type="file" accept="image/*" multiple />
              <span class="field-hint">PNG, JPG, or WebP. Multiple files allowed.</span>
            </label>
            <details class="payload-details">
              <summary>Arguments (JSON)</summary>
              <textarea id="argsInput" placeholder='{"num_images": 1}'></textarea>
            </details>
            <div class="controls">
              <button id="runBtn" type="button">Generate</button>
              <div class="status" id="statusText"></div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <script>
      const runBtn = document.getElementById("runBtn");
      const statusTextEl = document.getElementById("statusText");
      const statusChipEl = document.getElementById("statusChip");
      const promptEl = document.getElementById("promptInput");
      const urlEl = document.getElementById("urlInput");
      const fileEl = document.getElementById("fileInput");
      const argsEl = document.getElementById("argsInput");
      const outputStreamEl = document.getElementById("outputStream");
      const outputEmptyEl = document.getElementById("outputEmpty");
      let loading = false;

      function setStatus(message, isError = false) {
        statusTextEl.textContent = message || "";
        statusTextEl.classList.toggle("error", isError);
        statusChipEl.textContent = isError ? "error" : (message ? "busy" : "idle");
      }

      function setLoading(value) {
        loading = value;
        runBtn.disabled = value;
      }

      function formatTime(value) {
        if (!value) return "";
        const parsed = new Date(value);
        if (Number.isNaN(parsed.getTime())) return value;
        return parsed.toLocaleTimeString();
      }

      function parseImageUrls(text) {
        if (!text) return [];
        const trimmed = text.trim();
        if (!trimmed) return [];
        if (trimmed.startsWith("[")) {
          try {
            const parsed = JSON.parse(trimmed);
            if (Array.isArray(parsed)) {
              return parsed.map((item) => String(item).trim()).filter(Boolean);
            }
          } catch {
            return [];
          }
        }
        return trimmed
          .replace(/,/g, "\n")
          .split(/\r?\n/)
          .map((item) => item.trim())
          .filter(Boolean);
      }

      function extractImageUrls(payload) {
        const urls = [];
        const seen = new Set();
        const addUrl = (value) => {
          if (typeof value !== "string") return;
          if (!value.startsWith("http://") && !value.startsWith("https://") && !value.startsWith("data:")) return;
          if (seen.has(value)) return;
          seen.add(value);
          urls.push(value);
        };
        const walk = (value) => {
          if (!value) return;
          if (Array.isArray(value)) {
            value.forEach((item) => walk(item));
            return;
          }
          if (typeof value === "object") {
            Object.entries(value).forEach(([key, item]) => {
              if (typeof item === "string") {
                if (key.toLowerCase().includes("url")) addUrl(item);
              } else {
                walk(item);
              }
            });
          }
        };
        walk(payload);
        return urls;
      }

      function clearOutputEmpty() {
        if (outputEmptyEl && outputEmptyEl.isConnected) {
          outputEmptyEl.remove();
        }
      }

      function appendUserMessage(text, timestamp, urlCount, fileCount) {
        const message = document.createElement("div");
        message.className = "user-message";
        const meta = document.createElement("div");
        meta.className = "user-meta";
        const parts = [`Input - ${formatTime(timestamp)}`];
        if (urlCount) parts.push(`${urlCount} url${urlCount === 1 ? "" : "s"}`);
        if (fileCount) parts.push(`${fileCount} file${fileCount === 1 ? "" : "s"}`);
        meta.textContent = parts.join(" - ");
        const body = document.createElement("div");
        body.textContent = text;
        message.appendChild(meta);
        message.appendChild(body);
        outputStreamEl.appendChild(message);
      }

      function appendOutputCard(imageUrls, payload, timestamp) {
        const message = document.createElement("div");
        message.className = "output-message";

        const header = document.createElement("div");
        header.className = "output-header";
        const countText = imageUrls.length
          ? `${imageUrls.length} image${imageUrls.length === 1 ? "" : "s"}`
          : "no images";
        header.textContent = `Result - ${formatTime(timestamp)} - ${countText}`;

        const grid = document.createElement("div");
        grid.className = "image-grid";
        if (imageUrls.length) {
          imageUrls.forEach((url) => {
            const link = document.createElement("a");
            link.href = url;
            link.target = "_blank";
            const img = document.createElement("img");
            img.src = url;
            img.alt = "Generated image";
            link.appendChild(img);
            grid.appendChild(link);
          });
        } else {
          const empty = document.createElement("div");
          empty.className = "output-empty";
          empty.textContent = "No image URLs found in the payload.";
          grid.appendChild(empty);
        }

        const details = document.createElement("details");
        details.className = "payload-details";
        const summary = document.createElement("summary");
        summary.textContent = "Payload";
        const payloadBody = document.createElement("div");
        payloadBody.className = "payload";
        payloadBody.textContent = JSON.stringify(payload || {}, null, 2);
        details.appendChild(summary);
        details.appendChild(payloadBody);

        message.appendChild(header);
        message.appendChild(grid);
        message.appendChild(details);
        outputStreamEl.appendChild(message);
      }

      async function runImage() {
        const prompt = promptEl.value.trim();
        if (!prompt) {
          setStatus("Enter a prompt.", true);
          return;
        }

        const urls = parseImageUrls(urlEl.value);
        const files = fileEl.files;
        if ((!urls || !urls.length) && (!files || !files.length)) {
          setStatus("Provide image URLs or upload files.", true);
          return;
        }

        let args = {};
        const argsRaw = (argsEl.value || "").trim();
        if (argsRaw) {
          try {
            const parsed = JSON.parse(argsRaw);
            if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
              args = parsed;
            } else {
              setStatus("Arguments must be a JSON object.", true);
              return;
            }
          } catch (error) {
            setStatus(error.message || "Invalid JSON for arguments.", true);
            return;
          }
        }

        const formData = new FormData();
        formData.append("prompt", prompt);
        if (urls.length) {
          formData.append("image_urls", urls.join("\n"));
        }
        if (Object.keys(args).length) {
          formData.append("arguments", JSON.stringify(args));
        }
        if (files && files.length) {
          Array.from(files).forEach((file) => {
            formData.append("files", file);
          });
        }

        setStatus("Running...");
        setLoading(true);
        try {
          const response = await fetch("/image/nano-banana/edit/upload", {
            method: "POST",
            body: formData
          });
          if (!response.ok) {
            const detail = await response.text();
            throw new Error(detail || "Request failed");
          }
          const data = await response.json();
          const result = data.result || {};
          const imageUrls = extractImageUrls(result);
          const now = new Date().toISOString();
          clearOutputEmpty();
          appendUserMessage(prompt, now, urls.length, files ? files.length : 0);
          appendOutputCard(imageUrls, result, now);
          setStatus(imageUrls.length ? "Done." : "Done (no image URLs found).");
          fileEl.value = "";
        } catch (error) {
          setStatus(error.message || "Request failed.", true);
        } finally {
          setLoading(false);
        }
      }

      function bindShortcuts() {
        promptEl.addEventListener("keydown", (event) => {
          if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            event.preventDefault();
            runImage();
          }
        });
      }

      bindShortcuts();
      runBtn.addEventListener("click", runImage);
    </script>
  </body>
</html>
"""


@router.get("/image", response_class=HTMLResponse)
def image_page() -> HTMLResponse:
    return HTMLResponse(HTML)
