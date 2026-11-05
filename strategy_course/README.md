# No-Wick Entry Model — course transcription

- `logs/part1_log.md` … `logs/part5_log.md`: frame-by-frame logs (frame | timestamp | on-screen change | what he was saying).
  Frames were extracted with ffmpeg scene detection `select='gt(scene,0.02)'` plus one frame every 2 s, then
  near-duplicates were removed (the webcam box and the thin crosshair are ignored when comparing frames). Kept:
  P1 147, P2 140, P3 98, P4 132, P5 134 frames.
- `SPEC.md`: the strategy spec, built only from those logs, with open questions. No Pine Script yet.
- Part 6 (35:03 → 42:02) hasn't been received yet.
