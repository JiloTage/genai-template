# GenAI Template (DSPy + FastAPI)

Minimal, production-ready template for building a generative AI web app with:
- DSPy agents
- FastAPI JSON API
- Single-page HTML/CSS/JS UI
- Optional GCS-backed storage for logs/context

## Structure

```text
context/
  system_prompt.md
src/
  agents/
    generate_agents.py
    revise_agents.py
    nanobanana_agents.py
  image_models/
    fal_ai.py
  server/
    main.py
    routers/
      generate_api.py
      generate_ui.py
      image_api.py
      image_ui.py
  utils/
    chunking.py
    context_loader.py
    data_loader.py
    diff_utils.py
    logger.py
    storage.py
```

## Setup

```powershell
uv venv
uv sync
Copy-Item .env.example .env
```

Required env vars:
- `OPENAI_API_KEY`

Optional (fal.ai for image generation):
- `FAL_KEY`

Optional (GCS):
- `GCS_BUCKET`, `GCS_PREFIX`
- `GCS_CONTEXT_OBJECT` / `GCS_CONTEXT_PREFIX`
- `GCS_LOG_OBJECT` / `GCS_LOG_PREFIX`

## Run server

```powershell
uv sync --extra server
uv run uvicorn server.main:app --reload
```

Open:
- `http://localhost:8000/`

## Endpoints

- `GET /health`
- `GET /` (UI)
- `GET /image` (Image UI)
- `POST /generate`
- `POST /generate/revise`
- `POST /image/nano-banana/edit`
- `POST /image/nano-banana/edit/upload`

### `POST /generate`

**Request**
```json
{
  "text": "Your prompt"
}
```

**Response**
```json
{
  "text": "Generated output",
  "reasoning": "Optional reasoning"
}
```

### `POST /generate/revise`

**Request**
```json
{
  "text": "Original user input",
  "instruction": "Revise the output to be shorter",
  "base": "Previous output",
  "history": ["Previous revision instruction"]
}
```

**Response**
```json
{
  "text": "Revised output",
  "reasoning": "Optional reasoning",
  "diffs": [{ "start": 10, "end": 15, "before": "old", "after": "new" }]
}
```

## Notes
- The UI stores sessions in `localStorage`.
- DSPy tracing is logged to JSONL (local or GCS) via `utils/logger.py`.
- Customize `context/system_prompt.md` to define your system instructions.

## Cloud Run (Buildpacks)

Update `cloudbuild.yaml` substitutions and deploy via Cloud Build triggers.
