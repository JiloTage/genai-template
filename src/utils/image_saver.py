from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import unquote_to_bytes
from urllib.request import urlopen

_PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def _unwrap_result(output: Any) -> Any:
    if hasattr(output, "result"):
        return output.result
    return output


def _extract_image_entry(payload: Any, image_index: int) -> Any:
    if isinstance(payload, dict):
        if "images" in payload:
            images = payload["images"]
            if isinstance(images, list) and images:
                if image_index < 0 or image_index >= len(images):
                    raise IndexError("image_index is out of range")
                return images[image_index]
        if "layers" in payload:
            layers = payload["layers"]
            if isinstance(layers, list) and layers:
                if image_index < 0 or image_index >= len(layers):
                    raise IndexError("image_index is out of range")
                return layers[image_index]
        if "image" in payload:
            return payload["image"]
    return payload


def _extract_image_entries(payload: Any) -> list[Any]:
    if isinstance(payload, dict):
        if "images" in payload:
            images = payload["images"]
            if isinstance(images, list) and images:
                return list(images)
        if "layers" in payload:
            layers = payload["layers"]
            if isinstance(layers, list) and layers:
                return list(layers)
        if "image" in payload:
            return [payload["image"]]
    if isinstance(payload, list) and payload:
        return list(payload)
    return [payload]


def _extract_image_url(entry: Any) -> tuple[str, str | None]:
    content_type = None
    if isinstance(entry, str):
        return entry, None
    if isinstance(entry, dict):
        if isinstance(entry.get("content_type"), str):
            content_type = entry["content_type"]
        for key in ("url", "image_url"):
            value = entry.get(key)
            if isinstance(value, str):
                return value, content_type
    raise ValueError("画像URLが見つかりません")


def _decode_data_url(source: str) -> tuple[bytes, str | None]:
    header, data = source.split(",", 1)
    meta = header[5:]
    is_base64 = ";base64" in meta
    media_type = meta.split(";")[0] if meta else None
    if is_base64:
        return base64.b64decode(data), media_type
    return unquote_to_bytes(data), media_type


def _read_image_bytes(source: str, *, timeout: float) -> tuple[bytes, str | None]:
    if source.startswith("data:"):
        return _decode_data_url(source)
    if source.startswith(("http://", "https://")):
        with urlopen(source, timeout=timeout) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type")
        return data, content_type
    data = Path(source).read_bytes()
    return data, None


def _normalize_output_base(output_base: str | Path) -> tuple[Path, str]:
    path = Path(output_base)
    if path.suffix:
        return path.parent, path.stem
    return path, "image"


def _resolve_single_output_path(output_path: str | Path) -> Path:
    path = Path(output_path)
    if path.exists() and path.is_dir():
        path = path / "image.png"
    if path.suffix.lower() != ".png":
        path = path.with_suffix(".png")
    return path


def _resolve_psd_output_path(output_path: str | Path) -> Path:
    path = Path(output_path)
    if path.exists() and path.is_dir():
        path = path / "layers.psd"
    if path.suffix.lower() != ".psd":
        path = path.with_suffix(".psd")
    return path


def _save_png_bytes(
    data: bytes,
    content_type: str | None,
    output_base: str | Path,
    *,
    index: int | None = None,
) -> Path:
    if content_type and not content_type.startswith("image/png"):
        raise ValueError(f"PNG以外の画像形式です: {content_type}")
    if not data.startswith(_PNG_HEADER):
        raise ValueError("PNG以外のバイト列です。PNGで生成してください。")

    output_dir, prefix = _normalize_output_base(output_base)
    if index is None:
        filename = f"{prefix}.png"
    else:
        filename = f"{prefix}_{index}.png"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_bytes(data)
    return path


def save_agent_image_png(
    output: Any,
    output_path: str | Path,
    *,
    image_index: int = 0,
    timeout: float = 30.0,
) -> Path:
    """Agent出力からPNG画像を保存する。"""
    payload = _unwrap_result(output)
    entry = _extract_image_entry(payload, image_index)
    image_url, content_type = _extract_image_url(entry)
    data, fetched_content_type = _read_image_bytes(image_url, timeout=timeout)
    effective_content_type = content_type or fetched_content_type
    resolved_path = _resolve_single_output_path(output_path)
    return _save_png_bytes(data, effective_content_type, resolved_path)


def save_agent_images_png(
    output: Any,
    output_dir: str | Path,
    *,
    start_index: int = 0,
    timeout: float = 30.0,
) -> list[Path]:
    """Agent出力から複数のPNG画像を保存する。"""
    payload = _unwrap_result(output)
    entries = _extract_image_entries(payload)
    saved: list[Path] = []
    for offset, entry in enumerate(entries):
        image_url, content_type = _extract_image_url(entry)
        data, fetched_content_type = _read_image_bytes(image_url, timeout=timeout)
        effective_content_type = content_type or fetched_content_type
        saved.append(
            _save_png_bytes(
                data,
                effective_content_type,
                output_dir,
                index=start_index + offset,
            )
        )
    return saved


def save_agent_layered_psd(
    output: Any,
    output_path: str | Path,
    *,
    timeout: float = 30.0,
    layer_names: Sequence[str] | None = None,
) -> Path:
    """image_layered の出力からレイヤー付きPSDを保存する。"""
    payload = _unwrap_result(output)
    entries = _extract_image_entries(payload)
    if layer_names is not None and len(layer_names) != len(entries):
        raise ValueError("layer_names の数がレイヤー数と一致しません")

    try:
        import numpy as np
        from PIL import Image
        import packbits
        from pytoshop import enums
        from pytoshop import codecs as pytoshop_codecs
        from pytoshop.user import nested_layers
    except ImportError as exc:
        raise ImportError("PSD保存には pytoshop / pillow / numpy / packbits が必要です") from exc

    if getattr(pytoshop_codecs, "packbits", None) is None:
        pytoshop_codecs.packbits = packbits

    layers: list[nested_layers.Layer] = []
    max_width = 0
    max_height = 0

    for index, entry in enumerate(entries):
        image_url, content_type = _extract_image_url(entry)
        data, fetched_content_type = _read_image_bytes(image_url, timeout=timeout)
        effective_content_type = content_type or fetched_content_type
        if effective_content_type and not effective_content_type.startswith("image/png"):
            raise ValueError(f"PNG以外の画像形式です: {effective_content_type}")

        image = Image.open(BytesIO(data)).convert("RGBA")
        width, height = image.size
        max_width = max(max_width, width)
        max_height = max(max_height, height)
        rgba = np.asarray(image, dtype=np.uint8)
        if rgba.ndim != 3 or rgba.shape[2] < 4:
            raise ValueError("RGBA画像を指定してください")

        channels = {
            enums.ChannelId.red: rgba[:, :, 0],
            enums.ChannelId.green: rgba[:, :, 1],
            enums.ChannelId.blue: rgba[:, :, 2],
            enums.ChannelId.transparency: rgba[:, :, 3],
        }
        name = layer_names[index] if layer_names else f"layer_{index}"
        layer = nested_layers.Image(
            name=name,
            top=0,
            left=0,
            bottom=height,
            right=width,
            channels=channels,
            color_mode=enums.ColorMode.rgb,
        )
        layers.append(layer)

    psd = nested_layers.nested_layers_to_psd(
        layers,
        color_mode=enums.ColorMode.rgb,
        size=(max_height, max_width),
    )
    path = _resolve_psd_output_path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        psd.write(handle)
    return path
