import unittest
from datetime import date

from app import calculate_priority

class PriorityTests(unittest.TestCase):
    def test_due_today_high_importance(self):
        score = calculate_priority(
            "2026-11-18",
            5,
            today=date(2026, 11, 18)
        )

        self.assertEqual(score, 20)

    def test_due_later_has_lower_urgency(self):
        score = calculate_priority(
            "2026-12-01",
            3,
            today=date(2026, 11, 18)
        )

        self.assertEqual(score, 7)

if __name__ == "__main__":
    unittest.main()