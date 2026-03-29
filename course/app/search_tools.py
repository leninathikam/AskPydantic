"""Search tool used by the Pydantic AI agent."""

from __future__ import annotations

from typing import Any

from minsearch import Index


class SearchTool:
    def __init__(self, index: Index) -> None:
        self.index = index

    def search(self, query: str) -> list[Any]:
        """
        Perform a text-based search on the FAQ index.

        Args:
            query: The search query string.

        Returns:
            Up to 5 search results from the index.
        """
        return self.index.search(query, num_results=5)
