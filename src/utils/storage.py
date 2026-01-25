from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os

_ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class LogTarget:
    path: Path | None = None
    object_name: str | None = None


def gcs_enabled() -> bool:
    return bool(os.getenv("GCS_BUCKET"))


@lru_cache(maxsize=1)
def _gcs_client():
    from google.cloud import storage

    return storage.Client()


def _get_bucket():
    name = os.getenv("GCS_BUCKET")
    if not name:
        raise RuntimeError("GCS_BUCKET is not set")
    return _gcs_client().bucket(name)


def _resolve_object_name(
    default_name: str,
    env_var: str | None = None,
    prefix_env: str | None = None,
) -> str:
    if env_var:
        explicit = os.getenv(env_var)
        if explicit:
            return explicit
    prefix = os.getenv(prefix_env) if prefix_env else None
    if prefix is None:
        prefix = os.getenv("GCS_PREFIX", "")
    prefix = prefix.strip("/")
    if prefix:
        return f"{prefix}/{default_name.lstrip('/')}"
    return default_name.lstrip("/")


def _resolve_local_path(default_name: str) -> Path:
    rel = default_name.lstrip("/")
    return _ROOT_DIR / rel


def _read_text_gcs(object_name: str) -> str:
    blob = _get_bucket().blob(object_name)
    if not blob.exists():
        raise FileNotFoundError(f"GCS object not found: {object_name}")
    return blob.download_as_text(encoding="utf-8")


def _write_text_gcs(object_name: str, text: str) -> None:
    blob = _get_bucket().blob(object_name)
    blob.upload_from_string(text, content_type="text/plain; charset=utf-8")


def _read_bytes_gcs(object_name: str) -> bytes:
    blob = _get_bucket().blob(object_name)
    if not blob.exists():
        raise FileNotFoundError(f"GCS object not found: {object_name}")
    return blob.download_as_bytes()


def _write_bytes_gcs(object_name: str, data: bytes, content_type: str | None = None) -> None:
    blob = _get_bucket().blob(object_name)
    blob.upload_from_string(data, content_type=content_type)


def _append_text_gcs(object_name: str, line: str) -> None:
    blob = _get_bucket().blob(object_name)
    if blob.exists():
        existing = blob.download_as_text(encoding="utf-8")
        if existing and not existing.endswith("\n"):
            existing += "\n"
    else:
        existing = ""
    payload = f"{existing}{line.rstrip()}\n"
    blob.upload_from_string(payload, content_type="text/plain; charset=utf-8")


def _read_text_local(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def _write_text_local(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_bytes_local(path: Path) -> bytes:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_bytes()


def _write_bytes_local(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _append_text_local(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")


def read_text(default_name: str, env_var: str | None = None, prefix_env: str | None = None) -> str:
    if gcs_enabled():
        object_name = _resolve_object_name(default_name, env_var=env_var, prefix_env=prefix_env)
        try:
            return _read_text_gcs(object_name)
        except FileNotFoundError:
            local_path = _resolve_local_path(default_name)
            if local_path.exists():
                text = _read_text_local(local_path)
                try:
                    _write_text_gcs(object_name, text)
                except Exception:
                    pass
                return text
            raise
    return _read_text_local(_resolve_local_path(default_name))


def write_text(
    default_name: str,
    text: str,
    env_var: str | None = None,
    prefix_env: str | None = None,
) -> None:
    if gcs_enabled():
        _write_text_gcs(_resolve_object_name(default_name, env_var=env_var, prefix_env=prefix_env), text)
        return
    _write_text_local(_resolve_local_path(default_name), text)


def read_bytes(default_name: str, env_var: str | None = None, prefix_env: str | None = None) -> bytes:
    if gcs_enabled():
        object_name = _resolve_object_name(default_name, env_var=env_var, prefix_env=prefix_env)
        try:
            return _read_bytes_gcs(object_name)
        except FileNotFoundError:
            local_path = _resolve_local_path(default_name)
            if local_path.exists():
                data = _read_bytes_local(local_path)
                try:
                    _write_bytes_gcs(object_name, data)
                except Exception:
                    pass
                return data
            raise
    return _read_bytes_local(_resolve_local_path(default_name))


def write_bytes(
    default_name: str,
    data: bytes,
    env_var: str | None = None,
    prefix_env: str | None = None,
    content_type: str | None = None,
) -> None:
    if gcs_enabled():
        _write_bytes_gcs(
            _resolve_object_name(default_name, env_var=env_var, prefix_env=prefix_env),
            data,
            content_type=content_type,
        )
        return
    _write_bytes_local(_resolve_local_path(default_name), data)


def append_text_line(
    default_name: str,
    line: str,
    env_var: str | None = None,
    prefix_env: str | None = None,
) -> None:
    if gcs_enabled():
        _append_text_gcs(_resolve_object_name(default_name, env_var=env_var, prefix_env=prefix_env), line)
        return
    _append_text_local(_resolve_local_path(default_name), line)


def read_context_text(filename: str) -> str:
    return read_text(
        f"context/{filename}",
        env_var="GCS_CONTEXT_OBJECT",
        prefix_env="GCS_CONTEXT_PREFIX",
    )


def write_context_text(filename: str, text: str) -> None:
    write_text(
        f"context/{filename}",
        text,
        env_var="GCS_CONTEXT_OBJECT",
        prefix_env="GCS_CONTEXT_PREFIX",
    )


def make_log_target(default_name: str) -> LogTarget:
    if gcs_enabled():
        object_name = _resolve_object_name(
            default_name,
            env_var="GCS_LOG_OBJECT",
            prefix_env="GCS_LOG_PREFIX",
        )
        return LogTarget(object_name=object_name)
    return LogTarget(path=_resolve_local_path(default_name))


def append_log_line(target: LogTarget, line: str) -> None:
    if target.object_name:
        _append_text_gcs(target.object_name, line)
    elif target.path:
        _append_text_local(target.path, line)
