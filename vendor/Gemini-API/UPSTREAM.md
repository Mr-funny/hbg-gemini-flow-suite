# Vendored upstream

This directory contains a source snapshot of [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API), licensed under AGPL-3.0.

Snapshot reference recorded on 2026-07-29:

```text
upstream branch: master
upstream commit: fbe0790599ac8ee77692dabdce88a96110a33294
```

The snapshot includes local compatibility changes used by HBG Gemini Flow Suite. Compare this directory with the recorded upstream commit when updating it, preserve the upstream `LICENSE`, and document material changes in the pull request.

Local compatibility notes after the recorded snapshot:

- 2026-11-01: `_parse_candidate` video lookup also checks `candidate[12][0]["60"]...` and scans `candidate[12]` for dicts with key `"60"`. Gemini Web moved the generated-video card off `[12][59]` / `[12][8]["60"]`, which left `response.videos` empty on "Your video is ready!" turns.
