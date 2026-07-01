# 834 Safety Policy

## Must Preserve

- Windows system directories.
- Proxy/network tools.
- Codex configuration, workspaces, skills, and reports.
- Browser login/profile data.
- Open WebUI active volume.
- ComfyUI models, controlnet, custom nodes, workflows, input, and output.
- Desktop `4` model files.

## Allowed Cleanup Only With Logs

- Explicit old installer archives.
- Browser cache subfolders.
- pip/npm/uv/temp caches.
- Docker unused images, stopped containers, build cache, unused networks.
- Docker unused volumes only after recording Open WebUI mounts and only when user explicitly permits it.
- Hibernation only via `powercfg /h off`.

## Stop Conditions

Stop and report instead of deleting when:

- A path contains secrets, user media, project outputs, skills, reports, models, databases, or unknown app data.
- Docker is unhealthy before cleanup.
- Open WebUI active volume cannot be identified.
- A command needs admin permission and cannot run.
