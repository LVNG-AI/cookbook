#!/bin/bash
# Create a new AI agent
curl -s -X POST https://api.lvng.ai/api/v2/agents \
  -H "x-api-key: ${LVNG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Research Assistant",
    "system_prompt": "You are a helpful research assistant.",
    "model": "claude-sonnet-4-6",
    "tools": ["web_search", "knowledge_search"]
  }' | jq .
