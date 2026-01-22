#!/usr/bin/env python3
"""
Generate audio for Binary Search video and get timing.
"""

import edge_tts
import asyncio
import subprocess
import os
import json

SCRIPT = [
    {"id": "01_hook", "text": "How do you find a word in a dictionary?"},
    {"id": "02_answer", "text": "Binary Search."},
    {"id": "03_setup", "text": "Imagine a sorted array of numbers. We want to find a target value."},
    {"id": "04_naive", "text": "We could check every element one by one. But that's slow."},
    {"id": "05_insight", "text": "The key insight: if the array is sorted, we can eliminate half the elements at once."},
    {"id": "06_step1", "text": "Start in the middle. Is our target greater or less than this value?"},
    {"id": "07_step2", "text": "If greater, search the right half. If less, search the left half."},
    {"id": "08_step3", "text": "Repeat. Each step cuts the search space in half."},
    {"id": "09_example", "text": "Let's find 23 in this array. Middle is 15. 23 is greater, so go right."},
    {"id": "10_example2", "text": "New middle is 27. 23 is less, so go left. Found it!"},
    {"id": "11_complexity", "text": "With 16 elements, we need at most 4 steps. That's log n."},
    {"id": "12_takeaway", "text": "Divide and conquer turns linear search into logarithmic search."},
]


async def generate_audio(output_dir="audio_binary"):
    os.makedirs(output_dir, exist_ok=True)

    voice = "en-US-GuyNeural"
    timing = []
    cumulative = 0
    pause = 0.5

    print(f"🎙️ Generating Binary Search audio...\n")

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

    # Create concat list with gaps
    # First create silence file
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

    # Generate Python timing dict for animation code
    print("\n📋 Timing dict for animation code:")
    print("TIMING = {")
    for t in timing:
        print(f'    "{t["id"]}": {{"start": {t["start"]}, "end": {t["end"]}}},')
    print("}")

    return timing, total


if __name__ == "__main__":
    asyncio.run(generate_audio())
