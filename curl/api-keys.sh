#!/bin/bash
# API key management (requires JWT auth, not API key)
# Set JWT_TOKEN from your Supabase session

# Create a key
echo "=== Creating API key ==="
curl -s -X POST https://api.lvng.ai/api/v2/api-keys \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name": "ci-pipeline", "scopes": ["read", "execute"]}' | jq .

# List keys
echo "=== Listing API keys ==="
curl -s https://api.lvng.ai/api/v2/api-keys \
  -H "Authorization: Bearer ${JWT_TOKEN}" | jq .

# Revoke a key (replace KEY_ID)
# curl -s -X DELETE "https://api.lvng.ai/api/v2/api-keys/${KEY_ID}" \
#   -H "Authorization: Bearer ${JWT_TOKEN}" | jq .
