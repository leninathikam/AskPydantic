"""Load markdown from GitHub (zip) and build a minsearch index."""

from __future__ import annotations

import io
import zipfile
from collections.abc import Callable
from typing import Any

import frontmatter
import requests
from minsearch import Index


def read_repo_data(repo_owner: str, repo_name: str) -> list[dict[str, Any]]:
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main"
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    repository_data: list[dict[str, Any]] = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    for file_info in zf.infolist():
        fn_lower = file_info.filename.lower()
        if not (fn_lower.endswith(".md") or fn_lower.endswith(".mdx")):
            continue
        try:
            with zf.open(file_info) as f_in:
                raw = f_in.read().decode("utf-8", errors="ignore")
                post = frontmatter.loads(raw)
                data = post.to_dict()
                _, filename_repo = file_info.filename.split("/", maxsplit=1)
                data["filename"] = filename_repo
                repository_data.append(data)
        except Exception:
            continue
    zf.close()
    return repository_data


def sliding_window(seq: str, size: int, step: int) -> list[dict[str, Any]]:
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")
    n = len(seq)
    result: list[dict[str, Any]] = []
    for i in range(0, n, step):
        batch = seq[i : i + size]
        result.append({"start": i, "chunk": batch})
        if i + size >= n:
            break
    return result


def chunk_documents(
    docs: list[dict[str, Any]], *, size: int = 2000, step: int = 1000
) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for doc in docs:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop("content", "") or ""
        for ch in sliding_window(doc_content, size=size, step=step):
            ch = ch.copy()
            ch.update(doc_copy)
            chunks.append(ch)
    return chunks


def index_data(
    repo_owner: str,
    repo_name: str,
    *,
    doc_filter: Callable[[dict[str, Any]], bool] | None = None,
    chunk: bool = False,
    chunking_params: dict[str, int] | None = None,
    text_fields: list[str] | None = None,
    max_docs: int | None = None,
) -> Index:
    docs = read_repo_data(repo_owner, repo_name)
    if doc_filter is not None:
        docs = [d for d in docs if doc_filter(d)]
    if chunk:
        params = chunking_params or {"size": 2000, "step": 1000}
        docs = chunk_documents(docs, **params)
    if max_docs is not None:
        docs = docs[:max_docs]
    fields = text_fields or ["chunk", "title", "description", "filename"]
    index = Index(text_fields=fields, keyword_fields=[])
    index.fit(docs)
    return index
