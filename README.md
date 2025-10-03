
# arXiv-mcp

**arXiv-mcp** is a Model Context Protocol (MCP) server for querying and discovering the latest arXiv papers, built for seamless integration with LLMs and AI agents via the Smithery platform.

## Overview

This tool enables AI applications to fetch, filter, and summarize new arXiv submissions in any category, making it easy to build research assistants, literature review bots, or custom paper discovery workflows. Powered by Smithery MCP, it supports session-based configuration and is ready for deployment.

## Problem Statement

Staying up-to-date with the latest research on arXiv is challenging due to the volume and frequency of new submissions. arXiv-mcp solves this by providing a programmable interface for LLMs and agents to:
- Retrieve daily arXiv postings by category
- Search for papers by keyword
- Return structured metadata (title, authors, summary, link, published date)
- Personalize results with session config (in development currently!)

## Example Usage (LLM Chat)

> **User:**  
Find today's latest papers in the category `quant-ph`. Then curate a list of papers related to quantum computing. 
> 
> **LLM (using arXiv-mcp):**  
> Calls `fetch_current_arxiv_postings_rss(category="quant-ph")`  
> Returns a list of new papers with titles, authors, summaries, and links.

<br>

> **User:**  
> Show me recent arXiv papers about "fluxonium qubits" in quantum computing.
>
> **LLM (using arXiv-mcp):**  
> Calls `keyword_search_arxiv_rss(category="quant-ph", keyword="fluxonium qubits")`  
Returns a list of filtered papers whose title or abstract matches the keyword.

---

## Getting Started

1. **Run the server:**
   ```bash
   uv run dev
   ```

2. **Test interactively:**
   ```bash
   uv run playground
   ```

Your server code is in `src/hello_server/server.py`.  
The server capabilities can be modified there.

---

## Prerequisites

- **Smithery API key:** Get yours at [smithery.ai/account/api-keys](https://smithery.ai/account/api-keys)

---

This code can be deployed by pushing to GitHub and then deploying via [smithery.ai/new](https://smithery.ai/new)
