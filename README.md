# LVNG Cookbook

Ready-to-run examples for the [LVNG API](https://lvng.ai/docs) in cURL, TypeScript, Python, and Node.js.

## Quick Start

1. **Get an API key** from [Settings > Developer](https://app.lvng.ai/settings/developer)
2. **Set your key** as an environment variable:
   ```bash
   export LVNG_API_KEY="lvng_sk_live_..."
   ```
3. **Run any example** from the language folder of your choice

## Install Packages

```bash
# MCP Server (for Claude Code)
npm install -g https://api.lvng.ai/packages/lvng-mcp-server-1.0.0.tgz

# TypeScript SDK
npm install https://api.lvng.ai/packages/lvng-sdk-1.0.0.tgz
```

## Examples

| Recipe | cURL | TypeScript | Python | Node.js |
|--------|------|------------|--------|---------|
| Authenticate | [curl/](curl/) | [typescript/](typescript/) | [python/](python/) | [nodejs/](nodejs/) |
| List workflows | [curl/list-workflows.sh](curl/list-workflows.sh) | [typescript/list-workflows.ts](typescript/list-workflows.ts) | [python/list_workflows.py](python/list_workflows.py) | [nodejs/list-workflows.js](nodejs/list-workflows.js) |
| Execute workflow | [curl/execute-workflow.sh](curl/execute-workflow.sh) | [typescript/execute-workflow.ts](typescript/execute-workflow.ts) | [python/execute_workflow.py](python/execute_workflow.py) | [nodejs/execute-workflow.js](nodejs/execute-workflow.js) |
| Create agent | [curl/create-agent.sh](curl/create-agent.sh) | [typescript/create-agent.ts](typescript/create-agent.ts) | [python/create_agent.py](python/create_agent.py) | — |
| Message agent | [curl/message-agent.sh](curl/message-agent.sh) | [typescript/message-agent.ts](typescript/message-agent.ts) | [python/message_agent.py](python/message_agent.py) | — |
| Search knowledge | [curl/search-knowledge.sh](curl/search-knowledge.sh) | [typescript/search-knowledge.ts](typescript/search-knowledge.ts) | [python/search_knowledge.py](python/search_knowledge.py) | — |
| Stream chat (SSE) | [curl/stream-chat.sh](curl/stream-chat.sh) | [typescript/stream-chat.ts](typescript/stream-chat.ts) | [python/stream_chat.py](python/stream_chat.py) | — |
| Manage API keys | [curl/api-keys.sh](curl/api-keys.sh) | — | [python/api_keys.py](python/api_keys.py) | — |

## Claude Code Setup

```json
{
  "mcpServers": {
    "lvng": {
      "command": "lvng-mcp-server",
      "env": {
        "LVNG_API_KEY": "lvng_sk_live_..."
      }
    }
  }
}
```

## Documentation

- [API Reference](https://lvng.ai/docs/api)
- [Cookbook (web)](https://lvng.ai/docs/cookbook)
- [SDKs & Claude Code](https://lvng.ai/docs/sdks)
- [API Keys](https://lvng.ai/docs/api/api-keys)
- [OpenAPI Spec](https://lvng.ai/docs/openapi.json)

## License

MIT
