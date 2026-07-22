# Hermes Windows Native Screen Capture

Reusable Windows native screenshot skill for Hermes / Ai Ma Shi.

Default entrypoint:

```powershell
python H:\AI\skills\hermes-windows-native-screen-capture\scripts\capture_router.py
```

Default output:

```text
H:\AI\skills\hermes-windows-native-screen-capture\captures\wgc-latest.png
```

The router uses `windows-capture` / Windows Graphics Capture by default, then
runs white-screen analysis. It does not click, type, send messages, operate
accounts, or modify Hermes.

Run verification:

```powershell
python H:\AI\skills\hermes-windows-native-screen-capture\tests\verify_skill.py
python H:\AI\skills\hermes-windows-native-screen-capture\scripts\test_chrome_capture.py
```

