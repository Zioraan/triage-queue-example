# Design: Triage Priority Queue

## Data structure choice

This project uses **three `collections.deque` objects**, one per triage level (1, 2, and 3).

### Why three deques

- Triage priority is discrete and small (exactly three levels). Routing a patient to `levels[triage_level]` is O(1).
- Level 1 is highest priority and level 3 is lowest. `dequeue()` and `peek()` scan levels in order `1 → 2 → 3` and use the first non-empty deque.
- Arrival order is defined by **enqueue order**. Appending to the rear of a level deque and removing from the front preserves FIFO without a heap tie-breaker.
- A `heapq` would also work with a stable counter, but three deques match the rubric more directly: priority is which deque you look at; FIFO is the deque itself.

`arrived_at` is stored on each `Patient` for display and auditing. It is not used to reorder the queue when patients are enqueued out of chronological order; enqueue sequence is the source of truth for same-level ordering.

## How FIFO is guaranteed within a level

For a given triage level:

1. `enqueue` calls `deque.append(patient)` (rear).
2. `dequeue` calls `deque.popleft()` (front).
3. `list_queue` walks each deque from left to right.

Patients with the same triage level therefore leave in the same order they entered that level.

## How `peek()` works without corrupting state

`peek()` finds the highest-priority non-empty deque and returns `deque[0]` — the front element — without `popleft()`. The queues are unchanged, so a following `dequeue()` returns the same patient.

Empty `peek()` and `dequeue()` return `None` instead of raising.

## Concurrent mutation / double-processing

This CLI is single-threaded: only one menu action runs at a time, so enqueue and dequeue cannot interleave mid-operation.

In a real multi-worker system:

- If worker A has already **dequeued** (selected and removed) a patient, that assignment should stick. A newly enqueued critical patient must not retroactively replace the patient A is already processing; it only affects the **next** dequeue.
- If selection and removal are separate steps, two workers can both “see” the same front patient and both try to process them (double-processing). Selection and removal should be one **protected / atomic** operation (lock, compare-and-swap, or transactional dequeue).
- For this assignment, the single-threaded CLI plus atomic `dequeue()` (popleft as one call) is enough; the note above documents the concurrency concern the design must acknowledge.
