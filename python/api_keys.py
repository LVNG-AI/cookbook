"""Manage API keys (requires JWT auth)."""
import os, requests

BASE = "https://api.lvng.ai/api"
JWT = os.environ["LVNG_JWT_TOKEN"]  # Get from Supabase session
HEADERS = {"Authorization": f"Bearer {JWT}", "Content-Type": "application/json"}

# Create a key
resp = requests.post(f"{BASE}/v2/api-keys", headers=HEADERS, json={
    "name": "ci-pipeline",
    "scopes": ["read", "execute"]
})
resp.raise_for_status()
data = resp.json()["data"]
print(f"New key: {data['key']}")  # Save this — shown only once!
print(f"Key ID: {data['id']}")

# List keys
resp = requests.get(f"{BASE}/v2/api-keys", headers=HEADERS)
for key in resp.json()["data"]:
    print(f"  {key['name']} ({key['key_prefix']}...) — {', '.join(key['scopes'])}")
