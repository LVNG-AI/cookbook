"""
Research Pipeline — Automated multi-source research with LVNG

Takes a topic, searches web + knowledge graph, synthesizes findings
with an AI agent, and stores the final report as an artifact.

Usage:
    export LVNG_API_KEY="lvng_sk_live_..."
    python research-pipeline.py "AI agents in enterprise software 2026"
"""
import os, sys, time, json, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

topic = sys.argv[1] if len(sys.argv) > 1 else "AI agents in enterprise software 2026"
print(f"\n{'='*60}")
print(f"  LVNG Research Pipeline")
print(f"  Topic: {topic}")
print(f"{'='*60}\n")

# ── Step 1: Create or find a research workflow ──────────────────────
print("[1/5] Setting up research workflow...")

# First check if we already have one
resp = requests.get(f"{BASE}/v2/workflows", headers=HEADERS)
workflows = resp.json().get("data", [])
research_wf = next((w for w in workflows if "research" in w.get("name", "").lower()), None)

if not research_wf:
    # Create the workflow from natural language
    print("       Creating workflow from natural language...")
    resp = requests.post(f"{BASE}/v2/workflows/parse", headers=HEADERS, json={
        "description": """
        Research pipeline that:
        1. Searches the web for the given topic
        2. Searches the knowledge graph for internal context
        3. Synthesizes findings into a structured report
        4. Saves the report as an artifact
        """
    })
    if resp.ok:
        research_wf = resp.json().get("data", {})
        print(f"       Created: {research_wf.get('name', 'N/A')}")
    else:
        print(f"       Note: Could not parse workflow, using direct approach")
        research_wf = None

# ── Step 2: Search knowledge graph for internal context ─────────────
print("[2/5] Searching knowledge graph...")

resp = requests.post(f"{BASE}/knowledge/search", headers=HEADERS, json={
    "query": topic,
    "limit": 5
})
knowledge_results = resp.json().get("data", []) if resp.ok else []
print(f"       Found {len(knowledge_results)} internal knowledge entries")

for i, result in enumerate(knowledge_results[:3]):
    title = result.get("title", result.get("name", "Untitled"))
    score = result.get("score", "N/A")
    print(f"       [{i+1}] {title} (score: {score})")

# ── Step 3: Create a research agent ─────────────────────────────────
print("[3/5] Deploying research agent...")

resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json={
    "name": f"Research Agent — {topic[:30]}",
    "system_prompt": f"""You are an expert research analyst. Your task is to synthesize
information about: {topic}

You have access to both web search results and internal knowledge.
Create a well-structured report with:
- Executive Summary (2-3 sentences)
- Key Findings (3-5 bullet points)
- Market Trends (if applicable)
- Recommendations
- Sources

Be specific, data-driven, and concise.""",
    "model": "claude-sonnet-4-6",
    "tools": ["web_search", "knowledge_search"]
})

agent = resp.json().get("data", {}) if resp.ok else {}
agent_id = agent.get("id")
print(f"       Agent deployed: {agent_id}")

# ── Step 4: Run the research via agent message ──────────────────────
print("[4/5] Running research analysis...")

context = ""
if knowledge_results:
    context = "\n\nInternal knowledge context:\n" + "\n".join(
        f"- {r.get('title', 'N/A')}: {r.get('content', r.get('description', ''))[:200]}"
        for r in knowledge_results[:5]
    )

resp = requests.post(f"{BASE}/v2/agents/{agent_id}/message", headers=HEADERS, json={
    "message": f"""Research this topic thoroughly and create a structured report:

Topic: {topic}

{context}

Search the web for the latest information and combine it with the internal
knowledge provided above. Format as a professional research report."""
})

report = resp.json().get("data", {}).get("content", "No response") if resp.ok else "Agent unavailable"
print(f"       Report generated ({len(report)} chars)")

# ── Step 5: Save as artifact ────────────────────────────────────────
print("[5/5] Saving report as artifact...")

resp = requests.post(f"{BASE}/v2/artifacts", headers=HEADERS, json={
    "title": f"Research Report: {topic}",
    "content": report,
    "type": "report",
    "metadata": {
        "topic": topic,
        "knowledge_sources": len(knowledge_results),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent_id": agent_id
    }
})

artifact = resp.json().get("data", {}) if resp.ok else {}
artifact_id = artifact.get("id", "N/A")
print(f"       Artifact saved: {artifact_id}")

# ── Output ──────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  RESEARCH COMPLETE")
print(f"{'='*60}")
print(f"\n  Agent:    {agent_id}")
print(f"  Artifact: {artifact_id}")
print(f"  Sources:  {len(knowledge_results)} internal + web search")
print(f"\n{'─'*60}")
print(f"\n{report[:2000]}")
if len(report) > 2000:
    print(f"\n  ... ({len(report) - 2000} more characters)")
print(f"\n{'─'*60}")

# Cleanup: delete the ephemeral research agent
if agent_id:
    requests.delete(f"{BASE}/v2/agents/{agent_id}", headers=HEADERS)
    print(f"\n  Cleaned up research agent")

print(f"\n  View full report: https://app.lvng.ai/artifacts/{artifact_id}")
print()
