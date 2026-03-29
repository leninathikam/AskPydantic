# AskPydantic

An AI-powered assistant that lets you chat with the [Pydantic](https://github.com/pydantic/pydantic) GitHub repository, search its code and docs, and get context-aware answers from indexed documentation chunks.

This repository contains:

- **`project/`** — homework notebooks (ingest, search, agents, evaluation) and **`project/app/`** — a modular **Streamlit** + **CLI** app that indexes chunked Pydantic docs with [minsearch](https://github.com/alexeygrigorev/minsearch) and answers via [Pydantic AI](https://ai.pydantic.dev/).
- **`course/`** — parallel course notebooks and **`course/app/`** — FAQ demo for [DataTalksClub/faq](https://github.com/DataTalksClub/faq).
- **`project/eval/`** / **`course/eval/`** — optional notebooks for **evaluation** workflows (Day 7: portfolio + README metrics).

## Quick start (Pydantic app)

```bash
cd project/app
uv sync
# Set OPENAI_API_KEY (e.g. copy .env.example to repo root as .env)
uv run streamlit run app.py
```

```bash
uv run python main.py   # CLI
```

See **`project/Day_06_homework.ipynb`** and **`project/app/README.md`** for deployment notes. For polishing the repo for employers, see **`project/Day_07_homework.ipynb`**.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- `OPENAI_API_KEY` for the LLM (never commit real keys; use `.env` locally and Streamlit/GitHub secrets in production)

## License

Course materials follow your course terms; application code is provided as-is for learning.
