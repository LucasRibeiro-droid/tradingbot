"""Transcribe a lesson's audio offline with Whisper (via sherpa-onnx), with timestamps.

For uploaded videos that have audio. Nothing leaves the machine. Needs
``pip install sherpa-onnx numpy`` plus the Whisper model and Silero voice detector from
https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models
(sherpa-onnx-whisper-small.en.tar.bz2 and silero_vad.onnx) in --model-dir.

Usage:
    python scripts/transcribe_local.py VIDEO --out knowledge/sources/day10.md --model-dir DIR
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import sherpa_onnx

RATE = 16000


def load_audio(path: str) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(RATE),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def transcribe(audio: np.ndarray, model_dir: Path, threads: int) -> list[tuple[float, str]]:
    w = model_dir / "sherpa-onnx-whisper-small.en"
    recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(w / "small.en-encoder.int8.onnx"), decoder=str(w / "small.en-decoder.int8.onnx"),
        tokens=str(w / "small.en-tokens.txt"), language="en", task="transcribe", num_threads=threads)
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = str(model_dir / "silero_vad.onnx")
    cfg.silero_vad.min_silence_duration = 0.25
    cfg.silero_vad.max_speech_duration = 20  # Whisper handles at most 30 seconds at a time
    cfg.sample_rate = RATE
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=60)

    segments = []
    window = cfg.silero_vad.window_size
    for start in range(0, len(audio), window):
        vad.accept_waveform(audio[start:start + window])
        while not vad.empty():
            seg = vad.front
            stream = recognizer.create_stream()
            stream.accept_waveform(RATE, seg.samples)
            recognizer.decode_stream(stream)
            text = stream.result.text.strip()
            if text:
                segments.append((seg.start / RATE, text))
            vad.pop()
    vad.flush()
    while not vad.empty():
        seg = vad.front
        stream = recognizer.create_stream()
        stream.accept_waveform(RATE, seg.samples)
        recognizer.decode_stream(stream)
        if stream.result.text.strip():
            segments.append((seg.start / RATE, stream.result.text.strip()))
        vad.pop()
    return segments


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model-dir", required=True, type=Path)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--source", default="", help="original URL or title, written at the top")
    args = ap.parse_args()
    audio = load_audio(args.video)
    print(f"[transcribe] {len(audio) / RATE / 60:.1f} minutes of audio", file=sys.stderr)
    lines = [f"[{int(t // 60):02d}:{int(t % 60):02d}] {text}" for t, text in transcribe(audio, args.model_dir, args.threads)]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"Source: {args.source or Path(args.video).name}\nTranscribed offline by Whisper small.en "
                   f"(sherpa-onnx). Machine transcription: expect some misheard words.\n\n## Transcript\n\n"
                   + "\n".join(lines) + "\n")
    print(out)


if __name__ == "__main__":
    main()
