from pathlib import Path
from typing import Any
from uuid import uuid4
import json
import logging
import shutil
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from agents.nanobanana_agents import Agent as NanoBananaAgent

router = APIRouter(tags=["image"])
logger = logging.getLogger(__name__)


class NanoBananaEditRequest(BaseModel):
    prompt: str = Field(min_length=1)
    image_urls: list[str] = Field(min_items=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class NanoBananaEditResponse(BaseModel):
    result: dict[str, Any]


def _filter_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in arguments.items()
        if key not in {"prompt", "image_urls", "images"}
    }


def _run_nanobanana(prompt: str, images: list[str], arguments: dict[str, Any]) -> dict[str, Any]:
    filtered_args = _filter_arguments(arguments)
    agent = NanoBananaAgent(**filtered_args)
    prediction = agent(images=images, prompt=prompt)
    result = getattr(prediction, "result", None)
    if not isinstance(result, dict):
        raise ValueError("Unexpected response from Fal AI client")
    return result


def _parse_image_urls(value: str | None) -> list[str]:
    if not value:
        return []
    text = value.strip()
    if not text:
        return []
    if text.startswith("["):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid JSON for image_urls: {exc}")
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="image_urls JSON must be a list")
        return [str(item).strip() for item in data if str(item).strip()]
    parts = [part.strip() for part in text.replace(",", "\n").splitlines()]
    return [part for part in parts if part]


@router.post("/image/nano-banana/edit", response_model=NanoBananaEditResponse)
def nano_banana_edit(req: NanoBananaEditRequest) -> NanoBananaEditResponse:
    try:
        result = _run_nanobanana(req.prompt, req.image_urls, req.arguments)
    except Exception as exc:
        logger.exception("Nano-banana edit failed")
        raise HTTPException(status_code=500, detail=str(exc))

    return NanoBananaEditResponse(result=result)


@router.post("/image/nano-banana/edit/upload", response_model=NanoBananaEditResponse)
async def nano_banana_edit_upload(
    prompt: str = Form(...),
    image_urls: str | None = Form(None),
    arguments: str | None = Form(None),
    files: list[UploadFile] | None = File(None),
) -> NanoBananaEditResponse:
    try:
        args: dict[str, Any] = {}
        if arguments:
            try:
                parsed = json.loads(arguments)
            except json.JSONDecodeError as exc:
                raise HTTPException(status_code=400, detail=f"Invalid JSON for arguments: {exc}")
            if not isinstance(parsed, dict):
                raise HTTPException(status_code=400, detail="arguments must be a JSON object")
            args = parsed

        url_list = _parse_image_urls(image_urls)
        if not files and not url_list:
            raise HTTPException(status_code=400, detail="image_urls or files are required")

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_paths: list[str] = []
            for item in files or []:
                filename = (item.filename or "").strip()
                if not filename:
                    continue
                suffix = Path(filename).suffix
                target = Path(tmpdir) / f"{uuid4().hex}{suffix}"
                with target.open("wb") as handle:
                    shutil.copyfileobj(item.file, handle)
                temp_paths.append(str(target))

            images = url_list + temp_paths
            if not images:
                raise HTTPException(status_code=400, detail="No valid image inputs provided")

            result = _run_nanobanana(prompt, images, args)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Nano-banana upload edit failed")
        raise HTTPException(status_code=500, detail=str(exc))

    return NanoBananaEditResponse(result=result)
