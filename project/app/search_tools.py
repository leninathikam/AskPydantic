"""Search tool used by the Pydantic AI agent."""

from __future__ import annotations

from typing import Any

from minsearch import Index


class SearchTool:
    def __init__(self, index: Index) -> None:
        self.index = index

    def doc_search(self, query: str) -> list[Any]:
        """
        Search indexed documentation chunks.

        Args:
            query: The search query.

        Returns:
            Up to 5 matching chunks with metadata.
        """
        return self.index.search(query, num_results=5)
