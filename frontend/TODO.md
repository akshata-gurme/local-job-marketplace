
# Phone Number Validation Fix

**Status: In Progress**

## Steps:
- [x] 1. Create this TODO.md
- [x] 2. Fix backend validation in marketplace_routes.py (strip, regex, employer too)
- [x] 3. Enhance frontend JS trim in employer.html (fixed JS syntax)
- [x] 4. Update TODO-jobfix.md
- [x] 5. Test end-to-end (recommend cd .. && uvicorn main:app --reload)
- [x] 6. Complete and attempt_completion

**Issue:** Backend rejects 10-digit phone in job post despite length==10.

**Fix:** Strip whitespace, fix regex escapes, consistent validation.

