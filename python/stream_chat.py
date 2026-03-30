"""Stream a chat response via Server-Sent Events."""
import os, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

resp = requests.post(
    f"{BASE}/v2/chat/stream",
    headers=HEADERS,
    json={"message": "Write a 3-paragraph market analysis for AI in 2026"},
    stream=True
)
resp.raise_for_status()

for line in resp.iter_lines(decode_unicode=True):
    if line:
        print(line, flush=True)
