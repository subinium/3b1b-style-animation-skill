---
name: narration
description: Adding narration scripts and TTS audio to animations
metadata:
  tags: narration, tts, audio, voice, script
priority: medium
---

# Narration and TTS Integration

Add professional-sounding narration to your math animations using free TTS services.

## Free TTS Options

| Library | Quality | Language | Offline | Install |
|---------|---------|----------|---------|---------|
| **edge-tts** | ⭐⭐⭐⭐⭐ | Multi | ❌ | `pip install edge-tts` |
| **gTTS** | ⭐⭐⭐ | Multi | ❌ | `pip install gTTS` |
| **pyttsx3** | ⭐⭐ | System | ✅ | `pip install pyttsx3` |

**Recommended: edge-tts** - Microsoft Edge TTS engine, free with natural-sounding voices

## Quick Start

```bash
pip install edge-tts manim
```

```python
# 1. Write script
script = [
    (0, "Let's learn about Dijkstra's algorithm."),
    (3, "This algorithm finds the shortest path."),
    ...
]

# 2. Generate TTS
# edge-tts --voice en-US-GuyNeural --text "Hello" --write-media output.mp3

# 3. Add audio in Manim
self.add_sound("narration.mp3")
```

## Script Structure

### Timed Script Format

```python
# (start_time_seconds, dialogue)
SCRIPT = [
    (0.0, "Dijkstra's algorithm finds the shortest path in a graph."),
    (4.0, "The key idea is simple."),
    (6.5, "Always pick the closest unvisited node."),
    (10.0, "This greedy choice is surprisingly always optimal."),
    ...
]
```

### Scene-Synced Script

```python
class NarratedScene(Scene):
    def construct(self):
        # 대본과 애니메이션을 함께 정의
        self.narrate_and_animate(
            text="이것은 단위 정사각형입니다.",
            animation=Create(square),
            duration=2.0
        )
```

## Edge-TTS Usage

### Available Korean Voices

```bash
# 음성 목록 확인
edge-tts --list-voices | grep ko-KR
```

| Voice | 성별 | 스타일 |
|-------|-----|-------|
| `ko-KR-SunHiNeural` | 여성 | 자연스러움 |
| `ko-KR-InJoonNeural` | 남성 | 차분함 |
| `ko-KR-HyunsuNeural` | 남성 | 명확함 |

### English Voices

| Voice | Style |
|-------|-------|
| `en-US-GuyNeural` | Male, natural |
| `en-US-JennyNeural` | Female, friendly |
| `en-GB-RyanNeural` | British male |

### Generate Audio

```bash
# 단일 문장
edge-tts --voice ko-KR-SunHiNeural --text "안녕하세요" --write-media hello.mp3

# 파일에서
edge-tts --voice ko-KR-SunHiNeural --file script.txt --write-media narration.mp3

# 속도 조절
edge-tts --voice ko-KR-SunHiNeural --rate="-10%" --text "천천히 말하기" --write-media slow.mp3
```

## Python Integration

### Full Pipeline

```python
import edge_tts
import asyncio
from manim import *

class NarratedAnimation(Scene):
    """Animation with TTS narration."""

    # 대본 정의
    SCRIPT = [
        {"time": 0, "text": "다익스트라 알고리즘을 시각화해보겠습니다.", "duration": 3},
        {"time": 3, "text": "먼저 그래프를 만들어봅시다.", "duration": 2},
        {"time": 5, "text": "각 노드는 도시를, 엣지는 도로를 나타냅니다.", "duration": 3},
    ]

    async def generate_audio(self):
        """Generate TTS audio for all script segments."""
        voice = "ko-KR-SunHiNeural"

        for i, segment in enumerate(self.SCRIPT):
            communicate = edge_tts.Communicate(segment["text"], voice)
            await communicate.save(f"audio_{i}.mp3")

    def construct(self):
        # 사전에 오디오 생성 필요 (별도 스크립트로)
        # asyncio.run(self.generate_audio())

        # 애니메이션 시작
        # ... your animation code ...

        # 오디오 추가 (각 시점에)
        self.add_sound("audio_0.mp3", time_offset=0)
        self.add_sound("audio_1.mp3", time_offset=3)
        self.add_sound("audio_2.mp3", time_offset=5)
```

