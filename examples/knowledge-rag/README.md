# Knowledge RAG

> Ingest documents into the LVNG knowledge graph, then build a retrieval-augmented chat that answers questions using your data.

## What You'll Build

```
Documents → Ingest API → Knowledge Graph → Search API → Agent + Context → Answer
```

A complete RAG pipeline that:
1. Ingests text documents into your knowledge graph
2. Searches for relevant context given a user question
3. Passes context to an AI agent for grounded answers
4. Tracks sources and confidence scores

## Use Cases
- Internal documentation Q&A bot
- Customer support with product knowledge
- Legal document analysis
- Onboarding assistant for new team members
