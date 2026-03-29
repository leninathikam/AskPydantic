"""CLI entrypoint: index FAQ, run agent, log each turn."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import ingest
import logs
import search_agent
from dotenv import load_dotenv

REPO_OWNER = "DataTalksClub"
REPO_NAME = "faq"


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

    print(f"Starting AI FAQ Assistant for {REPO_OWNER}/{REPO_NAME}")
    print("Initializing data ingestion...")

    def de_only(doc) -> bool:
        return "data-engineering" in (doc.get("filename") or "").lower()

    index = ingest.index_data(REPO_OWNER, REPO_NAME, doc_filter=de_only)
    print("Data indexing completed successfully!")
    return index


def initialize_agent(index):
    print("Initializing search agent...")
    agent = search_agent.init_agent(index, REPO_OWNER, REPO_NAME)
    print("Agent initialized successfully!")
    return agent


def main():
    index = initialize_index()
    agent = initialize_agent(index)
    print("\nReady to answer your questions!")
    print("Type 'stop' to exit the program.\n")

    while True:
        question = input("Your question: ")
        if question.strip().lower() == "stop":
            print("Goodbye!")
            break

        print("Processing your question...")
        response = asyncio.run(agent.run(user_prompt=question))
        logs.log_interaction_to_file(agent, response.new_messages())

        print("\nResponse:\n", response.output)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