### Standalone Audio Generator

```python
#!/usr/bin/env python3
"""
generate_narration.py - Generate TTS audio from script
Usage: python generate_narration.py script.json output_dir/
"""

import edge_tts
import asyncio
import json
import sys

async def generate_all(script_file, output_dir, voice="ko-KR-SunHiNeural"):
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)

    for i, segment in enumerate(script):
        output_path = f"{output_dir}/segment_{i:03d}.mp3"
        communicate = edge_tts.Communicate(segment["text"], voice)
        await communicate.save(output_path)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_all(sys.argv[1], sys.argv[2]))
```

## Script Writing Guidelines

### Pacing

```python
# 읽기 속도: 약 150 단어/분 (영어), 300 음절/분 (한국어)

# 대략적인 시간 계산
def estimate_duration(text, language="ko"):
    if language == "ko":
        # 한국어: 약 5-6 음절/초
        return len(text) / 5.5
    else:
        # 영어: 약 2.5 단어/초
        words = len(text.split())
        return words / 2.5
```

### Sync with Animation

```python
# ❌ BAD: 대사와 애니메이션 불일치
self.play(Create(circle))  # 1초
# 대사: "원을 만들고 이동시켜봅시다" (3초 분량)

# ✅ GOOD: 대사 길이에 맞춤
self.play(Create(circle), run_time=1.5)  # "원을 만들어봅시다" (1.5초)
self.play(circle.animate.shift(RIGHT), run_time=1.5)  # "오른쪽으로 이동합니다" (1.5초)
```

### Natural Language

```python
# ❌ BAD: 기술적/딱딱한 표현
"행렬 A와 벡터 v의 곱을 계산합니다."

# ✅ GOOD: 자연스러운 설명
"이 행렬이 벡터에 어떤 영향을 주는지 봅시다."
```

## Combining Audio with Video

### Using Manim's add_sound

```python
class WithNarration(Scene):
    def construct(self):
        # 시작할 때 전체 나레이션 추가
        self.add_sound("full_narration.mp3")

        # 또는 특정 시점에 추가
        self.add_sound("intro.mp3", time_offset=0)
        self.play(Create(title))

        self.add_sound("main.mp3", time_offset=3)
        self.play(Create(content))
```

### Using FFmpeg (Post-processing)

```bash
# 비디오와 오디오 결합
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# 볼륨 조절
ffmpeg -i video.mp4 -i narration.mp3 -filter:a "volume=1.5" -c:v copy output.mp4

# 배경 음악 + 나레이션 믹싱
ffmpeg -i video.mp4 -i narration.mp3 -i bgm.mp3 \
  -filter_complex "[1:a]volume=1.0[narr];[2:a]volume=0.2[bgm];[narr][bgm]amix=inputs=2[a]" \
  -map 0:v -map "[a]" output.mp4
```

## Complete Example Workflow

```bash
# 1. 대본 작성 (script.json)
cat > script.json << 'EOF'
[
  {"time": 0, "text": "다익스트라 알고리즘에 대해 알아보겠습니다."},
  {"time": 3, "text": "이 알고리즘은 그래프에서 최단 경로를 찾습니다."},
  {"time": 6, "text": "핵심은 가장 가까운 노드를 선택하는 것입니다."}
]
EOF

# 2. TTS 생성
python generate_narration.py script.json audio/

# 3. 오디오 파일들 합치기
ffmpeg -f concat -i audio_list.txt -c copy full_narration.mp3

# 4. Manim 렌더링
manim -pqh scene.py MyScene

# 5. 비디오 + 오디오 결합
ffmpeg -i media/videos/.../MyScene.mp4 -i full_narration.mp3 -c:v copy final.mp4
```
