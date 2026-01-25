import re

CHUNK_THRESHOLD = 2400
CHUNK_TARGET = 800
CHUNK_MAX = 800

SENTENCE_RE = re.compile(r".+?(?:[.!?]+|$)", re.DOTALL)


def _split_by_length(text: str, limit: int) -> list[str]:
    return [text[i : i + limit] for i in range(0, len(text), limit)]


def _split_sentences(text: str) -> list[str]:
    sentences = [item.strip() for item in SENTENCE_RE.findall(text) if item.strip()]
    return sentences or ([text.strip()] if text.strip() else [])


def build_chunks(
    text: str,
    threshold: int = CHUNK_THRESHOLD,
    target_len: int = CHUNK_TARGET,
    max_len: int = CHUNK_MAX,
) -> list[str]:
    """Split text into chunks that are easier for LLMs to handle."""
    normalized = text.strip()
    if not normalized:
        return []
    if len(normalized) <= threshold:
        return [normalized]

    paragraphs = [p.strip() for p in re.split(r"\n{2,}", normalized) if p.strip()]
    sentences: list[str] = []
    for paragraph in paragraphs:
        sentences.extend(_split_sentences(paragraph))

    if not sentences:
        return [normalized]

    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) > max_len:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_split_by_length(sentence, max_len))
            continue

        if not current:
            current = sentence
        elif len(current) + 1 + len(sentence) <= max_len:
            current = f"{current} {sentence}"
        else:
            chunks.append(current)
            current = sentence

        if len(current) >= target_len:
            chunks.append(current)
            current = ""

    if current:
        chunks.append(current)

    return chunks or [normalized]
