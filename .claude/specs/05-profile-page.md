---
# Spec: Profile Page Backend Routes

## Overview
This feature replaces the hardcoded `/profile` stub with real database-backed routes. The `/profile` route must query the `users` and `expenses` tables to display the logged-in user's info, summary statistics, recent transactions, and category breakdowns. This connects the UI design from Step 4 to the actual database layer, making the profile page fully functional.

## Depends on
- Step 1: Database setup (users and expenses tables must exist)
- Step 2: Registration (users must be creatable)
- Step 3: Login + Logout (session must be set; `/profile` must be protected)
- Step 4: Profile Page Design (`profile.html` and `profile.css` must exist)

## Routes
- `GET /profile` — render profile page with live user data and expense statistics — logged-in only (redirect to `/login` if not authenticated)

No new routes.

## Database changes
No database changes. The existing `users` and `expenses` tables (from `database/db.py`) are sufficient. Queries use parameterized `SELECT` statements against these tables.

## Templates
- **Modify:** `templates/profile.html` — no structural changes required; it already consumes `user`, `stats`, `transactions`, and `categories` variables from `app.py`. Ensure it continues to extend `base.html`.

No new templates.

## Files to change
- `app.py` — replace the `/profile` stub with a database-backed route:
  - Query current user by `session["user_id"]`
  - Aggregate expenses (total spent, transaction count, top category) via parameterized SQL
  - Pass computed context variables (`user`, `stats`, `transactions`, `categories`) to `profile.html`
- `database/db.py` — add a helper query (optional but recommended) for expense aggregation; keep `get_db()` unchanged.

## Files to create
No new files required.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via `get_db()`
- Parameterised queries only (`?` placeholders) — never f-strings or string concatenation in SQL
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables (`--ink`, `--paper-card`, `--border`, `--accent`) — never hardcode hex values in templates or styles
- All templates extend `base.html` (`profile.html` already does this)
- Authentication guard: check `session.get("user_id")`; if absent, redirect with `redirect(url_for("login"))`
- DB logic must stay in `database/db.py`; route functions only call DB helpers and render templates
- `get_db()` must run `PRAGMA foreign_keys = ON` (already implemented)
- Aggregate queries: count transactions, sum amounts, and compute top category via `GROUP BY category`

## Definition of done
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] Visiting `/profile` while logged in returns HTTP 200
- [ ] Profile page shows the real user name and email from the `users` table
- [ ] Profile page shows real total spent computed from `expenses`
- [ ] Profile page shows real transaction count from `expenses`
- [ ] Profile page shows real top category computed from `expenses`
- [ ] Profile page displays at least three real recent transactions from `expenses`
- [ ] Profile page displays category breakdown with real totals from `expenses`
- [ ] All SQL queries use `?` parameter placeholders
- [ ] No new pip packages added
