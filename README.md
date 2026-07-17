# triage-queue-example

Simple CLI-based patient triage priority queue in Python.

## Run

```bash
python main.py
```

## Tests

```bash
python -m unittest test_triage_queue.py
```

## Layout

| File | Role |
|------|------|
| `patient.py` | `Patient` model (name, triage level 1–3, arrival time) |
| `triage_queue.py` | `TriageQueue` priority queue (three deques by level) |
| `main.py` | Text menu CLI |
| `DESIGN.md` | Data-structure and concurrency notes |
| `test_triage_queue.py` | Unit tests |
| `HANDOFF.md` | Assignment / handoff context |

## Queue operations

- `enqueue(patient)` — add a patient to their triage-level queue
- `dequeue()` — remove and return the next patient (level 1 before 2 before 3; FIFO within a level), or `None` if empty
- `peek()` — return the next patient without removing them, or `None` if empty
- `list_queue()` — ordered snapshot of everyone waiting
- `stats()` — counts per level and total

Priority: triage level `1` is highest, `3` is lowest. Same-level patients keep enqueue (FIFO) order.
