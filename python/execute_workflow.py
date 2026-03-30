"""Execute a workflow with input variables."""
import os, sys, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

workflow_id = sys.argv[1] if len(sys.argv) > 1 else input("Workflow ID: ")

resp = requests.post(
    f"{BASE}/v2/workflows/{workflow_id}/execute",
    headers=HEADERS,
    json={"inputs": {"topic": "Q4 market analysis"}}
)
resp.raise_for_status()
run = resp.json()["data"]
print(f"Run ID: {run['id']}")
