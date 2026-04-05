#!/usr/bin/env python3
"""
mcp_server.py — Implica Wiki MCP Server

Exposes wiki operations to Giancarlo via the Model Context Protocol.
Runs as a standalone MCP server that Giancarlo can connect to.

Usage:
  ./scripts/mcp_server.py [--port 8765]

Or via stdio (for MCP SDK):
  ./scripts/mcp_server.py --stdio
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path(__file__).parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"

# ─── MCP Protocol Helpers ─────────────────────────────────────────────────────

def json_response(result, error=None):
    """Build a JSON-RPC response"""
    if error:
        return json.dumps({"jsonrpc": "2.0", "error": error, "id": None})
    return json.dumps({"jsonrpc": "2.0", "result": result, "id": None})

def read_page(name):
    """Read a wiki page by name (without extension)"""
    # Try different subdirectories
    for subdir in ["", "entities/", "topics/", "syntheses/", "comparisons/", "source-summaries/"]:
        path = WIKI_DIR / subdir / f"{name}.md"
        if path.exists():
            return path.read_text(errors="replace")
    # Try exact filename
    path = WIKI_DIR / name
    if path.exists():
        return path.read_text(errors="replace")
    return None

def list_pages():
    """List all wiki pages"""
    pages = []
    for md in WIKI_DIR.rglob("*.md"):
        if md.name in ["index.md", "log.md"]:
            continue
        rel = str(md.relative_to(WIKI_DIR))
        pages.append({
            "name": md.stem,
            "path": rel,
            "type": md.parent.name if md.parent != WIKI_DIR else "root"
        })
    return pages

def wiki_status():
    """Get wiki statistics"""
    pages = list(list_pages())
    sources = list((WIKI_ROOT / "raw").glob("*"))
    sources = [s for s in sources if s.name != "sources.md"]

    log_path = WIKI_DIR / "log.md"
    log_lines = 0
    if log_path.exists():
        log_lines = len(log_path.read_text(errors="replace").splitlines())

    return {
        "total_pages": len(pages),
        "total_sources": len(sources),
        "log_entries": log_lines,
        "pages_by_type": {
            "entities": len([p for p in pages if p["type"] == "entities"]),
            "topics": len([p for p in pages if p["type"] == "topics"]),
            "syntheses": len([p for p in pages if p["type"] == "syntheses"]),
            "comparisons": len([p for p in pages if p["type"] == "comparisons"]),
            "source-summaries": len([p for p in pages if p["type"] == "source-summaries"]),
        }
    }

def search_wiki(query, max_results=10):
    """Search wiki pages using grep fallback"""
    terms = query.lower().split()
    results = []

    for md in WIKI_DIR.rglob("*.md"):
        if md.name in ["index.md", "log.md"]:
            continue
        content = md.read_text(errors="replace")
        content_lower = content.lower()
        score = sum(1 for term in terms if term in content_lower)
        if score > 0:
            # Find first matching line
            preview = ""
            for line in content.splitlines():
                if any(term in line.lower() for term in terms):
                    preview = line.strip()[:150]
                    break
            results.append({
                "page": md.stem,
                "path": str(md.relative_to(WIKI_ROOT)),
                "score": score,
                "preview": preview
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]

# ─── MCP Tools ───────────────────────────────────────────────────────────────

TOOLS = {
    "wiki_status": {
        "description": "Get wiki statistics and status",
        "input": {},
        "handler": lambda _: wiki_status()
    },
    "wiki_list": {
        "description": "List all wiki pages",
        "input": {},
        "handler": lambda _: list_pages()
    },
    "wiki_read": {
        "description": "Read a wiki page by name",
        "input": {"name": "str"},
        "handler": lambda args: {"content": read_page(args["name"]) or "Page not found"}
    },
    "wiki_search": {
        "description": "Search wiki pages",
        "input": {"query": "str", "max_results": "int?"},
        "handler": lambda args: search_wiki(args["query"], args.get("max_results", 10))
    },
    "wiki_log": {
        "description": "Read the wiki log",
        "input": {},
        "handler": lambda _: {"content": (WIKI_DIR / "log.md").read_text(errors="replace")}
    },
}

# ─── MCP Protocol (JSON-RPC 2.0 over stdio) ──────────────────────────────────

def handle_request(data):
    """Handle incoming JSON-RPC request"""
    if not isinstance(data, dict):
        return json_response(None, {"code": -32700, "message": "Parse error"})

    method = data.get("method", "")
    params = data.get("params", {})
    id_ = data.get("id")

    if method == "tools/list":
        tools_list = []
        for name, tool in TOOLS.items():
            tools_list.append({
                "name": name,
                "description": tool["description"],
                "input_schema": {
                    "type": "object",
                    "properties": {k: {"type": v} for k, v in tool["input"].items()},
                    "required": [k for k, v in tool["input"].items() if "?" not in v]
                }
            })
        return json_response({"tools": tools_list})

    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})

        if tool_name not in TOOLS:
            return json.dumps({"jsonrpc": "2.0", "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}, "id": id_})

        try:
            result = TOOLS[tool_name]["handler"](tool_args)
            return json.dumps({"jsonrpc": "2.0", "result": {"content": result}, "id": id_})
        except Exception as e:
            return json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": id_})

    elif method == "ping":
        return json_response({"pong": True})

    else:
        return json_response(None, {"code": -32601, "message": f"Method not found: {method}"})

def main():
    if "--stdio" in sys.argv:
        # MCP over stdio
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                response = handle_request(data)
                if response:
                    print(response, flush=True)
            except json.JSONDecodeError:
                print(json_response(None, {"code": -32700, "message": "Parse error"}), flush=True)
    else:
        # HTTP server mode
        import http.server
        import socketserver
        PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                try:
                    data = json.loads(body)
                    response = handle_request(data)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(response.encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())

            def do_GET(self):
                if self.path == "/health":
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK")
                else:
                    self.send_response(404)
                    self.end_headers()

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Implica MCP server running on port {PORT}", file=sys.stderr)
            httpd.serve_forever()

if __name__ == "__main__":
    main()
