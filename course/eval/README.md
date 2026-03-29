# Evaluation workflows (course)

Move **question generation** and **LLM-as-judge** experiments here so `Day_05_Evaluation.ipynb` stays a lesson file, not the only place eval code lives.

| Notebook | Purpose |
|----------|---------|
| `data-gen.ipynb` | Sample FAQ rows → synthetic questions → run agent → `logs/` with `source='ai-generated'` |
| `evaluations.ipynb` | Load logs → `evaluate_log_record_sync` → Pandas pass rates |

Point your repo **README** at this folder and paste **summary metrics** into an **Evaluation** section.
