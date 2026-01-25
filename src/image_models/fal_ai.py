from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

import fal_client

ImageSource = str | Path
QueueUpdateHandler = Callable[[fal_client.Status], None]


class FalAIClient:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        *,
        default_timeout: float = 120.0,
    ) -> None:
        self.model = model
        self._client = fal_client.SyncClient(
            key=api_key,
            default_timeout=default_timeout,
        )

    @staticmethod
    def _is_url(value: str) -> bool:
        return value.startswith(("http://", "https://", "data:"))

    def ensure_url(self, source: ImageSource) -> str:
        if isinstance(source, str) and self._is_url(source):
            return source
        return self._client.upload_file(Path(source))

    def ensure_urls(self, sources: Iterable[ImageSource]) -> list[str]:
        return [self.ensure_url(source) for source in sources]

    def generate(
        self,
        *,
        with_logs: bool = False,
        on_queue_update: QueueUpdateHandler | None = None,
        **arguments: Any,
    ) -> dict[str, Any]:
        return self._client.subscribe(
            self.model,
            arguments=arguments,
            with_logs=with_logs,
            on_queue_update=on_queue_update,
        )
