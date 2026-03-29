"""CLI: chunked Pydantic docs + agent."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import ingest
import logs
import search_agent
from dotenv import load_dotenv

REPO_OWNER = "pydantic"
REPO_NAME = "pydantic"
MAX_CHUNKS = 400


def _load_env() -> None:
    p = Path(__file__).resolve().parent
    for _ in range(8):
        if (p / ".env").is_file():
            load_dotenv(p / ".env")
            return
        if p.parent == p:
            break
        p = p.parent


def initialize_index():
    _load_env()
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY (e.g. in ai_hero/.env)")

    print(f"Indexing {REPO_OWNER}/{REPO_NAME} (chunked, max {MAX_CHUNKS})…")
    index = ingest.index_data(
        REPO_OWNER,
        REPO_NAME,
        chunk=True,
        max_docs=MAX_CHUNKS,
    )
    print("Indexing done.")
    return index


def initialize_agent(index):
    print("Initializing agent…")
    return search_agent.init_agent(index, REPO_OWNER, REPO_NAME)


def main():
    index = initialize_index()
    agent = initialize_agent(index)
    print("\nReady. Type 'stop' to exit.\n")

    while True:
        question = input("Your question: ")
        if question.strip().lower() == "stop":
            print("Goodbye!")
            break

        response = asyncio.run(agent.run(user_prompt=question))
        logs.log_interaction_to_file(agent, response.new_messages())
        print("\n", response.output, "\n")


if __name__ == "__main__":
    main()
