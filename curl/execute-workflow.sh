#!/bin/bash
# Execute a workflow with input variables
# Usage: ./execute-workflow.sh <workflow_id>
WORKFLOW_ID="${1:?Usage: ./execute-workflow.sh <workflow_id>}"

curl -s -X POST "https://api.lvng.ai/api/v2/workflows/${WORKFLOW_ID}/execute" \
  -H "x-api-key: ${LVNG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"topic": "Q4 market analysis"}}' | jq .
