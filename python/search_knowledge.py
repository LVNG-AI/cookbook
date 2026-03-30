"""Search the knowledge graph."""
import os, sys, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

query = sys.argv[1] if len(sys.argv) > 1 else input("Search query: ")

resp = requests.post(f"{BASE}/knowledge/search", headers=HEADERS, json={
    "query": query,
    "limit": 10
})
resp.raise_for_status()
for result in resp.json()["data"]:
    print(f"{result.get('title', 'Untitled')} — score: {result.get('score', 'N/A')}")
