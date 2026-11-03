"""Reuse the configured Windows MCP stdio server without changing its config."""
import argparse
import asyncio
import base64
import io
import json
import os
from pathlib import Path
import sys
import tomllib


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path.home() / ".codex" / "config.toml")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-tools", action="store_true")
    group.add_argument("--tool")
    group.add_argument("--interactive", action="store_true")
    parser.add_argument("--arguments", default="{}", help="JSON object for --tool")
    parser.add_argument("--server-cwd", type=Path, help="Existing Windows server working directory")
    parser.add_argument("--image-max-width", type=int, default=1280,
                        help="Resize returned images for transport; 0 preserves full size")
    return parser.parse_args()


def server_parameters(config_path, cwd_override=None):
    from mcp import StdioServerParameters
    with config_path.open("rb") as handle:
        config = tomllib.load(handle)
    entry = config.get("mcp_servers", {}).get("windows-mcp-v1")
    if not entry:
        raise ValueError("windows-mcp-v1 is not configured")
    if entry.get("enabled") is False:
        raise ValueError("windows-mcp-v1 is disabled; do not enable automatically")
    command = entry.get("command")
    if not command or entry.get("url"):
        raise ValueError("This adapter requires the existing stdio command")
    if not Path(command).is_file():
        raise FileNotFoundError("Configured executable does not exist")
    environment = dict(os.environ)
    environment.update(entry.get("env", {}))
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONUTF8"] = "1"
    executable = Path(command).resolve()
    cwd = cwd_override or (executable.parents[2] if executable.parent.name.lower() == "scripts"
                           and executable.parent.parent.name == ".venv" else executable.parent)
    if not cwd.is_dir():
        raise NotADirectoryError("Server working directory does not exist")
    params = StdioServerParameters(command=command, args=entry.get("args", []),
                                  env=environment,
                                  cwd=str(cwd))
    return (params, entry.get("enabled_tools"), set(entry.get("disabled_tools", [])),
            float(entry.get("startup_timeout_sec", 45)))


def authorize_tool(name, allowed, denied):
    if name in denied or (allowed is not None and name not in allowed):
        raise ValueError("Tool is disabled in the existing client configuration: " + name)


def tool_failed(result):
    data = result.model_dump(mode="json", by_alias=True)
    return bool(data.get("isError", data.get("is_error", False)))


def emit(result, max_width):
    obj = result.model_dump(mode="json", by_alias=True)
    content = []
    for block in obj.get("content", []):
        if block.get("type") == "image" and max_width > 0:
            from PIL import Image
            image = Image.open(io.BytesIO(base64.b64decode(block["data"]))).convert("RGB")
            original = image.size
            if image.width > max_width:
                image.thumbnail((max_width, max_width * 3))
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=55)
            block["data"] = base64.b64encode(output.getvalue()).decode("ascii")
            block["mimeType"] = "image/jpeg"
            content.append({"type": "text", "text":
                "Adapter image dimensions: server-returned=%s, emitted=%s. "
                "Use screenshot original dimensions and region origin to compute physical "
                "desktop coordinates; do not use emitted image pixels directly."
                % (original, image.size)})
        content.append(block)
    if "content" in obj:
        obj["content"] = content
    print("MCP_RESULT=" + json.dumps(obj, ensure_ascii=True), flush=True)


async def run(args):
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client
    params, allowed, denied, startup_timeout = server_parameters(args.config, args.server_cwd)
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await asyncio.wait_for(session.initialize(), timeout=startup_timeout)
            if args.list_tools:
                result = await session.list_tools()
                result.tools = [tool for tool in result.tools
                                if tool.name not in denied
                                and (allowed is None or tool.name in allowed)]
                emit(result, args.image_max_width)
                return 0
            if args.tool:
                authorize_tool(args.tool, allowed, denied)
                arguments = json.loads(args.arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("--arguments must contain a JSON object")
                result = await session.call_tool(args.tool, arguments)
                emit(result, args.image_max_width)
                return 1 if tool_failed(result) else 0
            print("MCP_READY", flush=True)
            successful = errors = requests = 0
            while True:
                line = await asyncio.to_thread(sys.stdin.readline)
                if not line or line.strip() == "EXIT":
                    print("MCP_SESSION_SUMMARY=" + json.dumps(
                        {"requests": requests, "successful": successful, "errors": errors}),
                        flush=True)
                    return 1 if errors else (0 if successful else 2)
                requests += 1
                try:
                    request = json.loads(line)
                    if not isinstance(request, dict):
                        raise ValueError("Request must be a JSON object")
                    name = request.get("name")
                    arguments = request.get("arguments", {})
                    if not isinstance(name, str) or not isinstance(arguments, dict):
                        raise ValueError("name must be text; arguments must be an object")
                    authorize_tool(name, allowed, denied)
                    result = await session.call_tool(name, arguments)
                    emit(result, args.image_max_width)
                    if tool_failed(result):
                        errors += 1
                    else:
                        successful += 1
                except Exception as error:
                    errors += 1
                    print("MCP_ERROR=" + json.dumps(str(error), ensure_ascii=True), flush=True)


def main():
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="strict")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    args = parse_args()
    if args.image_max_width < 0:
        raise SystemExit("--image-max-width must be non-negative")
    try:
        return asyncio.run(run(args))
    except Exception as error:
        import traceback
        traceback.print_exception(error)
        print("MCP_ERROR=" + json.dumps(str(error), ensure_ascii=True), file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
