"""Have Gemini watch a YouTube lesson and write down what is said and what is shown.

YouTube blocks downloads from the bot's cloud server, but Gemini fetches YouTube videos
on Google's side. This asks for a verbatim timestamped transcript plus a timestamped log
of what is on screen (charts, timeframes, prices, drawings), saved under
knowledge/sources/ so lessons can be studied from it.

Needs GEMINI_API_KEY. Usage:
    python scripts/gemini_watch.py URL --out knowledge/sources/day07_individuality.md [--model gemini-3.1-pro-preview]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

PROMPT = """You are transcribing a trading lesson for someone who cannot watch it.

Produce two sections, in Markdown:

## Transcript
Everything the speaker says, verbatim, from start to finish, including filler and
profanity. Start a new line at least every 15 seconds with a [MM:SS] timestamp.
Do not summarize or skip anything.

## On screen
A timestamped log of what is shown. Add an entry every time the screen meaningfully
changes, and at least every 60 seconds. For each entry give [MM:SS] and describe:
- whether it is a chart, a drawing, a document, a website or just the speaker
- for charts: the instrument, the timeframe (from the toolbar), the visible date range
  and price range, and which candles or areas the speaker points at
- every drawing, line, box, label, arrow or text the speaker adds, and where it is
  relative to the candles (e.g. "line at the wick high of the last up candle, ~1984.31")
- any text typed or shown on screen, copied exactly
Be precise about prices and dates you can read. Say "unreadable" rather than guessing.
"""


def watch(url: str, model: str, key: str) -> str:
    body = {
        "contents": [{"parts": [{"file_data": {"file_uri": url}}, {"text": PROMPT}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 65536},
    }
    req = urllib.request.Request(API.format(model=model), data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 503) and attempt < 3:
                print(f"[gemini] HTTP {e.code}, retrying in {20 * (attempt + 1)}s", file=sys.stderr)
                time.sleep(20 * (attempt + 1))
                continue
            raise SystemExit(f"Gemini request failed: HTTP {e.code}: {detail}")
    cand = (data.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    if not text:
        raise SystemExit(f"Gemini returned no text: {json.dumps(data)[:500]}")
    if cand.get("finishReason") not in (None, "STOP"):
        text += f"\n\n> Note: Gemini stopped early ({cand.get('finishReason')}); the end may be missing.\n"
    usage = data.get("usageMetadata", {})
    print(f"[gemini] {model}: {usage.get('promptTokenCount')} in, {usage.get('candidatesTokenCount')} out",
          file=sys.stderr)
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    args = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY is not set")
    text = watch(args.url, args.model, key)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"Source: {args.url}\nWatched by: {args.model} (Gemini), not by a human.\n\n{text}\n")
    print(out)


if __name__ == "__main__":
    main()
