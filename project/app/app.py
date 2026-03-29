"""Streamlit UI for the Pydantic documentation agent."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

import ingest
import logs
import search_agent

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


_load_env()

st.set_page_config(
    page_title="Pydantic doc agent",
    page_icon="📘",
    layout="centered",
)

if not os.environ.get("OPENAI_API_KEY"):
    st.error("Set **OPENAI_API_KEY** locally or in Streamlit Cloud secrets.")
    st.stop()


@st.cache_resource
def init_agent():
    index = ingest.index_data(
        REPO_OWNER,
        REPO_NAME,
        chunk=True,
        max_docs=MAX_CHUNKS,
    )
    return search_agent.init_agent(index, REPO_OWNER, REPO_NAME)


agent = init_agent()

st.title("📘 Pydantic documentation agent")
st.caption(f"Chunks from **{REPO_OWNER}/{REPO_NAME}** (max {MAX_CHUNKS}).")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def stream_answer(prompt: str):
    result = agent.run_stream_sync(user_prompt=prompt)
    for delta in result.stream_text(delta=True, debounce_by=0.02):
        yield delta
    logs.log_interaction_to_file(agent, result.new_messages())


if prompt := st.chat_input("Ask about Pydantic…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            full = st.write_stream(stream_answer(prompt))

    st.session_state.messages.append({"role": "assistant", "content": full or ""})
