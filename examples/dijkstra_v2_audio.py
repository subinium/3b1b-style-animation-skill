#!/usr/bin/env python3
"""
Generate audio for Dijkstra v2 - Comprehensive version (2-3 min).
"""

import edge_tts
import asyncio
import subprocess
import os
import json

# Comprehensive script for 2-3 min video
SCRIPT = [
    # Hook
    {"id": "01_hook", "text": "How does your GPS find the shortest route?"},
    {"id": "02_answer", "text": "It uses Dijkstra's algorithm."},

    # Setup
    {"id": "03_graph", "text": "Imagine a map as a graph. Cities are nodes. Roads are edges with distances."},
    {"id": "04_problem", "text": "We want the shortest path from a starting city to all other cities."},

    # Key Insight
    {"id": "05_insight", "text": "Here's the key insight: always visit the closest unvisited city first."},
    {"id": "06_why", "text": "Why? Because if it's the closest, no other path can be shorter."},

    # Initialize
    {"id": "07_init", "text": "Start by setting the distance to your starting point as zero, and everything else as infinity."},
    {"id": "08_begin", "text": "Now we begin. From A, we can reach B and C."},

    # Step by step
    {"id": "09_step1", "text": "The distance to B through A is 4. The distance to C through A is 2."},
    {"id": "10_pick_c", "text": "C is closer. So we visit C first and mark it as done."},
    {"id": "11_from_c", "text": "From C, we can reach B in 2 plus 1 equals 3. That's better than 4!"},
    {"id": "12_update_b", "text": "We update B's distance to 3. We can also reach D through C in 10."},
    {"id": "13_visit_b", "text": "Now B is the closest unvisited. Visit B."},
    {"id": "14_from_b", "text": "From B, we can reach D in 3 plus 5 equals 8. That's better than 10!"},
    {"id": "15_visit_d", "text": "Visit D. From D, we reach E in 8 plus 2 equals 10."},
    {"id": "16_visit_e", "text": "Finally, visit E. All nodes are done."},

    # Complete
    {"id": "17_result", "text": "We now have the shortest distance from A to every other node."},
    {"id": "18_path", "text": "The shortest path to E is A to C to B to D to E, with total distance 10."},

    # Takeaway
    {"id": "19_takeaway", "text": "Dijkstra's algorithm: always pick the closest, and you'll find the optimal path."},
    {"id": "20_complexity", "text": "It runs in O of V squared, or O of E log V with a priority queue."},
]


async def generate_audio(output_dir="audio_dijkstra_v2"):
    os.makedirs(output_dir, exist_ok=True)

    voice = "en-US-GuyNeural"
    timing = []
    cumulative = 0
    pause = 0.5

    print(f"🎙️ Generating Dijkstra v2 audio...\n")

    for seg in SCRIPT:
        path = f"{output_dir}/{seg['id']}.mp3"

        communicate = edge_tts.Communicate(seg["text"], voice)
        await communicate.save(path)

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
    print(f"\n✅ Total: {total:.1f}s ({total/60:.1f} min)")

    # Save timing
    with open(f"{output_dir}/timing.json", "w") as f:
        json.dump({"total": total, "segments": timing}, f, indent=2)

    # Create silence
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(pause), "-q:a", "9", "-acodec", "libmp3lame",
        f"{output_dir}/silence.mp3"
    ], capture_output=True)

    # Concat list
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
