from functools import lru_cache

from utils.storage import read_context_text


@lru_cache(maxsize=None)
def read_context_file(filename: str) -> str:
    return read_context_text(filename)


@lru_cache(maxsize=None)
def build_context_bundle(*filenames: str) -> str:
    if not filenames:
        raise ValueError("At least one context filename is required")
    parts = [read_context_file(name) for name in filenames]
    return "\n\n---\n\n".join(parts)
