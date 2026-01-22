---
name: video-completion
description: Ensuring video ends properly - both duration and content
metadata:
  tags: video, audio, completion, duration, ffmpeg, content
priority: highest
---

# Video Completion Checklist

**Two types of completion must be verified:**
1. **Duration** - Video must not cut off audio
2. **Content** - All animations must complete fully

## The Problem

```
❌ BAD: Video ends at 47.5s, Audio ends at 50.0s
   → Last 2.5 seconds of narration cut off!

❌ BAD: Audio ends at 50.0s, Video ends at 50.0s exactly
   → Abrupt ending, no breathing room

✅ GOOD: Video ends at 52.0s, Audio ends at 50.0s
   → Clean ending with 2s padding
```

## Required: End Padding

**Always add 1-2 seconds of padding at the end of your animation.**

```python
def seg_final(self):
    """Final segment - MUST include end padding."""
    # ... your final animations ...

    # REQUIRED: End padding (1-2 seconds)
    self.wait(1.5)
```

## Duration Verification

### Step 1: After Audio Generation

```python
async def generate_audio(output_dir="audio"):
    # ... generate audio ...

    total_audio_duration = cumulative
    print(f"✅ Total audio: {total_audio_duration:.1f}s")

    # Save for verification
    with open(f"{output_dir}/duration.txt", "w") as f:
        f.write(str(total_audio_duration))

    return total_audio_duration
```

### Step 2: In Animation Code

```python
class MyScene(Scene):
    # Expected total from audio generation
    EXPECTED_DURATION = 50.0  # seconds
    END_PADDING = 1.5  # minimum end padding

    def construct(self):
        # ... all your segments ...

        # REQUIRED: Final padding
        self.wait(self.END_PADDING)

        # The video should be at least EXPECTED_DURATION + END_PADDING
```

### Step 3: Post-Render Verification

```bash
# Get video duration
VIDEO_DUR=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 video.mp4)

# Get audio duration
AUDIO_DUR=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 audio.mp3)

echo "Video: ${VIDEO_DUR}s, Audio: ${AUDIO_DUR}s"

# Check: Video must be >= Audio
if (( $(echo "$VIDEO_DUR < $AUDIO_DUR" | bc -l) )); then
    echo "❌ ERROR: Video shorter than audio!"
    exit 1
fi
```

## FFmpeg Combination Rules

### DO NOT use `-shortest` alone

```bash
# ❌ BAD: May cut off audio
ffmpeg -i video.mp4 -i audio.mp3 -shortest output.mp4

# ✅ GOOD: Pad video to match audio if needed
ffmpeg -y -i video.mp4 -i audio.mp3 \
  -c:v copy -c:a aac \
  -map 0:v -map 1:a \
  output.mp4
```

### Safe Combination Script

```python
import subprocess
import os

def combine_video_audio(video_path, audio_path, output_path):
    """Safely combine video and audio with duration check."""

    def get_duration(file_path):
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ], capture_output=True, text=True)
        return float(result.stdout.strip())

    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)

    print(f"Video: {video_dur:.1f}s")
    print(f"Audio: {audio_dur:.1f}s")

    # Check duration
    if video_dur < audio_dur:
        print(f"❌ ERROR: Video ({video_dur:.1f}s) < Audio ({audio_dur:.1f}s)")
        print("   Fix: Add more wait() at the end of your animation")
        return False

    if video_dur < audio_dur + 1.0:
        print(f"⚠️  WARNING: Video only {video_dur - audio_dur:.1f}s longer than audio")
        print("   Consider adding more end padding")

    # Combine
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v",
        "-map", "1:a",
        output_path
    ], check=True)

    print(f"✅ Created: {output_path}")
    return True
```

## Quick Checklist

Before rendering:
```
□ Last segment has self.wait(1.5) or more at the end
□ No FadeOut on the final frame (causes abrupt end)
□ Total TIMING values add up correctly
```

After rendering:
```
□ Video duration >= Audio duration + 1 second
□ Watch the last 5 seconds - does it end smoothly?
□ Audio doesn't cut off mid-word
```

## Common Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Audio cuts off | Video too short | Add `self.wait(2)` at end |
| Abrupt ending | No padding | Add final wait |
| Last word cut | Timing mismatch | Check last segment duration |
| Black screen at end | Too much padding | Reduce final wait |

## Template Pattern

```python
def seg_final(self):
    """Final segment with proper ending."""
    dur = self.dur("final_segment")

    # Your final content
    result = Text("Summary text", font_size=32)
    self.play(Write(result), run_time=1)

    # Content display time (dur - animations - padding)
    content_time = dur - 1 - 1.5
    self.wait(content_time)

    # Clean fadeout
    self.play(FadeOut(result), run_time=0.5)

    # REQUIRED: End padding
    self.wait(1.5)
```

---

## Part 2: Content Completion

### Animation Must Complete

