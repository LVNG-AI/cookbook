"""Send a message to a running agent."""
import os, sys, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

agent_id = sys.argv[1] if len(sys.argv) > 1 else input("Agent ID: ")
message = sys.argv[2] if len(sys.argv) > 2 else input("Message: ")

resp = requests.post(
    f"{BASE}/v2/agents/{agent_id}/message",
    headers=HEADERS,
    json={"message": message}
)
resp.raise_for_status()
print(resp.json()["data"]["content"])
