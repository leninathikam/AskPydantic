"""Pydantic AI agent with doc_search over Pydantic repo chunks."""

from __future__ import annotations

from minsearch import Index
from pydantic_ai import Agent

import search_tools

SYSTEM_PROMPT_TEMPLATE = """
You answer questions about the **Pydantic** library using the doc_search tool.

Ground answers in retrieved chunks. Cite source filenames and link to GitHub when helpful:
https://github.com/{repo_owner}/{repo_name}/blob/main/
Format: [short label](FULL_GITHUB_LINK)

If search returns nothing useful, say so and give conservative general guidance.
""".strip()


def init_agent(index: Index, repo_owner: str, repo_name: str) -> Agent:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        repo_owner=repo_owner, repo_name=repo_name
    )
    search_tool = search_tools.SearchTool(index=index)
    return Agent(
        "openai:gpt-4o-mini",
        name="pydantic_doc_agent",
        instructions=system_prompt,
        tools=[search_tool.doc_search],
    )
