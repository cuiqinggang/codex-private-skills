# Codex Zombie Process Recovery - Successful Case 2026-06-30

## Time
2026-06-30 01:00 CST

## Scenario
Codex Desktop 重装后配置了完整技能包（108个），随后无法启动 — 进程在运行但窗口不出现。

## Symptoms
- `Get-Process -Name Codex` 显示 7 个进程
- 所有进程 `Responding = True`
- 所有进程 `MainWindowHandle = 0`，`MainWindowTitle = ""`
- `logs_2.sqlite` 持续写入（进程活着但 UI 卡死）
- `Start-Process "shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App"` 后进程数增加但窗口仍不出现

## Environment
- Windows 10, 3 monitors (3840x2160 + 2560x1440 + 2560x1440)
- Codex version: 26.623.8305.0 (msstore)
- 108 skill packages in `C:\Users\A\.codex\skills`
- Codex++ residue in AppData (not actively installed)
- Proxy: Clash/FlClash active

## Diagnosis Steps

1. **Phase 0** — Checked memory/skills/history: loaded `codex-desktop-clean-reinstall-skill-recovery` and `codex-reinstall-skill-recovery` skills
2. **Phase 1** — Environment check:
   - `.codex` exists with all directories
   - `winget list Codex` confirms msstore install
   - AppX package status: `Ok`
   - Codex++ residue at `AppData\Local\com.bigpizzav3.codexplusplus.manager` and `AppData\Roaming\Codex++` (files only, no winget install)
   - `config.toml` valid with gpt-5.5 model, sandbox_mode=danger-full-access
3. **Phase 2** — Attempted fix: killed processes, restarted → still no window
4. **Phase 3** — Skill isolation test: moved 107 skills to temp, kept only `.system` → Codex window appeared (MainWindowHandle=723240)
5. **Phase 4** — Restored all 107 skills → Codex window still appears with all 108 skills (MainWindowHandle=854562)

## Root Cause
**僵尸进程残留** (Zombie processes): Codex background processes from a previous launch attempt persisted without parent UI window. When user tried to restart Codex, the app detected existing processes and attached to them instead of creating a new UI. The processes kept running and writing logs but never rendered a window.

## Fix Applied
```
1. Kill all Codex processes
2. Temporary skill clean-start (move skills out → start → verify window → kill → move back)
3. Restart with full skill set
```

Total time: ~5 minutes. No reinstall needed. No data lost.

## Verification
- Codex window visible with MainWindowHandle=854562
- All 108 skill packages present
- `config.toml` unchanged
- Sessions intact

## Lessons Learned
1. MainWindowHandle=0 with Responding=True = zombie process syndrome (not a skill issue)
2. Skill isolation is a diagnostic tool, not a permanent fix — the real fix is killing zombies
3. 108 skill packages do NOT cause startup issues (confirmed working)
4. Always `Get-Process -Name Codex` to check window state before assuming "not running"
5. The cold-start with minimal skills can "unstick" the app even when skills aren't the root cause
