import unittest

from app import app

class AssignmentApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_rejects_invalid_course_id(self):
        response = self.client.post(
            "/api/assignments",
            json={
                "title": "Invalid Course Test",
                "due_date": "2026-11-25",
                "course_id": 999,
                "estimated_hours": 1.5,
                "importance": 3
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "The selected course does not exist."
        )

    def test_rejects_invalid_estimated_hours(self):
        response = self.client.post(
            "/api/assignments",
            json={
                "title": "Invalid Hours Test",
                "due_date": "2026-11-25",
                "course_id": 1,
                "estimated_hours": 0,
                "importance": 3
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Estimated hours must be greater than zero."
        )

    def test_rejects_invalid_importance(self):
        response = self.client.post(
            "/api/assignments",
            json={
                "title": "Invalid Importance Test",
                "due_date": "2026-11-25",
                "course_id": 1,
                "estimated_hours": 1.5,
                "importance": 6
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Importance must be between 1 and 5."
        )

    def test_rejects_invalid_due_date(self):
        response = self.client.post(
            "/api/assignments",
            json={
                "title": "Invalid Date Test",
                "due_date": "not-a-date",
                "course_id": 1,
                "estimated_hours": 1.5,
                "importance": 3
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Due date must be a valid date."
        )

if __name__ == "__main__":
    unittest.main()