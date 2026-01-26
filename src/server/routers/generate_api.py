from functools import lru_cache
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agents.generate_agents import Agent as GenerateAgent
from agents.revise_agents import Agent as ReviseAgent
from utils.diff_utils import build_highlight_diffs

router = APIRouter(tags=["generate"])
logger = logging.getLogger(__name__)


class GenerateRequest(BaseModel):
    text: str = Field(min_length=1)


class GenerateResponse(BaseModel):
    text: str
    reasoning: str = ""


class HighlightDiff(BaseModel):
    start: int
    end: int
    before: str = ""
    after: str = ""


class ReviseRequest(BaseModel):
    text: str = Field(min_length=1)
    instruction: str = Field(min_length=1)
    base: str = ""
    history: list[str] | None = None


class ReviseResponse(BaseModel):
    text: str
    reasoning: str = ""
    diffs: list[HighlightDiff] = Field(default_factory=list)


@lru_cache(maxsize=1)
def get_generate_agent() -> GenerateAgent:
    return GenerateAgent()


@lru_cache(maxsize=1)
def get_revise_agent() -> ReviseAgent:
    return ReviseAgent()


def _join_history(history: list[str] | None, instruction: str) -> str:
    items = [item.strip() for item in (history or []) if item.strip()]
    instruction = instruction.strip()
    if instruction:
        items.append(instruction)
    return "\n".join(items)


def _extract_text_and_reasoning(result) -> tuple[str, str]:
    if isinstance(result, dict):
        text = result.get("text", "")
        reasoning = result.get("reasoning", "")
    else:
        text = getattr(result, "text", "")
        reasoning = getattr(result, "reasoning", "")
    return (text or "").strip(), (reasoning or "").strip()


@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    try:
        agent = get_generate_agent()
        result = agent(text=req.text)
    except Exception as exc:
        logger.exception("Generate failed")
        raise HTTPException(status_code=500, detail=str(exc))

    text, reasoning = _extract_text_and_reasoning(result)
    if not text:
        raise HTTPException(status_code=400, detail="Empty output.")

    return GenerateResponse(text=text, reasoning=reasoning)


@router.post("/generate/revise", response_model=ReviseResponse)
def revise(req: ReviseRequest) -> ReviseResponse:
    instruction = _join_history(req.history, req.instruction)

    try:
        agent = get_revise_agent()
        result = agent(
            text=req.text,
            instruction=instruction,
            base=req.base,
        )
    except Exception as exc:
        logger.exception("Revision failed")
        raise HTTPException(status_code=500, detail=str(exc))

    text, reasoning = _extract_text_and_reasoning(result)
    if not text:
        raise HTTPException(status_code=400, detail="Empty output.")

    diffs = []
    if req.base and text and req.base != text:
        diffs = build_highlight_diffs(req.base, text)

    return ReviseResponse(text=text, reasoning=reasoning, diffs=diffs)
