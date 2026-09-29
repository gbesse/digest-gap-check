import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import TEXT, candidates, collect_report_ids


class AuditTests(unittest.TestCase):
    def test_candidates_respect_selection_and_window(self):
        report = {"windowStart": "2026-09-28T00:00:00Z", "windowEnd": "2026-09-29T00:00:00Z", "sections": [{"items": [{"links": {"aihot": "https://x/items/a"}}]}]}
        items = [{"id": "a", "selected": True, "publishedAt": "2026-09-28T12:00:00Z"}, {"id": "b", "selected": True, "publishedAt": "2026-09-28T12:00:00Z"}, {"id": "c", "selected": False, "publishedAt": "2026-09-28T12:00:00Z"}]
        self.assertEqual([r["id"] for r in candidates(report, items)], ["b"])

    def test_languages(self):
        self.assertEqual(set(TEXT), {"en", "fr", "es"})


if __name__ == "__main__":
    unittest.main()
