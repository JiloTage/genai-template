import os

from dotenv import load_dotenv
from fastapi import FastAPI

from server.routers import generate_api, generate_ui, image_api, image_ui
from utils.logger import trace_active

load_dotenv()
trace_active()

app = FastAPI(title="genai template api", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(generate_ui.router)
app.include_router(generate_api.router)
app.include_router(image_ui.router)
app.include_router(image_api.router)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=False)
