"""Pydantic AI agent with a search tool."""

from __future__ import annotations

from minsearch import Index
from pydantic_ai import Agent

import search_tools

SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions about documentation.

Use the search tool to find relevant information from the course materials before answering questions.

If you can find specific information through search, use it to provide accurate answers.

Always include references by citing the filename of the source material you used.
Build links using the repository base:
https://github.com/{repo_owner}/{repo_name}/blob/main/
Format: [LINK TITLE](FULL_GITHUB_LINK)

If the search doesn't return relevant results, let the user know and provide general guidance.
""".strip()


def init_agent(index: Index, repo_owner: str, repo_name: str) -> Agent:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        repo_owner=repo_owner, repo_name=repo_name
    )
    search_tool = search_tools.SearchTool(index=index)
    return Agent(
        "openai:gpt-4o-mini",
        name="gh_agent",
        instructions=system_prompt,
        tools=[search_tool.search],
    )
