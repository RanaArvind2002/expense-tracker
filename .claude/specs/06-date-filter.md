---
# Spec: Date Filter

## Overview
Adds a date-range filter to the profile page that lets logged-in users filter their expense transactions by start and end dates. The `/profile` route must read optional `start_date` and `end_date` query parameters, apply them to the `expenses` query with parameterized SQL, and pass filtered results to `profile.html`.

## Depends on
- Step 5: Profile Page (`/profile` route and `profile.html` exist)
- Step 1: Database setup (`expenses` table with `date` column exists)

## Routes
- `GET /profile` — modify existing route to accept optional `?start_date=YYYY-MM-DD` and `?end_date=YYYY-MM-DD` query params — logged-in only

No new routes.

## Database changes
No database changes. The existing `expenses` table (from `database/db.py`) already has a `date TEXT NOT NULL` column. The filter uses `WHERE date BETWEEN ? AND ?` or conditional `>= ?` / `<= ?` clauses with parameterized queries.

## Templates
- **Modify:** `templates/profile.html` — add a date filter form above the transactions table with two `<input type="date">` fields (`start_date`, `end_date`) and a submit button; keep extending `base.html`
- **Modify:** `templates/profile.html` — display the current filter values if set so users see what is applied

No new templates.

## Files to change
- `app.py` — update `/profile` route:
  - Read `request.args.get("start_date")` and `request.args.get("end_date")`
  - If either is provided, include `date >= ?` and/or `date <= ?` conditions in the parameterized `SELECT` query for transactions and aggregates
  - Pass `start_date` and `end_date` back to the template so the form retains selected values
- `templates/profile.html` — add date filter form (see Templates section above)
- `static/css/profile.css` — add styles for the date filter form using theme variables (`--border`, `--paper-card`, etc.)

## Files to create
- `static/css/profile-filter.css` (optional) — page-specific filter styles, or extend existing `profile.css`

No required new files; styles can be added to existing `profile.css`.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via `get_db()`
- Parameterised queries only (`?` placeholders) — never f-strings or string concatenation in SQL
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables (`--ink`, `--paper-card`, `--border`, `--accent`) — never hardcode hex values
- All templates extend `base.html`
- Authentication guard: check `session.get("user_id")`; if absent, redirect with `redirect(url_for("login"))`
- DB logic stays in `database/db.py`; route functions only call DB helpers and render templates
- `get_db()` must run `PRAGMA foreign_keys = ON`
- Filter should work when only `start_date` is provided, only `end_date` is provided, both, or neither (show all)
- Date comparison in SQLite: `date >= ?` and `date <= ?` work correctly with `TEXT` date strings in `YYYY-MM-DD` format

## Definition of done
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] Visiting `/profile` while logged in returns HTTP 200
- [ ] Profile shows all transactions when no date filter is applied
- [ ] Profile shows only transactions within the selected date range when `start_date` and `end_date` are set
- [ ] Profile shows only transactions on or after `start_date` when only `start_date` is set
- [ ] Profile shows only transactions on or before `end_date` when only `end_date` is set
- [ ] The date filter form retains the selected `start_date` and `end_date` after submission
- [ ] All SQL queries use `?` parameter placeholders (no f-strings in SQL)
- [ ] Date filter uses native `<input type="date">` elements
- [ ] Filter form uses CSS variables from theme, no hardcoded hex colors
- [ ] No new pip packages added
