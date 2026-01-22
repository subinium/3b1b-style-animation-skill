#!/usr/bin/env python3
"""
Generate audio for DFS (Depth-First Search) video.
Creative concept: Maze exploration metaphor.
"""

import edge_tts
import asyncio
import subprocess
import os
import json

# Short, punchy script for ~45s video
SCRIPT = [
    {"id": "01_hook", "text": "How do you escape a maze?"},
    {"id": "02_insight", "text": "Go as deep as you can. Hit a wall? Backtrack and try another path."},
    {"id": "03_name", "text": "This is Depth-First Search."},
    {"id": "04_start", "text": "Start at the entrance. Pick a path and commit."},
    {"id": "05_deep", "text": "Keep going deeper. Don't look back."},
    {"id": "06_stuck", "text": "Dead end! Time to backtrack."},
    {"id": "07_try", "text": "Back up and try the next unexplored path."},
    {"id": "08_found", "text": "Keep exploring until you find the exit."},
    {"id": "09_takeaway", "text": "Depth-first: Dive deep, then retreat. That's DFS."},
]


async def generate_audio(output_dir="audio_dfs"):
    os.makedirs(output_dir, exist_ok=True)

    voice = "en-US-GuyNeural"
    timing = []
    cumulative = 0
    pause = 0.4  # Slightly shorter pause for punchy feel

    print(f"🎙️ Generating DFS audio...\n")

    for seg in SCRIPT:
        path = f"{output_dir}/{seg['id']}.mp3"

        communicate = edge_tts.Communicate(seg["text"], voice)
        await communicate.save(path)

        # Get duration using ffprobe
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())

        timing.append({
            "id": seg["id"],
            "start": round(cumulative, 2),
            "duration": round(duration, 2),
            "end": round(cumulative + duration + pause, 2),
            "text": seg["text"]
        })

        print(f"  [{cumulative:5.1f}s] {seg['id']}: {duration:.1f}s")
        cumulative += duration + pause

    total = cumulative
    print(f"\n✅ Total: {total:.1f}s")

    # Save timing
    with open(f"{output_dir}/timing.json", "w") as f:
        json.dump({"total": total, "segments": timing}, f, indent=2)

    # Create silence for gaps
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(pause), "-q:a", "9", "-acodec", "libmp3lame",
        f"{output_dir}/silence.mp3"
    ], capture_output=True)

    # Concat list with silences
    with open(f"{output_dir}/concat.txt", "w") as f:
        for i, seg in enumerate(SCRIPT):
            f.write(f"file '{seg['id']}.mp3'\n")
            if i < len(SCRIPT) - 1:
                f.write(f"file 'silence.mp3'\n")

    # Create full audio
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", f"{output_dir}/concat.txt", "-c", "copy",
        f"{output_dir}/full.mp3"
    ], capture_output=True)

    print(f"\n📁 Files saved to {output_dir}/")

    # Print timing dict
    print("\n📋 TIMING = {")
    for t in timing:
        print(f'    "{t["id"]}": {{"start": {t["start"]}, "end": {t["end"]}}},')
    print("}")

    return timing, total


if __name__ == "__main__":
    asyncio.run(generate_audio())
