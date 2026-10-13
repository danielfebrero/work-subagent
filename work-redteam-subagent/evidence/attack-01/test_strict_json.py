import json
import unittest
from pathlib import Path
from auditlog import load_events

class StrictJsonRegression(unittest.TestCase):
    def test_reject_non_json_number(self):
        lines = Path("audit-output/maintenance/nonstandard-number.jsonl").read_text().splitlines()
        def reject_constant(token):
            raise ValueError("non-JSON constant: " + token)
        with self.assertRaisesRegex(ValueError, "non-JSON constant: NaN"):
            json.loads(lines[0], parse_constant=reject_constant)
        with self.assertRaisesRegex(ValueError, "line 1"):
            load_events(lines)

if __name__ == "__main__":
    unittest.main(verbosity=2)
