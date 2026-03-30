# Multi-Agent Team

> Deploy a team of specialized agents that collaborate to analyze a business problem — one researches, one analyzes data, and a lead agent synthesizes their findings.

## What You'll Build

```
Lead Agent
  ├── Research Agent  →  gathers web intelligence
  ├── Data Agent      →  analyzes internal metrics
  └── Lead synthesizes both into actionable recommendations
```

A coordinator pattern where:
1. A lead agent receives a business question
2. It delegates research to a web-search specialist
3. Simultaneously delegates data analysis to a metrics specialist
4. Collects both results and produces a unified strategy

## Use Cases
- Cross-functional analysis (marketing + finance + ops)
- Automated due diligence with multiple data sources
- Multi-perspective code review (security + performance + UX)
- Incident response with parallel investigation tracks
