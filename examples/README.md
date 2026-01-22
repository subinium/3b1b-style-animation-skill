# Examples

Working demonstrations of the 3Blue1Brown style animation skill.

## Algorithm Visualizations

### Binary Search (~68s)
- `binary_search_audio.py` — TTS audio generation script
- `binary_search_synced.py` — Animation synced to audio

### DFS - Depth-First Search (~39s)
- `dfs_audio.py` — TTS audio generation script
- `dfs_synced.py` — Creative maze exploration metaphor

### Dijkstra's Algorithm (~112s)
- `dijkstra_v2_audio.py` — TTS audio generation script
- `dijkstra_v2_synced.py` — Comprehensive step-by-step explanation

### Number Theory
- `gcd_lcm_demo.py` — GCD and LCM visualization (5 scenes)

## How to Run

```bash
# Prerequisites
pip install manim edge-tts

# 1. Generate audio first
python3 dfs_audio.py

# 2. Render animation
manim -qh dfs_synced.py DFSSynced

# 3. Combine video and audio
ffmpeg -y -i media/videos/dfs_synced/1080p60/DFSSynced.mp4 \
       -i audio_dfs/full.mp3 -c:v copy -c:a aac dfs_final.mp4
```

## Workflow Pattern

All examples follow the **Explanation-First** workflow:

```
1. Write narration script (content determines length)
2. Generate TTS → Measure actual timing
3. Create animation synced to audio
4. Render and combine
```

## Key Patterns Demonstrated

| Pattern | Example |
|---------|---------|
| Audio sync | All `*_synced.py` files use `TIMING` dict from TTS |
| Segment padding | `segment()` method pads to match audio duration |
| Visual hierarchy | Colors, sizes follow 3b1b style |
| No overlapping | Proper spacing and layout zones |
| Creative metaphors | DFS uses "maze exploration" concept |

## Duration by Complexity

| Example | Duration | Complexity |
|---------|----------|------------|
| DFS | 39s | Simple algorithm |
| Binary Search | 68s | Standard algorithm |
| Dijkstra | 112s | Complex algorithm |

Duration is determined by content, not pre-set.
