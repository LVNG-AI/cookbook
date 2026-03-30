"""
Content Pipeline — Multi-stage content creation with LVNG

Automates content production with specialized agents:
  - Writer: generates first draft
  - Reviewer: checks accuracy, structure, engagement
  - Brand Editor: applies brand voice and tone
  - Final output saved as artifact

Usage:
    export LVNG_API_KEY="lvng_sk_live_..."
    python content-pipeline.py "Blog post about AI agents for non-technical leaders"
    python content-pipeline.py "Product launch email for our new API SDK"
"""
import os, sys, json, time, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

brief = sys.argv[1] if len(sys.argv) > 1 else "Blog post about AI agents for non-technical business leaders"

print(f"\n{'='*60}")
print(f"  LVNG Content Pipeline")
print(f"  Brief: {brief}")
print(f"{'='*60}\n")

agents = {}

# ── Step 1: Deploy the content team ──────────────────────────────────
print("[1/5] Deploying content team...\n")

team = {
    "writer": {
        "name": "Content Writer",
        "system_prompt": f"""You are an expert content writer. Create a compelling first draft based on:

Brief: {brief}

Guidelines:
- Write in a clear, engaging style
- Use short paragraphs (2-3 sentences max)
- Include a strong opening hook
- Add subheadings for scanability
- Include specific examples or data points
- End with a clear call-to-action
- Target length: 800-1200 words
- Format: Markdown with headers""",
        "tools": ["web_search", "knowledge_search"]
    },
    "reviewer": {
        "name": "Content Reviewer",
        "system_prompt": """You are a senior content editor and fact-checker. Review the draft for:

1. **Accuracy** — flag any claims that need sources or seem incorrect
2. **Structure** — is the flow logical? Are transitions smooth?
3. **Engagement** — is the opening compelling? Does it hold attention?
4. **Clarity** — any jargon, run-on sentences, or confusing passages?
5. **Completeness** — does it fully address the brief?

Provide:
- Overall quality score (1-10)
- 3 specific strengths
- 3 specific improvements needed
- Revised version with your edits applied

Be constructive but honest.""",
        "tools": []
    },
    "brand_editor": {
        "name": "Brand Voice Editor",
        "system_prompt": """You are a brand voice specialist. Apply these brand guidelines:

Tone: Professional but approachable. Confident, not arrogant.
Voice: We speak as knowledgeable peers, not lecturers.
Language:
  - Active voice preferred
  - "You" over "one" or "users"
  - Contractions are fine (we're, you'll, it's)
  - Avoid: "leverage", "synergy", "disrupt", "revolutionary"
  - Prefer: "use", "combine", "improve", "practical"
  - Technical terms should be briefly explained on first use

Apply these guidelines to the content. Make minimal but impactful edits.
Return the final polished version ready to publish.""",
        "tools": []
    }
}

for role, spec in team.items():
    resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json={
        "name": spec["name"],
        "system_prompt": spec["system_prompt"],
        "model": "claude-sonnet-4-6",
        "tools": spec.get("tools", [])
    })
    if resp.ok:
        agent = resp.json().get("data", {})
        agents[role] = agent.get("id")
        print(f"  [{role:>12}]  {agent.get('id', 'N/A')}")
    else:
        agents[role] = None
        print(f"  [{role:>12}]  FAILED")

# ── Step 2: Generate first draft ─────────────────────────────────────
print(f"\n[2/5] Writing first draft...\n")

# Get relevant knowledge for context
resp = requests.post(f"{BASE}/knowledge/search", headers=HEADERS, json={
    "query": brief, "limit": 3
})
knowledge = resp.json().get("data", []) if resp.ok else []
context = "\n".join(f"- {k.get('title', '')}: {k.get('content', '')[:150]}" for k in knowledge)

resp = requests.post(f"{BASE}/v2/agents/{agents['writer']}/message", headers=HEADERS, json={
    "message": f"""Write the content based on this brief: {brief}

Internal knowledge for reference:
{context or '(No internal data — use web research)'}

Create a complete, publish-ready first draft."""
})

draft = resp.json().get("data", {}).get("content", "Draft failed") if resp.ok else "Error"
print(f"  Draft complete: {len(draft)} chars")

# ── Step 3: Review and improve ────────────────────────────────────────
print(f"\n[3/5] Reviewing draft...\n")

resp = requests.post(f"{BASE}/v2/agents/{agents['reviewer']}/message", headers=HEADERS, json={
    "message": f"""Review this content draft:

Brief: {brief}

Draft:
{draft}

Provide your quality assessment and improved version."""
})

review = resp.json().get("data", {}).get("content", "Review failed") if resp.ok else "Error"
print(f"  Review complete: {len(review)} chars")

# ── Step 4: Apply brand voice ─────────────────────────────────────────
print(f"\n[4/5] Applying brand voice...\n")

resp = requests.post(f"{BASE}/v2/agents/{agents['brand_editor']}/message", headers=HEADERS, json={
    "message": f"""Apply brand voice guidelines to this reviewed content:

{review}

Return only the final polished version, ready to publish."""
})

final_content = resp.json().get("data", {}).get("content", "Brand edit failed") if resp.ok else "Error"
print(f"  Final version: {len(final_content)} chars")

# ── Step 5: Save as artifact ──────────────────────────────────────────
print(f"\n[5/5] Saving final content...\n")

resp = requests.post(f"{BASE}/v2/artifacts", headers=HEADERS, json={
    "title": f"Content: {brief[:60]}",
    "content": final_content,
    "type": "document",
    "metadata": {
        "brief": brief,
        "pipeline_stages": ["draft", "review", "brand_voice"],
        "agents_used": 3,
        "draft_length": len(draft),
        "final_length": len(final_content),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
})

artifact = resp.json().get("data", {}) if resp.ok else {}
artifact_id = artifact.get("id", "N/A")

# ── Output ────────────────────────────────────────────────────────────
print(f"{'='*60}")
print(f"  CONTENT PIPELINE COMPLETE")
print(f"{'='*60}")
print(f"\n  Brief:     {brief}")
print(f"  Stages:    Writer → Reviewer → Brand Editor")
print(f"  Draft:     {len(draft)} chars")
print(f"  Final:     {len(final_content)} chars")
print(f"  Artifact:  {artifact_id}")
print(f"\n{'─'*60}")
print(f"\n{final_content[:2000]}")
if len(final_content) > 2000:
    print(f"\n  ... ({len(final_content) - 2000} more characters)")
print(f"\n{'─'*60}")

# Cleanup
print(f"\n  Cleaning up agents...")
for role, agent_id in agents.items():
    if agent_id:
        requests.delete(f"{BASE}/v2/agents/{agent_id}", headers=HEADERS)
print(f"  Done.")

print(f"\n  View: https://app.lvng.ai/artifacts/{artifact_id}")
print()
