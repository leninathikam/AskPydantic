# FAQ agent app (Day 6)

Modular code for the **DataTalksClub/faq** agent: ingest → search tool → Pydantic AI → optional JSON logs.

## Setup

```bash
cd course/app
uv sync
```

Set `OPENAI_API_KEY` in `ai_hero/.env` or export it in the shell.

## CLI

```bash
uv run python main.py
```

## Streamlit (local)

```bash
uv run streamlit run app.py
```

## Deploy (Streamlit Cloud)

1. Push this repo to GitHub.
2. Point Streamlit Cloud at `course/app` and `app.py` (or adjust root path).
3. Add a secret: `OPENAI_API_KEY=...`
4. Optional: `LOGS_DIRECTORY=/tmp/logs` if you need a writable log folder.

Export lockfile requirements for platforms that do not use `uv`:

```bash
uv export --no-dev --no-hashes -o requirements.txt
```
