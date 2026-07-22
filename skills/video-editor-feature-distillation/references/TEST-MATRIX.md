# Test Matrix

## Install And Launch

| Test | Evidence |
|---|---|
| App installed | winget list or registry uninstall entry |
| Executable found | full path |
| Can launch | process starts or GUI screenshot when available |
| Version recorded | winget/registry/app about page |

## Functional Tests

| Feature | Minimal Test |
|---|---|
| Import video | open a small generated MP4 |
| Export MP4 | export H.264/AAC if GUI route is used |
| Auto subtitles | create SRT from test audio or verify built-in speech-to-text |
| Trim/join | produce a shorter or joined clip |
| Background music | mix a sine/music sample below voice |
| Scene split | create scene list/contact sheet |
| Vertical output | produce 1080x1920 H.264/AAC/yuv420p |
| Cover | extract one representative frame |

## Decision Criteria

- Direct-use when the GUI feature is free, stable, and faster than scripting.
- Script-distill when output can be reproduced with commands and verified.
- Hybrid when GUI improves creative review but scripts should do bulk work.
- Do-not-copy when the value depends on proprietary assets, paid templates,
  account-gated AI, or unclear licensing.

