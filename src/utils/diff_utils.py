from __future__ import annotations

from difflib import SequenceMatcher


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []
    ranges = sorted(ranges, key=lambda item: (item[0], item[1]))
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def build_highlight_ranges(before: str, after: str) -> list[tuple[int, int]]:
    if not before or not after or before == after:
        return []
    matcher = SequenceMatcher(a=before, b=after)
    ranges: list[tuple[int, int]] = []
    for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "insert") and j2 > j1:
            ranges.append((j1, j2))
    return _merge_ranges(ranges)


def build_highlight_diffs(before: str, after: str) -> list[dict]:
    if not before or not after or before == after:
        return []
    matcher = SequenceMatcher(a=before, b=after)
    diffs: list[dict] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "insert") and j2 > j1:
            diffs.append(
                {
                    "start": j1,
                    "end": j2,
                    "before": before[i1:i2],
                    "after": after[j1:j2],
                }
            )
    return diffs
