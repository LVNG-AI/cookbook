"""
Knowledge RAG — Retrieval-Augmented Generation with LVNG

Ingests documents into the knowledge graph, then answers questions
using retrieved context for grounded, source-backed responses.

Usage:
    export LVNG_API_KEY="lvng_sk_live_..."
    python knowledge-rag.py
"""
import os, sys, json, requests

BASE = "https://api.lvng.ai/api"
HEADERS = {"x-api-key": os.environ["LVNG_API_KEY"], "Content-Type": "application/json"}

print(f"\n{'='*60}")
print(f"  LVNG Knowledge RAG Pipeline")
print(f"{'='*60}\n")

# ── Step 1: Ingest sample documents ──────────────────────────────────
print("[1/4] Ingesting documents into knowledge graph...\n")

documents = [
    {
        "title": "Q4 2025 Revenue Report",
        "content": """Q4 2025 revenue reached $4.2M, up 34% YoY. Enterprise segment
grew 52% driven by 12 new Fortune 500 accounts. SMB segment declined 8% due to
increased churn from pricing changes in September. ARPU increased to $2,400/month
for enterprise vs $89/month for SMB. Net revenue retention was 118% for enterprise
and 94% for SMB. Total ARR exiting Q4 was $16.8M."""
    },
    {
        "title": "Product Roadmap 2026",
        "content": """2026 priorities: (1) Multi-agent orchestration — ship by Q1,
enables teams of AI agents working together. (2) Knowledge graph v2 — semantic
search with embeddings, due Q2. (3) Enterprise SSO — SAML/OIDC support, Q2.
(4) Workflow marketplace — community-shared templates, Q3. (5) Mobile app — iOS
and Android, Q4. Budget allocated: $2.1M engineering, $800K infrastructure."""
    },
    {
        "title": "Customer Feedback Summary - March 2026",
        "content": """Top requests from enterprise customers: (1) Better API
documentation and SDKs (mentioned by 67% of accounts). (2) Custom agent
templates (54%). (3) Audit logging for compliance (48%). (4) On-premise
deployment option (31%). (5) Slack/Teams integration (89%). NPS score: 72
(up from 64 in Q3). Main detractor theme: onboarding complexity."""
    },
    {
        "title": "Competitive Analysis - AI Platforms",
        "content": """Key competitors: Platform A ($200M funding, 10K customers,
strong in code generation). Platform B (open source, 50K GitHub stars, weak
in enterprise). Platform C (acquired by BigCo, losing indie developers).
Our differentiators: multi-agent collaboration, knowledge graph integration,
workflow automation. Weakness: smaller developer community, limited integrations."""
    }
]

for doc in documents:
    resp = requests.post(f"{BASE}/knowledge/upload", headers=HEADERS, json={
        "title": doc["title"],
        "content": doc["content"],
        "type": "document"
    })
    status = "OK" if resp.ok else f"Error {resp.status_code}"
    print(f"  [{status:>5}]  {doc['title']}")

# ── Step 2: Verify knowledge graph stats ─────────────────────────────
print(f"\n[2/4] Checking knowledge graph...\n")

resp = requests.get(f"{BASE}/knowledge-graph/statistics", headers=HEADERS)
if resp.ok:
    stats = resp.json().get("data", {})
    print(f"  Entities:      {stats.get('entity_count', 'N/A')}")
    print(f"  Relationships: {stats.get('relationship_count', 'N/A')}")
    print(f"  Documents:     {stats.get('document_count', 'N/A')}")

# ── Step 3: Create a RAG-enabled agent ───────────────────────────────
print(f"\n[3/4] Setting up RAG agent...\n")

resp = requests.post(f"{BASE}/v2/agents", headers=HEADERS, json={
    "name": "Knowledge Assistant",
    "system_prompt": """You are a helpful assistant that answers questions using
the provided knowledge context. Follow these rules:

1. ONLY use information from the provided context to answer
2. If the context doesn't contain enough information, say so
3. Always cite which document your information comes from
4. Be specific — include numbers, dates, and percentages
5. If asked about something not in the context, say "I don't have
   information about that in my knowledge base."

Format: Start with a direct answer, then supporting details with citations.""",
    "model": "claude-sonnet-4-6",
    "tools": ["knowledge_search"]
})

agent = resp.json().get("data", {}) if resp.ok else {}
agent_id = agent.get("id")
print(f"  Agent deployed: {agent_id}")

# ── Step 4: Ask questions with RAG ───────────────────────────────────
print(f"\n[4/4] Running RAG queries...\n")

questions = [
    "What was our Q4 revenue and how did enterprise vs SMB perform?",
    "What are the top customer requests and what's our NPS?",
    "What are our main competitive differentiators?",
    "When is the mobile app shipping and what's the budget?",
]

for i, question in enumerate(questions):
    print(f"  Question {i+1}: {question}")

    # Search knowledge graph for context
    search_resp = requests.post(f"{BASE}/knowledge/search", headers=HEADERS, json={
        "query": question,
        "limit": 3
    })
    context_docs = search_resp.json().get("data", []) if search_resp.ok else []

    # Build context string from search results
    context = "\n\n".join(
        f"[{doc.get('title', 'Unknown')}]: {doc.get('content', doc.get('description', ''))}"
        for doc in context_docs
    )

    # Send to agent with context
    resp = requests.post(f"{BASE}/v2/agents/{agent_id}/message", headers=HEADERS, json={
        "message": f"""Answer this question using ONLY the context below.

Question: {question}

Context:
{context}

Remember to cite your sources."""
    })

    answer = resp.json().get("data", {}).get("content", "No answer") if resp.ok else "Error"
    print(f"  Answer: {answer[:300]}")
    if len(answer) > 300:
        print(f"          ... ({len(answer) - 300} more chars)")
    print(f"  Sources: {', '.join(d.get('title', '?') for d in context_docs[:3])}")
    print()

# ── Cleanup ───────────────────────────────────────────────────────────
if agent_id:
    requests.delete(f"{BASE}/v2/agents/{agent_id}", headers=HEADERS)
    print(f"  Cleaned up agent: {agent_id}")

print(f"\n{'='*60}")
print(f"  RAG PIPELINE COMPLETE")
print(f"{'='*60}\n")
