import unittest

from roster_report.core import build_report


class BuildReportTests(unittest.TestCase):
    def test_normalizes_sorts_and_applies_rules(self) -> None:
        report = build_report(
            [
                {
                    "id": "b-2",
                    "name": " bia luz ",
                    "department": "ops",
                    "hours": "7",
                    "training_required": "yes",
                },
                {
                    "id": "a-1",
                    "name": "ana lima",
                    "department": "school",
                    "hours": "2",
                    "training_required": "sim",
                },
            ]
        )
        self.assertEqual([record["id"] for record in report["records"]], ["A-1", "B-2"])
        self.assertEqual(report["records"][0]["priority"], "urgent")
        self.assertEqual(report["summary"], {"accepted": 2, "rejected": 0, "urgent": 1})

    def test_keeps_valid_rows_when_one_row_is_invalid(self) -> None:
        report = build_report(
            [
                {
                    "id": "a",
                    "name": "Ana",
                    "department": "ops",
                    "hours": "3",
                    "training_required": "no",
                },
                {
                    "id": "b",
                    "name": "Bia",
                    "department": "ops",
                    "hours": "broken",
                    "training_required": "no",
                },
            ]
        )
        self.assertEqual(report["summary"]["accepted"], 1)
        self.assertEqual(report["summary"]["rejected"], 1)
        self.assertIn("hours must be", report["errors"][0])


if __name__ == "__main__":
    unittest.main()
