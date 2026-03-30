# Discord Bot Integration

> Connect a Discord bot to LVNG so your team can trigger workflows, query knowledge, and chat with agents directly from Discord channels.

## What You'll Build

```
Discord Message → Bot Handler → LVNG API → Agent/Workflow/Knowledge → Discord Reply
```

A Discord bot that:
1. Listens for commands in your server
2. Routes `/research`, `/ask`, `/workflow` to LVNG APIs
3. Streams agent responses back to Discord
4. Formats results with Discord embeds

## Commands
| Command | What it does |
|---------|-------------|
| `/ask <question>` | Chat with your LVNG agent |
| `/research <topic>` | Run a research workflow |
| `/knowledge <query>` | Search the knowledge graph |
| `/workflow <name>` | Execute a saved workflow |

## Use Cases
- Team-wide access to AI agents without leaving Discord
- Trigger workflows from mobile via Discord
- Knowledge base Q&A in support channels
- Automated notifications from workflow results
