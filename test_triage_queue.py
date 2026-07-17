"""Unit tests for Patient and TriageQueue."""

from __future__ import annotations

import unittest
from datetime import datetime

from patient import Patient
from triage_queue import TriageQueue


class PatientValidationTests(unittest.TestCase):
    def test_valid_patient(self) -> None:
        arrived = datetime(2026, 7, 17, 8, 0, 0)
        patient = Patient("Ada", 1, arrived_at=arrived)
        self.assertEqual(patient.name, "Ada")
        self.assertEqual(patient.triage_level, 1)
        self.assertEqual(patient.arrived_at, arrived)

    def test_strips_name_whitespace(self) -> None:
        patient = Patient("  Ada  ", 2)
        self.assertEqual(patient.name, "Ada")

    def test_blank_name_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Patient("", 1)
        with self.assertRaises(ValueError):
            Patient("   ", 1)

    def test_invalid_triage_level_rejected(self) -> None:
        for level in (0, 4, -1):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    Patient("Ada", level)

    def test_non_integer_triage_level_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Patient("Ada", 1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            Patient("Ada", True)  # type: ignore[arg-type]


class TriageQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = TriageQueue()

    def test_empty_dequeue_and_peek_return_none(self) -> None:
        self.assertIsNone(self.queue.dequeue())
        self.assertIsNone(self.queue.peek())

    def test_priority_level_1_before_2_before_3(self) -> None:
        p3 = Patient("Low", 3)
        p2 = Patient("Mid", 2)
        p1 = Patient("High", 1)
        self.queue.enqueue(p3)
        self.queue.enqueue(p2)
        self.queue.enqueue(p1)

        self.assertEqual(self.queue.dequeue(), p1)
        self.assertEqual(self.queue.dequeue(), p2)
        self.assertEqual(self.queue.dequeue(), p3)
        self.assertIsNone(self.queue.dequeue())

    def test_fifo_within_same_level(self) -> None:
        first = Patient("First", 2)
        second = Patient("Second", 2)
        third = Patient("Third", 2)
        self.queue.enqueue(first)
        self.queue.enqueue(second)
        self.queue.enqueue(third)

        self.assertEqual(self.queue.dequeue(), first)
        self.assertEqual(self.queue.dequeue(), second)
        self.assertEqual(self.queue.dequeue(), third)

    def test_duplicate_levels_ordered_by_enqueue_arrival(self) -> None:
        a = Patient("A", 1)
        b = Patient("B", 1)
        c = Patient("C", 1)
        self.queue.enqueue(a)
        self.queue.enqueue(b)
        self.queue.enqueue(c)
        self.assertEqual([p.name for p in self.queue.list_queue()], ["A", "B", "C"])

    def test_peek_does_not_remove(self) -> None:
        patient = Patient("Ada", 1)
        self.queue.enqueue(patient)
        self.assertEqual(self.queue.peek(), patient)
        self.assertEqual(self.queue.peek(), patient)
        self.assertEqual(self.queue.stats()["total"], 1)
        self.assertEqual(self.queue.dequeue(), patient)

    def test_list_queue_and_stats_consistency(self) -> None:
        self.queue.enqueue(Patient("L3a", 3))
        self.queue.enqueue(Patient("L1a", 1))
        self.queue.enqueue(Patient("L2a", 2))
        self.queue.enqueue(Patient("L1b", 1))
        self.queue.enqueue(Patient("L3b", 3))

        names = [p.name for p in self.queue.list_queue()]
        self.assertEqual(names, ["L1a", "L1b", "L2a", "L3a", "L3b"])

        stats = self.queue.stats()
        self.assertEqual(stats, {"level_1": 2, "level_2": 1, "level_3": 2, "total": 5})

        self.queue.dequeue()
        stats_after = self.queue.stats()
        self.assertEqual(stats_after["total"], 4)
        self.assertEqual(stats_after["level_1"], 1)
        self.assertEqual(
            [p.name for p in self.queue.list_queue()],
            ["L1b", "L2a", "L3a", "L3b"],
        )

    def test_enqueue_rejects_non_patient(self) -> None:
        with self.assertRaises(TypeError):
            self.queue.enqueue("not a patient")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
