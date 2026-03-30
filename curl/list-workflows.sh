#!/bin/bash
# List all workflows in your workspace
curl -s https://api.lvng.ai/api/v2/workflows \
  -H "x-api-key: ${LVNG_API_KEY}" | jq .
