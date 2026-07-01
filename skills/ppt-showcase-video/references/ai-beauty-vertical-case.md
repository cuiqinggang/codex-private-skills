# AI 美女集合竖屏大图案例

This case records the accepted 2026-06-07 workflow for a Douyin / WeChat Moments image showcase video.

## User Feedback That Defined The Final Version

- Horizontal 16:9 video inside Douyin looked wrong: the phone editor showed a wide strip and the image became too small.
- The accepted version must be vertical 9:16 and image-first.
- The user liked the final vertical big-image result.
- Music should stay as light music, not urgent, not generated, not bird/environment sounds.

## Accepted Output

```text
C:\Users\A\Desktop\AI美女集合_PPT展示视频_竖屏大图轻音乐版.mp4
```

Verified properties:

```text
video: h264, 1080x1920, 30 fps
audio: aac, stereo
duration: 27.8s
mean_volume: -32.2 dB
max_volume: -14.3 dB
```

## Source Images

Original image folder used:

```text
C:\Users\A\Desktop\4\AI美女集合
```

The folder contained 8 PNG images. Most were portrait `941x1672`; one was square `1254x1254`; one was `1122x1402`.

## Layout Parameters

```text
canvas: 1080x1920
portrait image max box: 1060x1888
non-portrait image max box: 1060x1620
background: cover-fit source image, Gaussian blur 30, brightness 0.62, color 0.86
foreground: centered
edge: 4 px off-white border
shadow: soft shadow behind foreground
seconds per slide: 4.0
fade seconds: 0.6
fps: 30
video codec: libx264
crf: 18
pixel format: yuv420p
```

## Accepted Music

Bundled asset:

```text
assets/calm-piano-background-music-free-orange-free-sounds.mp3
```

Source:

```text
https://orangefreesounds.com/calm-piano-background-music-free/
```

The accepted version reused this music with volume reduced to background level.

## Avoided Versions

- Self-synthesized chord/tone music: rejected as simple and unpleasant.
- Kevin MacLeod Upbeat Forever: rejected as too urgent/tension-building.
- Gentle Lo-Fi / Cookies: rejected because the opening felt like bird-like chirping or did not match.
- Horizontal 1920x1080 layout: rejected for Douyin/WeChat because the image appears small in a vertical editor.

