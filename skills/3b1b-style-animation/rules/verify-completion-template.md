---
name: verify-completion-template
description: Template code for video completion verification
metadata:
  tags: template, verification, audio, video
priority: high
---

# Completion Verification Template

Copy this into your project to verify video completion.

## verify_completion.py

```python
#!/usr/bin/env python3
"""
verify_completion.py - Verify video/audio completion before combining.

Usage:
    python verify_completion.py video.mp4 audio.mp3 timing.json
"""

import subprocess
import json
import sys


def get_duration(file_path: str) -> float:
    """Get media file duration in seconds."""
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())


def verify_duration(video_path: str, audio_path: str) -> tuple[bool, str]:
    """Check video is longer than audio."""
    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)
    diff = video_dur - audio_dur

    status = {
        "video": video_dur,
        "audio": audio_dur,
        "diff": diff
    }

    if diff < 0:
        return False, f"❌ Video too short by {-diff:.1f}s", status
    elif diff < 1.0:
        return True, f"⚠️  Only {diff:.1f}s padding (recommend 1.5s+)", status
    else:
        return True, f"✅ {diff:.1f}s padding", status


def verify_content(timing_path: str) -> tuple[bool, str]:
    """Check content timing is adequate."""
    with open(timing_path) as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        return False, "❌ No segments found"

    issues = []

    # Check final segment
    last = segments[-1]
    last_dur = last["end"] - last["start"]
    if last_dur < 3.0:
        issues.append(f"Final segment too short: {last_dur:.1f}s (need 3s+)")

    # Check all segments have minimum time for content
    for seg in segments:
        text = seg.get("text", "")
        words = len(text.split())
        dur = seg["end"] - seg["start"]
        min_time = words / 2.5 + 0.3  # 2.5 words/sec + buffer

        if dur < min_time:
            issues.append(f"{seg['id']}: {dur:.1f}s < {min_time:.1f}s needed")

    if issues:
        return False, "❌ " + "; ".join(issues[:3])  # Show first 3

    return True, "✅ All segments have adequate time"


def combine_safe(video_path: str, audio_path: str, output_path: str) -> bool:
    """Combine video and audio only if verification passes."""

    # Don't use -shortest, let video determine length
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v",
        "-map", "1:a",
        output_path
    ], capture_output=True)

    return result.returncode == 0


def main():
    if len(sys.argv) < 4:
        print("Usage: python verify_completion.py video.mp4 audio.mp3 timing.json")
        sys.exit(1)

    video_path = sys.argv[1]
    audio_path = sys.argv[2]
    timing_path = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) > 4 else "output.mp4"

    print("=" * 50)
    print("VIDEO COMPLETION VERIFICATION")
    print("=" * 50)

    # Duration check
    dur_ok, dur_msg, dur_stats = verify_duration(video_path, audio_path)
    print(f"\n📹 Video: {dur_stats['video']:.1f}s")
    print(f"🔊 Audio: {dur_stats['audio']:.1f}s")
    print(f"📏 {dur_msg}")

    # Content check
    content_ok, content_msg = verify_content(timing_path)
    print(f"📝 {content_msg}")

    print("\n" + "=" * 50)

    if dur_ok and content_ok:
        print("✅ ALL CHECKS PASSED")
        if combine_safe(video_path, audio_path, output_path):
            print(f"✅ Created: {output_path}")
            return 0
    else:
        print("❌ VERIFICATION FAILED")
        if not dur_ok:
            print("   → Add self.wait() at end of animation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## Usage in Animation Workflow

```python
# In your audio script
async def generate_audio(output_dir="audio"):
    # ... generate audio ...

    # Save timing for verification
    with open(f"{output_dir}/timing.json", "w") as f:
        json.dump({"total": total, "segments": timing}, f, indent=2)
```

```bash
# After rendering
python verify_completion.py \
    media/videos/Scene/1080p60/Scene.mp4 \
    audio/full.mp3 \
    audio/timing.json \
    final_output.mp4
```

## Integration Pattern

Add to your animation file:

```python
class MyScene(Scene):
    # Audio duration from generation
    AUDIO_DURATION = 50.0

    def construct(self):
        self.seg_01()
        self.seg_02()
        # ...
        self.seg_final()

        # ALWAYS: End with verification padding
        self._ensure_completion()

    def _ensure_completion(self):
        """Ensure video is complete."""
        # Minimum 1.5s padding at end
        self.wait(1.5)
```
