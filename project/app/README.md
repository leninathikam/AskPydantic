# Pydantic doc agent (Day 6 homework)

Same layout as `course/app`, but indexes **`pydantic/pydantic`** with **chunking** (see Days 1–4 homework).

```bash
cd project/app
uv sync
uv run streamlit run app.py
```

Deploy on Streamlit Cloud with secrets `OPENAI_API_KEY`. Export dependencies:

```bash
uv export --no-dev --no-hashes -o requirements.txt
```
