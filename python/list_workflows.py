"""List all workflows in your workspace."""
import os, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

resp = requests.get(f"{BASE}/v2/workflows", headers=HEADERS)
resp.raise_for_status()

for wf in resp.json()["data"]:
    print(f"{wf['name']} — {wf['status']}")
