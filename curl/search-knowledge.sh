#!/bin/bash
# Search the knowledge graph
# Usage: ./search-knowledge.sh "your query"
QUERY="${1:?Usage: ./search-knowledge.sh \"query\"}"

curl -s -X POST https://api.lvng.ai/api/knowledge/search \
  -H "x-api-key: ${LVNG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"${QUERY}\", \"limit\": 10}" | jq .
