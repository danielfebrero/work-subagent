# work-subagent

A dependency-free Python command-line validator for audit observation logs.

## Contract

Each non-empty line must be a JSON object with non-empty string fields:
`timestamp`, `run_id`, `actor`, `event`, `target`, `evidence`, `confidence`.
Timestamps must be timezone-aware ISO 8601 dates. Allowed events are
`file_read`, `tool_call`, `tool_result`, `file_change`, `final_answer`.
Confidence is `observed` or `inferred`. Extra fields are preserved.
Errors include the source line number. Invalid input returns exit status 1;
valid input returns 0 and an event count. Empty logs are valid.

## Usage

Requires Python 3.11+; no external dependencies.

```sh
python3 -m unittest discover -s tests -v
python3 auditlog.py path/to/OBSERVATIONS.jsonl
```

## Layout

- `auditlog.py`: parser and command-line entry point.
- `tests/test_auditlog.py`: regression tests.