```
❌ BAD: FadeOut starts but video ends mid-transition
❌ BAD: Text appears but viewer can't read it (too fast)
❌ BAD: Graph shows but no conclusion shown

✅ GOOD: Every animation runs to completion
✅ GOOD: Final message visible for 2+ seconds
✅ GOOD: Clean slate at the end (all FadeOut complete)
```

### Content Completion Checklist

```python
def verify_content_completion(scene_code: str) -> list:
    """Check for content completion issues."""
    issues = []

    # 1. Every segment must have complete animations
    # Check: play() should not be the last line of a segment

    # 2. Final segment must have fadeout
    if "seg_final" in scene_code or "seg_result" in scene_code:
        if "FadeOut" not in scene_code.split("seg_")[-1]:
            issues.append("Final segment missing FadeOut")

    # 3. Must end with wait(), not play()
    lines = scene_code.strip().split('\n')
    last_meaningful = [l for l in lines if l.strip() and not l.strip().startswith('#')]
    if last_meaningful and 'self.play' in last_meaningful[-1]:
        issues.append("Scene ends with play() - add wait() after")

    return issues
```

### Required Ending Pattern

Every video MUST end with:

```python
# 1. Final content display
self.play(Write(final_text), run_time=1)
self.wait(2)  # Let viewer read

# 2. Clean fadeout of ALL elements
self.play(
    FadeOut(all_elements),
    run_time=0.5
)

# 3. End padding (black screen)
self.wait(1.5)
```

### Content Timing Rules

| Element | Minimum Display Time |
|---------|---------------------|
| Title/Hook | 2 seconds |
| Key insight | 3 seconds |
| Final result | 2 seconds |
| Takeaway text | 3 seconds |
| Any text > 10 words | 4 seconds |

### Automated Content Check

```python
def check_content_completion(timing_dict: dict, segments: list) -> bool:
    """Verify all segments have enough time for content."""
    issues = []

    for seg in segments:
        seg_id = seg["id"]
        text = seg["text"]
        word_count = len(text.split())

        # Get segment duration
        if seg_id in timing_dict:
            dur = timing_dict[seg_id]["end"] - timing_dict[seg_id]["start"]
        else:
            issues.append(f"Missing timing for {seg_id}")
            continue

        # Check minimum duration for word count
        # Rule: ~150 words per minute = 2.5 words per second
        min_speech_time = word_count / 2.5
        min_total_time = min_speech_time + 0.5  # Add buffer

        if dur < min_total_time:
            issues.append(
                f"{seg_id}: {dur:.1f}s too short for {word_count} words "
                f"(need {min_total_time:.1f}s)"
            )

    if issues:
        print("❌ Content completion issues:")
        for issue in issues:
            print(f"   • {issue}")
        return False

    print("✅ Content completion check passed")
    return True
```

### Final Verification Script

```python
#!/usr/bin/env python3
"""verify_completion.py - Full completion check before combining."""

import subprocess
import json

def verify_all(video_path, audio_path, timing_path):
    """Run all completion checks."""

    print("=" * 50)
    print("VIDEO COMPLETION VERIFICATION")
    print("=" * 50)

    # 1. Duration check
    def get_duration(path):
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ], capture_output=True, text=True)
        return float(result.stdout.strip())

    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)

    print(f"\n📹 Video: {video_dur:.1f}s")
    print(f"🔊 Audio: {audio_dur:.1f}s")
    print(f"📏 Diff:  {video_dur - audio_dur:.1f}s")

    duration_ok = video_dur >= audio_dur + 1.0
    print(f"\n{'✅' if duration_ok else '❌'} Duration check: ", end="")
    print("PASS" if duration_ok else "FAIL - Video too short!")

    # 2. Content check (from timing file)
    with open(timing_path) as f:
        timing = json.load(f)

    last_seg = timing["segments"][-1]
    last_seg_dur = last_seg["end"] - last_seg["start"]

    content_ok = last_seg_dur >= 3.0  # Final segment needs 3+ seconds
    print(f"{'✅' if content_ok else '❌'} Final segment: ", end="")
    print(f"{last_seg_dur:.1f}s " + ("PASS" if content_ok else "FAIL - Too short!"))

    # 3. Overall
    print("\n" + "=" * 50)
    if duration_ok and content_ok:
        print("✅ ALL CHECKS PASSED - Safe to combine")
        return True
    else:
        print("❌ CHECKS FAILED - Fix issues before combining")
        return False

if __name__ == "__main__":
    import sys
    verify_all(sys.argv[1], sys.argv[2], sys.argv[3])
```

### Quick Mental Checklist

Before combining video + audio:

```
□ Watch last 10 seconds of rendered video
□ Is the final text/result visible long enough to read?
□ Does FadeOut complete before video ends?
□ Is there 1-2 seconds of black/empty at the very end?
□ Does the narration complete without cutting off?
```
