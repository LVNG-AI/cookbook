#!/bin/bash
# Stream a chat response via Server-Sent Events
curl -N -X POST https://api.lvng.ai/api/v2/chat/stream \
  -H "x-api-key: ${LVNG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a 3-paragraph market analysis for AI in 2026"}'
