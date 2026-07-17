"""Priority queue for patient triage using one deque per level."""

from __future__ import annotations

from collections import deque
from typing import Optional

from patient import Patient


class TriageQueue:
    """Priority queue: triage level 1 highest, 3 lowest; FIFO within a level."""

    def __init__(self) -> None:
        self._levels: dict[int, deque[Patient]] = {
            1: deque(),
            2: deque(),
            3: deque(),
        }

    def enqueue(self, patient: Patient) -> None:
        """Add a patient to the rear of their triage-level queue."""
        if not isinstance(patient, Patient):
            raise TypeError("enqueue expects a Patient instance.")
        self._levels[patient.triage_level].append(patient)

    def dequeue(self) -> Optional[Patient]:
        """Remove and return the next patient, or None if empty."""
        for level in (1, 2, 3):
            if self._levels[level]:
                return self._levels[level].popleft()
        return None

    def peek(self) -> Optional[Patient]:
        """Return the next patient without removing them, or None if empty."""
        for level in (1, 2, 3):
            if self._levels[level]:
                return self._levels[level][0]
        return None

    def list_queue(self) -> list[Patient]:
        """Return patients in dequeue order: level 1, then 2, then 3 (FIFO each)."""
        ordered: list[Patient] = []
        for level in (1, 2, 3):
            ordered.extend(self._levels[level])
        return ordered

    def stats(self) -> dict[str, int]:
        """Return counts per triage level and total waiting."""
        level_1 = len(self._levels[1])
        level_2 = len(self._levels[2])
        level_3 = len(self._levels[3])
        return {
            "level_1": level_1,
            "level_2": level_2,
            "level_3": level_3,
            "total": level_1 + level_2 + level_3,
        }
