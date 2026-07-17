# Progress

## 2026-07-17 — Triage Queue CLI

- Added `Patient` with validation for blank names and triage levels outside 1–3.
- Implemented `TriageQueue` with three `deque`s (levels 1–3): enqueue, dequeue, peek, list_queue, stats.
- Built text menu CLI in `main.py` that survives invalid input.
- Documented structure and concurrency concerns in `DESIGN.md`.
- Added `unittest` suite covering priority, FIFO, empty ops, and validation failures.
- Reconciled `README.md` with the real file layout.
