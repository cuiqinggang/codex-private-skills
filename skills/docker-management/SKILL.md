---
name: docker-management
description: Use when this Windows Codex studio needs Docker Desktop, containers, images, volumes, networks, Compose, Dockerfile, or cleanup guidance. Use for local Windows Docker diagnosis, New API/Hermes-adjacent stacks, project-local Compose verification, and safe cleanup planning with manifest-first Stop Gates for destructive actions.
---

# Docker Management Windows Studio

Use this skill for Docker Desktop operations on this Windows machine.

## Windows Studio Rules

- Use PowerShell and Docker Desktop compatible commands.
- Diagnose before changing state.
- Run Compose commands from the directory containing the Compose file.
- Preserve logs before restart or repair.
- Never delete containers, images, volumes, networks, bind-mounted data, databases, or caches without a reviewed manifest and explicit approval.
- Do not change Hermes/Open WebUI/New API ports unless the active task explicitly requires it.

## Workflow

1. Check availability: `docker version`, `docker context ls`, `docker compose version`.
2. Inspect state: `docker ps -a`, `docker images`, `docker volume ls`, `docker network ls`.
3. For a project stack, locate the Compose file and run `docker compose ps`.
4. Collect logs before changes: `docker logs <name>` or `docker compose logs --tail 200`.
5. Make the smallest repair: restart one service, rebuild one image, or update one config only when needed.
6. Verify with the narrowest health check, local HTTP endpoint, or container command.

## Cleanup Gate

For cleanup, first produce a manifest listing exact objects and why they are safe to remove. Stop before deletion.

## Verification

- PASS: command exit code is 0, logs are preserved, and service health is rechecked.
- FAIL: Docker unavailable, Compose file unclear, data volume risk, or destructive action lacks a manifest.

