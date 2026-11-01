"""Locate generated-video cards in Gemini Web candidate payloads."""

from typing import Any


def _nested(data: Any, path: list[int | str], default: Any = None) -> Any:
    """Stdlib-only nested lookup, matching ``get_nested_value`` semantics."""

    current = data
    for key in path:
        found = False
        if isinstance(key, int):
            if isinstance(current, list) and -len(current) <= key < len(current):
                current = current[key]
                found = True
        elif isinstance(key, str):
            if isinstance(current, dict) and key in current:
                current = current[key]
                found = True
        if not found:
            return default
    return current if current is not None else default


def extract_generated_video_info(candidate_data: Any) -> Any:
    """
    Return the generated-video card from a Gemini Web candidate, or ``[]``.

    Gemini Web has moved the card across ``candidate[12]`` several times:

    - legacy: ``[12][59][0][0][0]``
    - Jul 2026: ``[12][8]["60"][0][0][0][0]``
    - Nov 2026: ``[12][0]["60"][0][0][0][0]`` (dict keys ``"8"`` / ``"60"``)

    Download URLs live on that card at index ``[7]`` (thumb at ``[0]``,
    mp4 at ``[1]``), or at the older ``[0][7]`` path.
    """

    video_info = _nested(candidate_data, [12, 59, 0, 0, 0], [])
    if not video_info:
        for path in (
            [12, 8, "60", 0, 0, 0, 0],
            [12, 0, "60", 0, 0, 0, 0],
            [12, 0, 60, 0, 0, 0, 0],
        ):
            video_info = _nested(candidate_data, path, [])
            if video_info:
                break
    if not video_info:
        block12 = _nested(candidate_data, [12], [])
        if isinstance(block12, list):
            for item in block12:
                if isinstance(item, dict) and ("60" in item or 60 in item):
                    card = item.get("60", item.get(60))
                    video_info = _nested(card, [0, 0, 0, 0], [])
                    if video_info:
                        break
    return video_info or []


def extract_generated_video_urls(candidate_data: Any) -> tuple[str, str] | None:
    """
    Return ``(thumbnail_url, mp4_url)`` from a candidate, or ``None``.
    """

    video_info = extract_generated_video_info(candidate_data)
    if not video_info:
        return None
    urls = _nested(video_info, [0, 7], [])
    if not urls:
        urls = _nested(video_info, [7], [])
    if isinstance(urls, list) and len(urls) >= 2 and urls[0] and urls[1]:
        return str(urls[0]), str(urls[1])
    return None
