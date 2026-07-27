"""Perform a read-only handshake with the live Blender MCP bridge."""

from __future__ import annotations

import argparse
import json
import socket


READ_ONLY_PROBE = """import bpy
result = {
    "blender_version": bpy.app.version_string,
    "blend_file": bpy.data.filepath,
    "is_dirty": bpy.data.is_dirty,
    "scene": bpy.context.scene.name if bpy.context.scene else None,
    "object_count": len(bpy.data.objects),
    "material_count": len(bpy.data.materials),
    "image_count": len(bpy.data.images),
    "render_engine": bpy.context.scene.render.engine if bpy.context.scene else None,
}
"""


def receive_message(sock: socket.socket) -> dict[str, object]:
    payload = bytearray()
    while b"\0" not in payload:
        block = sock.recv(65536)
        if not block:
            break
        payload.extend(block)
    if not payload:
        raise ConnectionError("Blender returned no response")
    message = bytes(payload).partition(b"\0")[0]
    response = json.loads(message.decode("utf-8"))
    if not isinstance(response, dict):
        raise ConnectionError("Blender returned a non-object response")
    return response


def probe(host: str, port: int, timeout: float) -> dict[str, object]:
    request = json.dumps(
        {"type": "execute", "code": READ_ONLY_PROBE, "strict_json": True}
    ).encode("utf-8") + b"\0"
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        connection.sendall(request)
        return receive_message(connection)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read live Blender metadata without modifying the file"
    )
    parser.add_argument(
        "--host",
        choices=("localhost", "127.0.0.1"),
        default="127.0.0.1",
    )
    parser.add_argument("--port", type=int, default=9876)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    try:
        response = probe(args.host, args.port, args.timeout)
    except (ConnectionError, OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "unavailable", "error": str(error)}, indent=2))
        return 2
    print(json.dumps(response, indent=2, ensure_ascii=False))
    return 0 if response.get("status") == "ok" else 3


if __name__ == "__main__":
    raise SystemExit(main())
