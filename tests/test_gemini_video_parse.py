from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from typing import Any


HELPER_PATH = (
    Path(__file__).resolve().parents[1]
    / "vendor"
    / "Gemini-API"
    / "src"
    / "gemini_webapi"
    / "utils"
    / "generated_video.py"
)
CLIENT_PATH = (
    Path(__file__).resolve().parents[1]
    / "vendor"
    / "Gemini-API"
    / "src"
    / "gemini_webapi"
    / "client.py"
)

_spec = importlib.util.spec_from_file_location(
    "gemini_generated_video", HELPER_PATH
)
assert _spec and _spec.loader
generated_video = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(generated_video)
extract_generated_video_urls = generated_video.extract_generated_video_urls


THUMB = "https://example.test/thumb.jpg"
MP4 = "https://example.test/video.mp4"


def _slot(index: int, value: Any, fill: Any = None) -> list[Any]:
    items = [fill] * (index + 1)
    items[index] = value
    return items


def _card_with_urls_at_7() -> list[Any]:
    return _slot(7, [THUMB, MP4])


def _card_with_urls_at_0_7() -> list[Any]:
    return [_slot(7, [THUMB, MP4])]


def _wrap_card(card: Any) -> list[Any]:
    return [[[[card]]]]


class GeminiVideoParseTests(unittest.TestCase):
    def test_client_wires_helper_and_documents_nov2026_paths(self) -> None:
        source = CLIENT_PATH.read_text(encoding="utf-8")
        self.assertIn("extract_generated_video_urls", source)
        self.assertIn('candidate[12][0]["60"]', source)
        helper = HELPER_PATH.read_text(encoding="utf-8")
        self.assertIn('[12, 0, "60", 0, 0, 0, 0]', helper)
        self.assertIn('[12, 8, "60", 0, 0, 0, 0]', helper)
        self.assertIn("[12, 59, 0, 0, 0]", helper)
        self.assertIn('"60" in item or 60 in item', helper)

    def test_legacy_path_12_59(self) -> None:
        candidate = _slot(12, _slot(59, [[[_card_with_urls_at_0_7()]]]))
        self.assertEqual(extract_generated_video_urls(candidate), (THUMB, MP4))

    def test_july_2026_path_12_8_60(self) -> None:
        candidate = _slot(12, _slot(8, {"60": _wrap_card(_card_with_urls_at_7())}))
        self.assertEqual(extract_generated_video_urls(candidate), (THUMB, MP4))

    def test_nov_2026_path_12_0_60(self) -> None:
        candidate = _slot(12, [{"60": _wrap_card(_card_with_urls_at_7())}])
        self.assertEqual(extract_generated_video_urls(candidate), (THUMB, MP4))

    def test_fallback_scan_finds_60_card_at_another_index(self) -> None:
        block12 = [None, None, None, {"60": _wrap_card(_card_with_urls_at_7())}]
        candidate = _slot(12, block12)
        self.assertEqual(extract_generated_video_urls(candidate), (THUMB, MP4))

    def test_fallback_scan_accepts_int_key_60(self) -> None:
        candidate = _slot(12, [{60: _wrap_card(_card_with_urls_at_7())}])
        self.assertEqual(extract_generated_video_urls(candidate), (THUMB, MP4))

    def test_missing_video_card_returns_none(self) -> None:
        self.assertIsNone(extract_generated_video_urls([]))
        self.assertIsNone(extract_generated_video_urls(_slot(12, [None, {}, []])))


if __name__ == "__main__":
    unittest.main()
