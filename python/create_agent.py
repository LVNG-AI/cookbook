"""Create a new AI agent."""
import os, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json={
    "name": "Research Assistant",
    "system_prompt": "You are a helpful research assistant.",
    "model": "claude-sonnet-4-6",
    "tools": ["web_search", "knowledge_search"]
})
resp.raise_for_status()
agent = resp.json()["data"]
print(f"Agent ID: {agent['id']}")
