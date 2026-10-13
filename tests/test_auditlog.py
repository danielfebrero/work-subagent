import json
import unittest
from auditlog import load_events, validate_event


class AuditLogTests(unittest.TestCase):
    def setUp(self):
        self.event = dict(timestamp='2026-10-13T18:00:00Z', run_id='unit',
                          actor='auditor', event='file_read', target='README.md',
                          evidence='evidence/read.json', confidence='observed')

    def test_valid_event(self):
        self.assertEqual(validate_event(self.event), self.event)

    def test_missing_field(self):
        del self.event['actor']
        with self.assertRaisesRegex(ValueError, 'actor'):
            validate_event(self.event)

    def test_naive_timestamp(self):
        self.event['timestamp'] = '2026-10-13T18:00:00'
        with self.assertRaisesRegex(ValueError, 'timezone'):
            validate_event(self.event)

    def test_line_numbers(self):
        with self.assertRaisesRegex(ValueError, 'line 2'):
            load_events(['\n', '{invalid json}\n'])

    def test_blank_lines(self):
        self.assertEqual(load_events(['\n', json.dumps(self.event)]), [self.event])


if __name__ == '__main__':
    unittest.main()
