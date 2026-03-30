<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/banner.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/banner.svg">
  <img alt="LVNG Cookbook" src=".github/banner.svg" width="100%">
</picture>

<br /><br />

[![API Docs](https://img.shields.io/badge/API_Docs-lvng.ai%2Fdocs-6C5CE7?style=for-the-badge&logo=readthedocs&logoColor=white)](https://lvng.ai/docs/api)
[![Cookbook](https://img.shields.io/badge/Cookbook-Web_Version-00D2FF?style=for-the-badge&logo=bookstack&logoColor=white)](https://lvng.ai/docs/cookbook)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0_Spec-85EA2D?style=for-the-badge&logo=openapiinitiative&logoColor=black)](https://lvng.ai/docs/openapi.json)
[![License](https://img.shields.io/badge/License-MIT-white?style=for-the-badge)](LICENSE)

</div>

<br />

## What is LVNG?

[LVNG](https://lvng.ai) (Living Network) is a managed multi-agent AI platform. It hosts **AI agents**, **automated workflows**, a **knowledge graph**, and **artifact storage** — all running on LVNG's infrastructure. You interact with the platform through the web app at [app.lvng.ai](https://app.lvng.ai), a REST API, or Claude Code via MCP.

**This cookbook** is a collection of recipes and full working examples that show you how to use the LVNG API to orchestrate agents, workflows, and knowledge from your own code.

<br />

## How It Works — What Runs Where

Understanding the split between **your code** and **LVNG** is the key concept:

```
┌──────────────────────────────┐           ┌──────────────────────────────┐
│  YOUR ENVIRONMENT            │           │  LVNG CLOUD (managed)        │
│                              │           │                              │
│  Where your code runs:       │  HTTPS    │  What LVNG runs for you:     │
│  - Your laptop               │  ──────►  │  - AI agents (Claude, etc.)  │
│  - Your server / VPS         │  API      │  - Workflow execution engine  │
│  - CI pipeline (GitHub, etc) │  calls    │  - Knowledge graph (Neo4j)   │
│  - Cron job                  │           │  - Artifact storage          │
│  - Docker container          │  ◄──────  │  - Web search tools          │
│  - Claude Code terminal      │  JSON     │  - Real-time messaging       │
│                              │  results  │  - Scheduling engine         │
│  You provide:                │           │                              │
│  - API key                   │           │  You get:                    │
│  - The "what" (instructions) │           │  - All compute + AI costs    │
│                              │           │  - Persistence + storage     │
│  Think of it like calling    │           │  - Multi-agent orchestration  │
│  the Stripe API — your code  │           │  - Results at app.lvng.ai    │
│  triggers it, Stripe does    │           │                              │
│  the work.                   │           │                              │
└──────────────────────────────┘           └──────────────────────────────┘
```

### What you write vs. what LVNG does

| You write (runs on your machine) | LVNG handles (runs on LVNG servers) |
|---|---|
| A Python script that says "create a research agent" | Provisions the agent, loads the AI model, connects tools |
| An API call that says "execute this workflow" | Runs every step, manages retries, stores results |
| A search query for your knowledge graph | Queries the graph, ranks results, returns matches |
| A message to an agent | Routes to AI model, executes tool calls, returns response |

**You never deploy code to LVNG.** You don't upload Python files, build containers for LVNG, or modify the platform. Your code stays on your machine and makes API calls. LVNG does the heavy lifting.

### Concrete example

When you run `python research-pipeline.py "AI agents in enterprise"`:

1. **Your laptop** sends `POST /api/v2/agents` to create a research agent → **LVNG** provisions it
2. **Your laptop** sends `POST /api/knowledge/search` → **LVNG** searches your knowledge graph and returns results
3. **Your laptop** sends `POST /api/v2/agents/{id}/message` with the research prompt → **LVNG** runs the AI model, executes web searches, generates the report
4. **Your laptop** sends `POST /api/v2/artifacts` to save the report → **LVNG** stores it permanently
5. **Your laptop** sends `DELETE /api/v2/agents/{id}` to clean up → **LVNG** removes the temp agent

The script took ~10 seconds. The output — a full research report — is now viewable at [app.lvng.ai/artifacts](https://app.lvng.ai). Your laptop did nothing except send 5 HTTP requests.

<br />

## Quick Start

### Prerequisites

- A free LVNG account at [app.lvng.ai](https://app.lvng.ai)
- An API key (create one at [Settings > Developer](https://app.lvng.ai/settings/developer))
- Python 3.8+ (for Python examples) or Node.js 18+ (for JS/TS examples)

### 1. Get your API key

Sign in to [app.lvng.ai](https://app.lvng.ai), go to **Settings > Developer**, and click **Generate API Key**. Copy the key — it's only shown once.

### 2. Set your environment variable

```bash
export LVNG_API_KEY="lvng_sk_live_..."
```

> Add this to your `~/.bashrc` or `~/.zshrc` to persist across terminal sessions.

### 3. Try a quick API call

```bash
# List your workflows
curl https://api.lvng.ai/api/v2/workflows \
  -H "x-api-key: $LVNG_API_KEY" | jq '.data[].name'
```

If you see your workflow names (or an empty array if you haven't created any), you're connected.

### 4. Run an example

```bash
# Clone this repo
git clone https://github.com/LVNG-AI/cookbook.git
cd cookbook

# Install Python dependencies (just requests — no heavy frameworks)
pip install requests

# Run the research pipeline example
python examples/research-pipeline/research-pipeline.py "AI agents in enterprise 2026"
```

The script will:
1. Create a temporary research agent in your LVNG workspace
2. Search the web and your knowledge graph
3. Generate a structured report
4. Save it as an artifact you can view at [app.lvng.ai/artifacts](https://app.lvng.ai)
5. Clean up the temporary agent

<br />

## Install (Optional Packages)

These are optional — the Python examples only need `requests`, and the cURL examples need nothing.

```bash
# MCP Server — connects Claude Code to your LVNG workspace (21 tools)
npm install -g https://api.lvng.ai/packages/lvng-mcp-server-1.0.0.tgz

# TypeScript SDK — programmatic access with full types
npm install https://api.lvng.ai/packages/lvng-sdk-1.0.0.tgz
```

<br />

## Recipes

> Short, single-file scripts that demonstrate one API operation each. Every recipe has **cURL**, **TypeScript**, **Python**, and **Node.js** variants. Click any link to view the source.

These run on your machine. Each one makes 1-2 API calls to LVNG and prints the result.

<table>
<tr>
<td width="200"><strong>Recipe</strong></td>
<td width="140" align="center"><strong>cURL</strong></td>
<td width="140" align="center"><strong>TypeScript</strong></td>
<td width="140" align="center"><strong>Python</strong></td>
<td width="140" align="center"><strong>Node.js</strong></td>
</tr>

<tr>
<td>List workflows</td>
<td align="center"><a href="curl/list-workflows.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/list-workflows.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/list_workflows.py"><code>.py</code></a></td>
<td align="center"><a href="nodejs/list-workflows.js"><code>.js</code></a></td>
</tr>

<tr>
<td>Execute workflow</td>
<td align="center"><a href="curl/execute-workflow.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/execute-workflow.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/execute_workflow.py"><code>.py</code></a></td>
<td align="center"><a href="nodejs/execute-workflow.js"><code>.js</code></a></td>
</tr>

<tr>
<td>Create agent</td>
<td align="center"><a href="curl/create-agent.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/create-agent.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/create_agent.py"><code>.py</code></a></td>
<td align="center">—</td>
</tr>

<tr>
<td>Message agent</td>
<td align="center"><a href="curl/message-agent.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/message-agent.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/message_agent.py"><code>.py</code></a></td>
<td align="center">—</td>
</tr>

<tr>
<td>Search knowledge</td>
<td align="center"><a href="curl/search-knowledge.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/search-knowledge.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/search_knowledge.py"><code>.py</code></a></td>
<td align="center">—</td>
</tr>

<tr>
<td>Stream chat (SSE)</td>
<td align="center"><a href="curl/stream-chat.sh"><code>.sh</code></a></td>
<td align="center"><a href="typescript/stream-chat.ts"><code>.ts</code></a></td>
<td align="center"><a href="python/stream_chat.py"><code>.py</code></a></td>
<td align="center">—</td>
</tr>

<tr>
<td>Manage API keys</td>
<td align="center"><a href="curl/api-keys.sh"><code>.sh</code></a></td>
<td align="center">—</td>
<td align="center"><a href="python/api_keys.py"><code>.py</code></a></td>
<td align="center">—</td>
</tr>

</table>

<br />

## Examples

> Full working applications that combine multiple LVNG APIs into real-world use cases. Each example is a self-contained script that runs on your machine and orchestrates LVNG's hosted agents, workflows, and knowledge graph.

### How to run any example

```bash
# 1. Clone the cookbook
git clone https://github.com/LVNG-AI/cookbook.git && cd cookbook

# 2. Make sure your API key is set
export LVNG_API_KEY="lvng_sk_live_..."

# 3. Install dependencies (Python examples just need the requests library)
pip install requests

# 4. Run an example — it calls the LVNG API and prints results to your terminal
python examples/research-pipeline/research-pipeline.py "AI agents in enterprise 2026"
```

### What happens when you run an example

1. **The script runs on your machine** — it's a regular Python/Node.js program
2. **It makes API calls to LVNG** — creating agents, searching knowledge, executing workflows
3. **LVNG does the heavy lifting** — AI inference, web search, knowledge graph queries
4. **Results come back to your terminal** — and persist in your LVNG workspace at [app.lvng.ai](https://app.lvng.ai)
5. **Temporary resources are cleaned up** — agents are deleted, but artifacts (reports, docs) stay in your workspace for you to review

No Docker required. No special runtime. No deployment to LVNG. Just `python script.py`.

<table>
<tr>
<td width="60" align="center">&#128269;</td>
<td width="220"><strong><a href="examples/research-pipeline">Research Pipeline</a></strong></td>
<td>Multi-source research automation — web search + knowledge graph + AI synthesis into a formatted report</td>
</tr>

<tr>
<td align="center">&#129302;</td>
<td><strong><a href="examples/multi-agent-team">Multi-Agent Team</a></strong></td>
<td>Coordinated agent collaboration — researcher + analyst + lead synthesize a business recommendation</td>
</tr>

<tr>
<td align="center">&#128218;</td>
<td><strong><a href="examples/knowledge-rag">Knowledge RAG</a></strong></td>
<td>Retrieval-augmented generation — ingest docs, search for context, answer questions with sources</td>
</tr>

<tr>
<td align="center">&#128202;</td>
<td><strong><a href="examples/automated-reports">Automated Reports</a></strong></td>
<td>Scheduled report generation — pull metrics, analyze trends, produce weekly/monthly business reports</td>
</tr>

<tr>
<td align="center">&#128172;</td>
<td><strong><a href="examples/discord-integration">Discord Bot</a></strong></td>
<td>Discord slash commands that trigger LVNG agents, workflows, and knowledge search from any channel</td>
</tr>

<tr>
<td align="center">&#9997;&#65039;</td>
<td><strong><a href="examples/content-pipeline">Content Pipeline</a></strong></td>
<td>Multi-stage content creation — writer agent + reviewer + brand voice editor for publish-ready content</td>
</tr>
</table>

<details>
<summary><strong>Example details: what each one does step by step</strong></summary>
<br />

**Research Pipeline** (`python examples/research-pipeline/research-pipeline.py "your topic"`)
1. Creates a temporary research workflow in your LVNG workspace
2. Searches your knowledge graph for internal context
3. Deploys a research agent with web search + knowledge tools
4. Agent searches the web, combines with internal data, writes a report
5. Saves the report as an artifact (viewable at app.lvng.ai/artifacts)
6. Deletes the temporary agent (artifact persists)

**Multi-Agent Team** (`python examples/multi-agent-team/multi-agent-team.py "business question"`)
1. Deploys 3 specialized agents in your workspace: Researcher, Analyst, Lead
2. Runs Researcher and Analyst **in parallel** (uses Python threads)
3. Researcher searches the web; Analyst searches your knowledge graph
4. Lead agent receives both outputs and synthesizes a recommendation
5. Saves combined report as artifact, cleans up all 3 agents

**Knowledge RAG** (`python examples/knowledge-rag/knowledge-rag.py`)
1. Ingests 4 sample documents into your LVNG knowledge graph
2. Creates a RAG-enabled agent with strict grounding rules
3. Asks 4 test questions — for each, searches knowledge first, then sends context + question to the agent
4. Agent answers using ONLY the retrieved context, citing sources
5. Cleans up the agent (documents remain in your knowledge graph)

**Automated Reports** (`python examples/automated-reports/automated-reports.py --period weekly`)
1. Creates a reporting workflow via natural language parsing
2. Queries your knowledge graph for metrics across 4 categories
3. Deploys a report-writing agent with business formatting instructions
4. Agent analyzes the data and generates a structured weekly/monthly report
5. Saves as artifact with metadata (period, date range, data points)
6. Includes cron scheduling tip for true automation

**Discord Bot** (`node examples/discord-integration/discord-bot.js`)
1. Starts a Discord bot (requires `DISCORD_TOKEN` env var)
2. Registers 4 slash commands: `/ask`, `/research`, `/knowledge`, `/workflow`
3. When someone uses `/ask`, creates an agent, sends the question, returns the answer as a Discord embed
4. `/research` triggers a mini research pipeline; `/knowledge` searches the graph; `/workflow` executes a saved workflow
5. This one runs as a **long-lived process** — deploy it on a server, VPS, or container

**Content Pipeline** (`python examples/content-pipeline/content-pipeline.py "content brief"`)
1. Deploys 3 agents: Writer, Reviewer, Brand Voice Editor
2. Writer generates a first draft using web search and knowledge
3. Reviewer scores the draft and produces an improved version
4. Brand Editor applies tone/style guidelines for final polish
5. Saves publish-ready content as artifact, cleans up all agents

</details>

<br />

## Claude Code

Connect [Claude Code](https://docs.anthropic.com/en/docs/claude-code) to your LVNG workspace with 21 MCP tools — manage workflows, agents, and knowledge directly from your terminal using natural language.

### Setup

```bash
# 1. Install the MCP server
npm install -g https://api.lvng.ai/packages/lvng-mcp-server-1.0.0.tgz
```

```json
// 2. Add to ~/.claude/settings.json
{
  "mcpServers": {
    "lvng": {
      "command": "lvng-mcp-server",
      "env": {
        "LVNG_API_KEY": "lvng_sk_live_..."
      }
    }
  }
}
```

### Usage

Once configured, ask Claude anything about your LVNG workspace:

```
> list my workflows
> create an agent called "Data Analyst" with web search tools
> search knowledge for "Q4 revenue"
> execute workflow wf_123 with topic "market research"
```

Claude Code calls the LVNG API on your behalf through the MCP server. Agents, workflows, and artifacts are created in your LVNG workspace — same as if you used the API directly.

<details>
<summary><strong>All 21 MCP Tools</strong></summary>
<br />

| Category | Count | Tools |
|----------|-------|-------|
| **Workflows** | 9 | `list` `get` `create` `update` `delete` `execute` `get_run` `list_runs` `parse` |
| **Agents** | 8 | `list` `get` `create` `update` `delete` `message` `start` `stop` |
| **Knowledge** | 4 | `search` `ingest` `list_entities` `get_stats` |

</details>

<br />

## API Key Format

```
lvng_sk_live_7e8949d627f560d298f310ceeadb492c
│       │    │
│       │    └── 32 random hex characters
│       └── Environment (live / test)
└── Prefix (identifies as LVNG per-user key)
```

- Keys are **SHA-256 hashed** at rest — never stored in plaintext
- Raw key shown **once** at creation — store it securely
- Max **10 active keys** per user
- Scopes: `read` · `write` · `execute` · `admin` · `knowledge:read` · `knowledge:write`

<br />

## Where to Run Your Code

Since your code just makes API calls, it can run anywhere with internet access:

| Environment | Best for | Example |
|---|---|---|
| **Your laptop** | Development, testing, one-off tasks | `python research-pipeline.py "topic"` |
| **Cron job** | Scheduled reports, recurring workflows | `0 9 * * MON python automated-reports.py` |
| **GitHub Actions** | CI/CD automation, triggered by events | Run on push, PR, or schedule |
| **Docker container** | Long-running services (Discord bot) | `docker run -e LVNG_API_KEY=... bot` |
| **VPS / server** | Always-on bots, high-frequency automation | Any cloud provider |
| **Claude Code** | Interactive, natural language | "list my workflows" in terminal |
| **Your own app** | Embedding LVNG in your product | Import the SDK, call the API |

The only dependency is an API key and `pip install requests` (Python) or `npm install axios` (Node). No LVNG-specific runtime, no containers to build for LVNG, no special deployment step.

<br />

## FAQ

**Do I need to deploy anything to LVNG?**
No. LVNG is a fully managed platform. You call the API from wherever your code runs, and LVNG handles everything on its servers — AI inference, workflow execution, knowledge graph queries, artifact storage. You never upload code to LVNG or build containers for it.

**Where do the Python/Node.js scripts run?**
On your machine (or server, CI, cron — anywhere). Clone this repo, set your `LVNG_API_KEY` environment variable, and run the scripts from your terminal. They make HTTPS calls to `api.lvng.ai` and print results locally.

**What does the script create inside my LVNG workspace?**
Depends on the example, but typically:
- **Agents** — created temporarily to do work, then deleted when the script finishes
- **Artifacts** — reports, documents, analysis results that persist in your workspace
- **Knowledge entries** — documents ingested into your knowledge graph (persist permanently)
- **Workflow runs** — execution logs with status, inputs, and outputs

You can see all of these in the web app at [app.lvng.ai](https://app.lvng.ai).

**What's the difference between the web app and the API?**
Same platform, different interfaces. The web app at [app.lvng.ai](https://app.lvng.ai) lets you create agents, build workflows, and browse your knowledge graph with a visual UI. The API lets you do the same things programmatically — from scripts, apps, or Claude Code. Anything created via API shows up in the web app and vice versa.

**Can I schedule scripts to run automatically?**
Yes. Use any scheduler — cron, GitHub Actions, AWS Lambda, etc. For example, a weekly report every Monday at 9am:
```
0 9 * * MON LVNG_API_KEY="lvng_sk_live_..." python automated-reports.py --period weekly
```

**Can I use LVNG from inside my own application?**
Yes. That's what the TypeScript SDK and API are for. Import the SDK into your app, initialize it with your API key, and call LVNG from your backend. Common use cases: adding AI agents to a SaaS product, building a knowledge Q&A into a support tool, triggering workflows from webhooks.

**What about the Discord bot — where does that run?**
The Discord bot is the one example that runs as a long-lived process (it stays connected to Discord). Deploy it on any server, VPS, or container that stays running. It connects to both Discord and the LVNG API. Every other example is a run-once script.

**Do I pay for the AI inference?**
Your LVNG plan includes API usage. When your script creates an agent and sends it a message, LVNG handles the AI model call (Claude, etc.) on its servers. You don't need your own Anthropic API key or pay separately for AI inference — it's part of your LVNG workspace.

<br />

## Links

| Resource | URL |
|----------|-----|
| API Reference | [lvng.ai/docs/api](https://lvng.ai/docs/api) |
| Cookbook (web) | [lvng.ai/docs/cookbook](https://lvng.ai/docs/cookbook) |
| SDKs & Claude Code | [lvng.ai/docs/sdks](https://lvng.ai/docs/sdks) |
| API Keys | [lvng.ai/docs/api/api-keys](https://lvng.ai/docs/api/api-keys) |
| OpenAPI Spec | [lvng.ai/docs/openapi.json](https://lvng.ai/docs/openapi.json) |
| Developer Settings | [app.lvng.ai/settings/developer](https://app.lvng.ai/settings/developer) |

<br />

<div align="center">

Made by [LVNG](https://lvng.ai) · MIT License

</div>
