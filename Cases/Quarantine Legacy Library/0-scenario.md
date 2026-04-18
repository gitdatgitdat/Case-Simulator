# Case: Quarantine Legacy Library

## Summary
A malware or vulnerability scanner flagged an older shared library on a Linux endpoint. We need to determine whether the library is actively required before removing it.

## Objective
Safely isolate the file without deleting it, then observe the system for dependency or service failures.

## Approach
Move the file into a quarantine directory and preserve it for rollback.

## Success Criteria
- File is removed from original path
- System remains stable
- No application or dependency errors are observed
- File can be restored quickly if needed