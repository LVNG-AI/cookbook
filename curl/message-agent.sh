#!/bin/bash
# Send a message to a running agent
# Usage: ./message-agent.sh <agent_id> "your message"
AGENT_ID="${1:?Usage: ./message-agent.sh <agent_id> \"message\"}"
MESSAGE="${2:?Provide a message as second argument}"

curl -s -X POST "https://api.lvng.ai/api/v2/agents/${AGENT_ID}/message" \
  -H "x-api-key: ${LVNG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"${MESSAGE}\"}" | jq .
