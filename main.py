"""CLI menu for the patient triage priority queue."""

from __future__ import annotations

from patient import Patient
from triage_queue import TriageQueue


def print_menu() -> None:
    print("\n=== Patient Triage Queue ===")
    print("1. Enqueue patient")
    print("2. Dequeue next patient")
    print("3. Peek next patient")
    print("4. List queue")
    print("5. Show stats")
    print("6. Exit")


def handle_enqueue(queue: TriageQueue) -> None:
    name = input("Patient name: ").strip()
    level_raw = input("Triage level (1=highest, 3=lowest): ").strip()
    try:
        triage_level = int(level_raw)
        patient = Patient(name=name, triage_level=triage_level)
    except ValueError as exc:
        print(f"Could not enqueue: {exc}")
        return

    queue.enqueue(patient)
    print(f"Enqueued: {patient.display()}")


def handle_dequeue(queue: TriageQueue) -> None:
    patient = queue.dequeue()
    if patient is None:
        print("Queue is empty.")
        return
    print(f"Dequeued: {patient.display()}")


def handle_peek(queue: TriageQueue) -> None:
    patient = queue.peek()
    if patient is None:
        print("Queue is empty.")
        return
    print(f"Next: {patient.display()}")


def handle_list(queue: TriageQueue) -> None:
    patients = queue.list_queue()
    if not patients:
        print("Queue is empty.")
        return
    print("Current queue (highest priority first):")
    for index, patient in enumerate(patients, start=1):
        print(f"  {index}. {patient.display()}")


def handle_stats(queue: TriageQueue) -> None:
    stats = queue.stats()
    print("Queue stats:")
    print(f"  Level 1: {stats['level_1']}")
    print(f"  Level 2: {stats['level_2']}")
    print(f"  Level 3: {stats['level_3']}")
    print(f"  Total:   {stats['total']}")


def main() -> None:
    queue = TriageQueue()
    handlers = {
        "1": handle_enqueue,
        "2": handle_dequeue,
        "3": handle_peek,
        "4": handle_list,
        "5": handle_stats,
    }

    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if choice == "6":
            print("Goodbye.")
            break

        handler = handlers.get(choice)
        if handler is None:
            print("Invalid option. Enter a number from 1 to 6.")
            continue

        try:
            handler(queue)
        except Exception as exc:  # noqa: BLE001 — keep CLI loop alive
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
