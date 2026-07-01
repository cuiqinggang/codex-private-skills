# Chrome Capture Test

PASS: True

This test does not open a new browser. It captures the current Windows desktop, including any currently open Chrome window, through capture_router.py.

## Result

- Screenshot path: H:\AI\skills\hermes-windows-native-screen-capture\captures\chrome-capture-test.png
- Dimensions: 3840x2160
- File size: 3827850 bytes
- Suspected white screen: False
- White pixel ratio: 0.03664846161265432
- Can be Hermes default screenshot channel: True

## Raw Router JSON

```json
{
  "ok": true,
  "backend": "windows-capture",
  "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\chrome-capture-test.png",
  "analysis": {
    "ok": true,
    "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\chrome-capture-test.png",
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
    "image_path": "H:\\AI\\skills\\hermes-windows-native-screen-capture\\captures\\chrome-capture-test.png",
    "width": 3840,
    "height": 2160,
    "file_size": 3827850,
    "duration_ms": 3370,
    "requested_monitor_index": 0,
    "effective_monitor_index": 1,
    "error": null
  }
}
```
