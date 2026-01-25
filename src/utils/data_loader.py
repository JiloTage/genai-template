from pathlib import Path


_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_data_text(relative_path: str) -> str:
    """Load text from `data/relative_path`.

    - If `relative_path` points to a file: return its UTF-8 content.
    - If it points to a directory: read all files under it (recursive), sort by
      relative path, and concatenate contents with newlines.
    Raises FileNotFoundError if missing; ValueError if path escapes `data/`.
    """
    base = _DATA_DIR
    target = (base / relative_path).resolve()
    if base not in target.parents and target != base:
        raise ValueError("Path must stay within the data directory")
    if not target.exists():
        raise FileNotFoundError(target)

    if target.is_dir():
        files = [
            p
            for p in target.rglob("*")
            if p.is_file()
        ]
        # Stable order for reproducible prompts
        files.sort(key=lambda p: p.relative_to(base).as_posix())
        contents = [p.read_text(encoding="utf-8") for p in files]
        return "\n\n".join(contents)

    return target.read_text(encoding="utf-8")
