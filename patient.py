"""Patient model for the triage priority queue."""

from __future__ import annotations

from datetime import datetime


class Patient:
    """A patient waiting in the triage queue."""

    def __init__(
        self,
        name: str,
        triage_level: int,
        arrived_at: datetime | None = None,
    ) -> None:
        cleaned_name = name.strip() if isinstance(name, str) else ""
        if not cleaned_name:
            raise ValueError("Patient name cannot be blank.")

        if not isinstance(triage_level, int) or isinstance(triage_level, bool):
            raise ValueError("Triage level must be an integer from 1 to 3.")
        if triage_level not in (1, 2, 3):
            raise ValueError("Triage level must be an integer from 1 to 3.")

        self.name = cleaned_name
        self.triage_level = triage_level
        self.arrived_at = arrived_at if arrived_at is not None else datetime.now()

    def __repr__(self) -> str:
        arrived = self.arrived_at.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Patient(name={self.name!r}, triage_level={self.triage_level}, "
            f"arrived_at={arrived})"
        )

    def display(self) -> str:
        """Human-readable line for CLI listing."""
        arrived = self.arrived_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"[Level {self.triage_level}] {self.name} (arrived {arrived})"
