# Lab 5: Static Code Analysis

## Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Broad exception handling | Code quality / reliability | Verify report | Bare except blocks hide unexpected failures. | Catch expected exceptions and handle them explicitly. |
| Mutable default argument | Bug risk | Verify report | The default zone_records list is reused across calls. | Change the default to None and initialize a new list. |
| Inconsistent expiry date | Functional bug | Verify report | The demo uses a date format different from the parser. | Use YYYY-MM-DD consistently and validate the date. |
| Invalid parking zone | Input validation | Verify report | A permit is registered for zone Z, outside A-C. | Validate zones before registering. |
| Unsafe or unmanaged file handling | Reliability | Verify report | Files are opened without context managers. | Use with open(...) and handle expected errors. |