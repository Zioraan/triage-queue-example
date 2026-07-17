# Triage Queue CLI Implementation

## Progress

- [x] Create patient.py with validated Patient
- [x] Create triage_queue.py with three deques and five ops
- [x] Create main.py text menu CLI
- [x] Write DESIGN.md
- [x] Add test_triage_queue.py
- [x] Reconcile README; project-structure.md; progress.md; archive plan

## Approach

Use three `collections.deque`s (one per triage level 1–3). Enqueue appends to the matching level deque; dequeue/peek prefer level 1, then 2, then 3. FIFO within a level is natural deque order.

## File layout

- `patient.py` — Patient model + validation
- `triage_queue.py` — TriageQueue with five ops
- `main.py` — Text menu CLI
- `DESIGN.md` — Structure choice + concurrency note
- `test_triage_queue.py` — Unit tests
- `README.md` — Run/layout docs

## Completed

All deliverables implemented and verified with `python -m unittest test_triage_queue.py` (12 tests OK).
