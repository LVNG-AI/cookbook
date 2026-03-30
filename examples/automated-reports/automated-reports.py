"""
Automated Reports — Scheduled report generation with LVNG

Creates a workflow that generates business reports on demand or on a schedule.
Pulls data from knowledge graph, analyzes with an agent, and stores as artifact.

Usage:
    export LVNG_API_KEY="lvng_sk_live_..."
    python automated-reports.py                    # Generate report now
    python automated-reports.py --period weekly    # Weekly report
    python automated-reports.py --period monthly   # Monthly report

Tip: Schedule with cron for automated delivery:
    0 9 * * MON python automated-reports.py --period weekly
"""
import os, sys, json, time, requests
from datetime import datetime, timedelta

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

# Parse period argument
period = "weekly"
if "--period" in sys.argv:
    idx = sys.argv.index("--period")
    if idx + 1 < len(sys.argv):
        period = sys.argv[idx + 1]

now = datetime.now()
if period == "weekly":
    start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    period_label = f"Week of {start_date}"
elif period == "monthly":
    start_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    period_label = f"Month ending {now.strftime('%Y-%m-%d')}"
else:
    start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    period_label = f"Custom: {start_date} to {now.strftime('%Y-%m-%d')}"

print(f"\n{'='*60}")
print(f"  LVNG Automated Report Generator")
print(f"  Period: {period_label}")
print(f"{'='*60}\n")

# ── Step 1: Create or find the reporting workflow ─────────────────────
print("[1/5] Setting up reporting workflow...\n")

resp = requests.post(f"{BASE}/v2/workflows/parse", headers=HEADERS, json={
    "description": f"""
    Automated {period} business report that:
    1. Searches knowledge for metrics from the past {period}
    2. Identifies trends and anomalies
    3. Generates an executive summary
    4. Creates actionable recommendations
    """
})

workflow = resp.json().get("data", {}) if resp.ok else {}
workflow_id = workflow.get("id")
print(f"  Workflow: {workflow_id or 'Using direct approach'}")

# ── Step 2: Gather data from knowledge graph ──────────────────────────
print("[2/5] Gathering data...\n")

data_queries = [
    f"revenue metrics {period} {start_date}",
    f"customer activity {period} trends",
    f"product usage {period} statistics",
    f"team performance {period} updates",
]

all_data = []
for query in data_queries:
    resp = requests.post(f"{BASE}/knowledge/search", headers=HEADERS, json={
        "query": query,
        "limit": 3
    })
    results = resp.json().get("data", []) if resp.ok else []
    all_data.extend(results)
    print(f"  [{len(results)} results]  {query}")

print(f"\n  Total data points: {len(all_data)}")

# ── Step 3: Deploy report writer agent ────────────────────────────────
print("\n[3/5] Deploying report writer...\n")

resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json={
    "name": f"Report Writer — {period_label}",
    "system_prompt": f"""You are an expert business report writer.
Generate a professional {period} report for the period: {period_label}.

Report structure:
1. **Executive Summary** — 3 sentence overview
2. **Key Metrics** — table of top 5 KPIs with period-over-period change
3. **Highlights** — top 3 positive developments
4. **Concerns** — top 3 items needing attention
5. **Trend Analysis** — what's moving and why
6. **Recommendations** — 3 specific action items with owners
7. **Next Period Outlook** — what to watch for

Formatting rules:
- Use markdown with headers and bullet points
- Include specific numbers when available
- Bold key figures and percentages
- Keep total length under 1000 words
- End each section with a one-line takeaway""",
    "model": "claude-sonnet-4-6",
    "tools": ["web_search", "knowledge_search"]
})

agent = resp.json().get("data", {}) if resp.ok else {}
agent_id = agent.get("id")
print(f"  Agent: {agent_id}")

# ── Step 4: Generate the report ───────────────────────────────────────
print("\n[4/5] Generating report...\n")

data_context = "\n".join(
    f"- [{item.get('title', 'N/A')}] {item.get('content', item.get('description', ''))[:200]}"
    for item in all_data[:15]
)

resp = requests.post(f"{BASE}/v2/agents/{agent_id}/message", headers=HEADERS, json={
    "message": f"""Generate the {period} business report for: {period_label}

Available data from knowledge graph:
{data_context if data_context else "(No internal data available — generate a template report with placeholder metrics)"}

If internal data is limited, supplement with reasonable analysis based on
the available information. Clearly mark any assumptions."""
})

report = resp.json().get("data", {}).get("content", "Report generation failed") if resp.ok else "Error"
print(f"  Report generated: {len(report)} characters")

# ── Step 5: Save as artifact ──────────────────────────────────────────
print("\n[5/5] Saving report...\n")

resp = requests.post(f"{BASE}/v2/artifacts", headers=HEADERS, json={
    "title": f"{period.title()} Report — {period_label}",
    "content": report,
    "type": "report",
    "metadata": {
        "period": period,
        "period_label": period_label,
        "start_date": start_date,
        "end_date": now.strftime("%Y-%m-%d"),
        "data_points": len(all_data),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent_id": agent_id,
        "workflow_id": workflow_id
    }
})

artifact = resp.json().get("data", {}) if resp.ok else {}
artifact_id = artifact.get("id", "N/A")
print(f"  Artifact: {artifact_id}")

# ── Output ────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  REPORT GENERATED")
print(f"{'='*60}")
print(f"\n  Period:    {period_label}")
print(f"  Data:      {len(all_data)} knowledge entries")
print(f"  Artifact:  {artifact_id}")
print(f"\n{'─'*60}")
print(f"\n{report[:2000]}")
if len(report) > 2000:
    print(f"\n  ... ({len(report) - 2000} more characters)")
print(f"\n{'─'*60}")

# Cleanup
if agent_id:
    requests.delete(f"{BASE}/v2/agents/{agent_id}", headers=HEADERS)
    print(f"\n  Cleaned up report agent")

print(f"\n  View: https://app.lvng.ai/artifacts/{artifact_id}")
print(f"\n  Tip: Schedule with cron for automatic delivery:")
print(f"    0 9 * * MON python automated-reports.py --period weekly")
print()
