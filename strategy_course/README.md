# No-Wick Entry Model — course transcription

- `logs/part1_log.md` … `logs/part6_log.md`: frame-by-frame logs (frame | timestamp | on-screen change | what he was saying).
  Frames were extracted with ffmpeg scene detection `select='gt(scene,0.02)'` plus one frame every 2 s, then
  near-duplicates were removed (the webcam box and the thin crosshair are ignored when comparing frames). Kept:
  P1 147, P2 140, P3 98, P4 132, P5 134, P6 193 frames.
- `SPEC.md`: the strategy spec, built only from those logs, with open questions. No Pine Script yet.
- All 6 parts are logged.
