---
description: Research a superannuation, financial services, or regulatory topic — returns a cited research brief with APRA/ASIC/ATO sources, industry benchmarks, and global comparisons
argument-hint: <topic or question>
---

Use the `research-agent` subagent to research: $ARGUMENTS

The research-agent will:
1. Search APRA, ASIC, ATO, and industry sources (ASFA, AIST, Mercer)
2. Synthesise findings with specific citations and data vintage
3. Apply regulatory context where relevant
4. Compare to global pension systems where useful
5. Save a research brief to `outputs/YYYY-MM-DD_research_<topic>.md`

When the research-agent returns, summarise the headline findings and the brief's location. If any regulatory flags were raised, highlight those explicitly.
