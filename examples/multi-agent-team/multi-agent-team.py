"""
Multi-Agent Team — Coordinated agent collaboration with LVNG

Deploys a team of specialized agents that work together:
  - Research Agent: web search for external intelligence
  - Data Agent: analyzes internal knowledge/metrics
  - Lead Agent: synthesizes both into actionable recommendations

Usage:
    export LVNG_API_KEY="lvng_sk_live_..."
    python multi-agent-team.py "Should we expand into the European market?"
"""
import os, sys, json, time, requests
from concurrent.futures import ThreadPoolExecutor

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

question = sys.argv[1] if len(sys.argv) > 1 else "Should we expand into the European market?"
print(f"\n{'='*60}")
print(f"  LVNG Multi-Agent Team")
print(f"  Question: {question}")
print(f"{'='*60}\n")

agents = {}

# ── Step 1: Deploy the agent team ────────────────────────────────────
print("[1/4] Deploying agent team...\n")

team_specs = {
    "researcher": {
        "name": "Research Specialist",
        "system_prompt": f"""You are a research specialist focused on external intelligence.
Your job is to search the web for relevant data about: {question}

Provide:
- 3-5 key findings from recent sources
- Market data and statistics
- Competitor actions or industry trends
- Include source URLs where possible

Be factual and data-driven. No fluff.""",
        "model": "claude-sonnet-4-6",
        "tools": ["web_search"]
    },
    "analyst": {
        "name": "Data Analyst",
        "system_prompt": f"""You are an internal data analyst.
Your job is to analyze internal knowledge and metrics related to: {question}

Search the knowledge graph for relevant internal data and provide:
- Key internal metrics and trends
- Historical context from past decisions
- Risk factors from internal data
- Relevant past projects or initiatives

Be specific and reference actual data points.""",
        "model": "claude-sonnet-4-6",
        "tools": ["knowledge_search"]
    },
    "lead": {
        "name": "Strategy Lead",
        "system_prompt": """You are a senior strategy advisor.
You will receive analysis from two specialists:
1. A Research Specialist (external/market data)
2. A Data Analyst (internal metrics/knowledge)

Your job is to synthesize both into a clear recommendation with:
- Executive Summary (2-3 sentences)
- Key Arguments For (with supporting data)
- Key Arguments Against (with supporting data)
- Risk Assessment (High/Medium/Low with explanation)
- Recommended Action (specific next steps)
- Timeline suggestion

Be decisive. Give a clear yes/no/conditional recommendation.""",
        "model": "claude-sonnet-4-6",
        "tools": []
    }
}

for role, spec in team_specs.items():
    resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json=spec)
    if resp.ok:
        agent = resp.json().get("data", {})
        agents[role] = agent.get("id")
        print(f"  [{role.upper():>10}]  {agent.get('id', 'N/A')}  ({spec['name']})")
    else:
        print(f"  [{role.upper():>10}]  FAILED — {resp.status_code}")
        agents[role] = None

# ── Step 2: Run research + analysis in parallel ──────────────────────
print(f"\n[2/4] Running parallel analysis...\n")

def run_agent(role, agent_id, message):
    """Send a message to an agent and return the response."""
    if not agent_id:
        return role, "Agent not available"
    start = time.time()
    resp = requests.post(f"{BASE}/v2/agents/{agent_id}/message", headers=HEADERS, json={
        "message": message
    })
    elapsed = time.time() - start
    if resp.ok:
        content = resp.json().get("data", {}).get("content", "No response")
        print(f"  [{role.upper():>10}]  Done ({elapsed:.1f}s, {len(content)} chars)")
        return role, content
    else:
        print(f"  [{role.upper():>10}]  Error: {resp.status_code}")
        return role, f"Error: {resp.status_code}"

# Run researcher and analyst simultaneously
results = {}
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(run_agent, "researcher", agents["researcher"],
            f"Research this business question thoroughly: {question}"),
        executor.submit(run_agent, "analyst", agents["analyst"],
            f"Analyze internal data relevant to this question: {question}")
    ]
    for future in futures:
        role, content = future.result()
        results[role] = content

# ── Step 3: Lead agent synthesizes ───────────────────────────────────
print(f"\n[3/4] Lead agent synthesizing findings...\n")

synthesis_prompt = f"""Here is the business question: {question}

## Research Specialist Findings:
{results.get('researcher', 'No data available')}

## Internal Data Analysis:
{results.get('analyst', 'No data available')}

---

Now synthesize both inputs into your strategic recommendation.
Be specific, reference data from both sources, and give a clear recommendation."""

_, lead_response = run_agent("lead", agents["lead"], synthesis_prompt)
results["lead"] = lead_response

# ── Step 4: Save results ─────────────────────────────────────────────
print(f"\n[4/4] Saving team output...\n")

full_report = f"""# Multi-Agent Analysis: {question}

## Research Specialist Report
{results.get('researcher', 'N/A')}

---

## Internal Data Analysis
{results.get('analyst', 'N/A')}

---

## Strategic Recommendation
{results.get('lead', 'N/A')}
"""

resp = requests.post(f"{BASE}/v2/artifacts", headers=HEADERS, json={
    "title": f"Team Analysis: {question[:50]}",
    "content": full_report,
    "type": "report",
    "metadata": {
        "team_size": 3,
        "agents": agents,
        "question": question,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
})

artifact_id = resp.json().get("data", {}).get("id", "N/A") if resp.ok else "N/A"

# ── Output ────────────────────────────────────────────────────────────
print(f"{'='*60}")
print(f"  ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"\n  Artifact: {artifact_id}")
print(f"\n{'─'*60}")
print(f"\n{results.get('lead', 'No synthesis available')[:2000]}")
if len(results.get('lead', '')) > 2000:
    print(f"\n  ... ({len(results['lead']) - 2000} more characters)")
print(f"\n{'─'*60}")

# Cleanup
print(f"\n  Cleaning up agents...")
for role, agent_id in agents.items():
    if agent_id:
        requests.delete(f"{BASE}/v2/agents/{agent_id}", headers=HEADERS)
        print(f"    Deleted {role}: {agent_id}")

print(f"\n  View full report: https://app.lvng.ai/artifacts/{artifact_id}")
print()
