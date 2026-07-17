# Agent Handoff

## Objective

Build a CLI-based patient triage priority queue project in Python.

The queue must support a `Patient` class with at least:

- `name`
- `triage_level` as an `int` from `1` to `3`
- `arrived_at`

Priority rules:

- triage level `1` is highest priority
- triage level `3` is lowest priority
- within the same triage level, ordering must preserve FIFO / arrival order

Required queue operations:

- `enqueue(patient)`
- `dequeue()`
- `peek()`
- `list_queue()`
- `stats()`

The project also needs:

- a text menu CLI operable from the terminal
- a root-level `DESIGN.md`

Allowed libraries are limited to:

- `collections.deque`
- `heapq`
- `datetime`

Persistence is not required.

## Evaluation Criteria

The implementation should satisfy all of the following:

- `TriageQueue` correctly models a priority queue: level 1 before level 2, level 2 before level 3
- FIFO order is strictly preserved within the same triage level
- all five operations are implemented and work correctly
- empty queue `dequeue()` and `peek()` do not crash
- duplicate triage levels are ordered by arrival
- code is organized into classes with clear responsibilities
- logic is not dumped into `main()`
- `DESIGN.md` explains the internal data structure choice with a concrete reason
- `DESIGN.md` addresses the concurrent mutation / double-processing scenario
- CLI loop is functional and does not crash on invalid input

## Current Repository State

As of July 17, 2026, the repo is almost empty.

Files currently present at the root:

- `README.md`
- `HANDOFF.md`

Important note:

- `README.md` currently says to run `python main.py`, but `main.py` does not exist yet
- `README.md` also lists queue operations, but none of the queue implementation files exist yet

## Suggested Implementation Plan

One clean layout would be:

- `patient.py` for the `Patient` class
- `triage_queue.py` for the queue logic
- `main.py` for the CLI wrapper
- `DESIGN.md` for design decisions and edge-case handling
- optional tests if the environment supports them

## Data Structure Guidance

Two good implementation approaches fit the allowed-library constraint:

1. Three `deque` objects, one per triage level
2. A `heapq` with a stable tie-breaker

Recommendation:

- prefer three `deque` objects if arrival order is defined by enqueue order
- prefer `heapq` if `arrived_at` must control ordering even when patients are enqueued out of chronological order

Whichever approach is chosen, the design note should explain:

- why that structure matches the rubric
- how FIFO is guaranteed for equal-priority patients
- how `peek()` is implemented without corrupting queue state

## Edge Cases To Cover

- empty `dequeue()` returns a safe value such as `None`
- empty `peek()` returns a safe value such as `None`
- invalid triage levels are rejected
- blank patient names are rejected
- same-priority patients remain ordered correctly
- invalid CLI menu input does not crash the app

## Concurrent Mutation Note

The design write-up should include an informal explanation of the double-processing scenario:

- if one worker is choosing a patient while another patient is enqueued, a newly arrived critical patient should affect the next dequeue, not retroactively replace a patient already assigned
- to prevent two workers from processing the same patient, selection and removal would need to happen as one protected operation in a real concurrent system
- for this assignment, a single-threaded CLI is enough, but the design note should still acknowledge the concurrency concern

## Deliverable Checklist

- create the patient model
- create the priority queue class
- implement all five operations
- build the CLI menu
- write `DESIGN.md`
- reconcile `README.md` with the actual file layout
- verify the queue behavior against the rubric
