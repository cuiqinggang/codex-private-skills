# Verification Result

Status: PASS

## Checks

- router_exit_0: True
- router_ok: True
- analysis_exit_0: True
- analysis_ok: True
- png_exists: True
- not_white_screen: True

## Capture

- Path: H:\AI\skills\hermes-windows-native-screen-capture\captures\wgc-latest.png
- Width: 3840
- Height: 2160
- File size: 3827850
- Suspected white screen: False

## Commands

```text
C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe H:\AI\skills\hermes-windows-native-screen-capture\scripts\capture_router.py --out H:\AI\skills\hermes-windows-native-screen-capture\captures\wgc-latest.png
C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe H:\AI\skills\hermes-windows-native-screen-capture\scripts\analyze_capture.py H:\AI\skills\hermes-windows-native-screen-capture\captures\wgc-latest.png --report H:\AI\skills\hermes-windows-native-screen-capture\reports\verification-analysis.json
```

## Router JSON

```json
{
  "ok": true,
  "backend": "windows-capture",
  "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\wgc-latest.png",
  "analysis": {
    "ok": true,
    "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\wgc-latest.png",
    "exists": true,
    "width": 3840,
    "height": 2160,
    "file_size": 3827850,
    "mean_brightness": 75.82042510609568,
    "white_pixel_ratio": 0.03664846161265432,
    "non_white_pixel_ratio": 0.9633515383873457,
    "suspected_white_screen": false,
    "suspected_failure": false,
    "failure_reasons": []
  },
  "error": null,
  "capture": {
    "ok": true,
    "backend": "windows-capture",
    "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\wgc-latest.png",
    "width": 3840,
    "height": 2160,
    "file_size": 3827850,
    "duration_ms": 5836,
    "requested_monitor_index": 0,
    "effective_monitor_index": 1,
    "error": null
  }
}
```

## Analysis JSON

```json
{
  "ok": true,
  "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\wgc-latest.png",
  "exists": true,
  "width": 3840,
  "height": 2160,
  "file_size": 3827850,
  "mean_brightness": 75.82042510609568,
  "white_pixel_ratio": 0.03664846161265432,
  "non_white_pixel_ratio": 0.9633515383873457,
  "suspected_white_screen": false,
  "suspected_failure": false,
  "failure_reasons": []
}
```
