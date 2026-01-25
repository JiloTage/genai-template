import json
import time
import copy
from typing import Any

import dspy
from dspy.utils.callback import BaseCallback

from utils.storage import append_log_line, make_log_target

def trace_active():
    dspy.configure(callbacks=[JsonlTraceCallback()], track_usage=True)


class JsonlTraceCallback(BaseCallback):
    def __init__(self):
        super().__init__()
        timestamp = time.strftime("%Y%m%d%H%M%S")
        default_name = f".log/dspy_trace_{timestamp}.jsonl"
        self.log_target = make_log_target(default_name)
        self._module_instances: dict[str, Any] = {}
        self._lm_instances: dict[str, Any] = {}
        self._lm_history_len: dict[str, int | None] = {}

    def _dumpable(self, x):
        try:
            json.dumps(x, ensure_ascii=False)
            return x
        except TypeError:
            return str(x)

    def _safe_copy(self, value: Any) -> Any:
        try:
            return copy.deepcopy(value)
        except Exception:
            return value

    def _merge_usage_entries(
        self,
        usage_entry1: dict[str, Any] | None,
        usage_entry2: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not usage_entry1:
            return dict(usage_entry2 or {})
        if not usage_entry2:
            return dict(usage_entry1)

        result = dict(usage_entry2)
        for k, v in usage_entry1.items():
            current_v = result.get(k)
            if isinstance(v, dict) or isinstance(current_v, dict):
                result[k] = self._merge_usage_entries(
                    current_v if isinstance(current_v, dict) else {},
                    v if isinstance(v, dict) else {},
                )
            elif isinstance(v, (int, float)) and isinstance(current_v, (int, float)):
                result[k] = (current_v or 0) + (v or 0)
            elif current_v is None:
                result[k] = v
            else:
                result[k] = current_v
        return result

    def _merge_usage_list(self, usage_entries: list[dict[str, Any]]) -> dict[str, Any] | None:
        merged: dict[str, Any] = {}
        for entry in usage_entries:
            if entry:
                merged = self._merge_usage_entries(merged, entry)
        return merged or None

    def _extract_usage_from_outputs(self, outputs: Any) -> dict[str, Any] | None:
        if outputs is None:
            return None
        if hasattr(outputs, "get_lm_usage"):
            return outputs.get_lm_usage()
        if isinstance(outputs, (list, tuple)):
            for item in outputs:
                usage = self._extract_usage_from_outputs(item)
                if usage:
                    return usage
        if isinstance(outputs, dict):
            for value in outputs.values():
                usage = self._extract_usage_from_outputs(value)
                if usage:
                    return usage
        return None

    def _extract_lm_usage_from_history(
        self,
        instance: Any,
        start_index: int | None,
    ) -> dict[str, Any] | None:
        history = getattr(instance, "history", None)
        if not history:
            return None
        if start_index is None:
            start_index = max(len(history) - 1, 0)
        start_index = max(0, min(start_index, len(history)))
        usage_entries = []
        for entry in history[start_index:]:
            if isinstance(entry, dict):
                usage = entry.get("usage")
                if usage:
                    usage_entries.append(usage)
        return self._merge_usage_list(usage_entries)

    def _write(self, event: str, **payload):
        rec = {
            "event": event,
            **{k: self._dumpable(v) for k, v in payload.items()},
        }
        append_log_line(self.log_target, json.dumps(rec, ensure_ascii=False))

    def on_module_start(self, call_id, instance, inputs):
        self._module_instances[call_id] = instance
        self._write(
            "model_start",
            call_id=call_id,
            instance=self._safe_copy(instance),
            inputs=self._safe_copy(inputs),
        )

    def on_module_end(self, call_id, outputs, exception=None):
        instance = self._module_instances.pop(call_id, None)
        token_usage = self._extract_usage_from_outputs(outputs)
        self._write(
            "model_end",
            call_id=call_id,
            instance=self._safe_copy(instance),
            outputs=self._safe_copy(outputs),
            token_usage=token_usage,
            usage=token_usage,
            exception=exception,
        )

    def on_lm_start(self, call_id, instance, inputs):
        history = getattr(instance, "history", None)
        self._lm_instances[call_id] = instance
        self._lm_history_len[call_id] = len(history) if history is not None else None
        self._write(
            "lm_start",
            call_id=call_id,
            model=getattr(instance, "model", None),
            inputs=self._safe_copy(inputs),
        )

    def on_lm_end(self, call_id, outputs, exception=None):
        instance = self._lm_instances.pop(call_id, None)
        start_index = self._lm_history_len.pop(call_id, None)
        token_usage = (
            self._extract_lm_usage_from_history(instance, start_index)
            if instance is not None
            else None
        )
        self._write(
            "lm_end",
            call_id=call_id,
            model=getattr(instance, "model", None),
            outputs=self._safe_copy(outputs),
            token_usage=token_usage,
            usage=token_usage,
            exception=exception,
        )
