"""MCP server for Context Window Semantic Compression & Salience Pruner."""
import sys
import json
from client import ContextWindowSaliencePruner

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "prune_context_window",
                "description": "Prunes low-salience messages to fit within a target token budget",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "messages": {"type": "array"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["messages"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "prune_context_window":
            args = params.get("arguments", {})
            res = ContextWindowSaliencePruner.prune_context(
                args.get("messages", []),
                int(args.get("max_tokens", 1000))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
