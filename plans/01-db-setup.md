# Plan: DB Setup (Step 1)

## Context
The `database/db.py` file is a stub. The spec (`spec/01-db-setup.md`) requires implementing SQLite helpers (`get_db`, `init_db`, `seed_db`) so future routes (auth, expenses) have a working data layer. `database/db.py` currently only has comments; `app.py` lacks DB imports/startup calls.

## Approach
- Modify `database/db.py`: implement `get_db()` (sqlite3 connection to `spendly.db`, `row_factory = sqlite3.Row`, `PRAGMA foreign_keys = ON`), `init_db()` (`CREATE TABLE IF NOT EXISTS` for `users` and `expenses`), `seed_db()` (check if users table empty; if so insert demo user with `werkzeug.security.generate_password_hash`, and 8 sample expenses across 7 categories with `YYYY-MM-DD` dates in current month, parameterized queries only).
- Modify `app.py`: import `get_db`, `init_db`, `seed_db` from `database.db`; call `init_db()` and `seed_db()` inside `with app.app_context():` before `app.run()`.
- No new files; no new pip packages.

## Verification
Run `python app.py` — app starts on port 5001 without errors. Check `spendly.db` exists with both tables, demo user (`demo@spendly.com` with hashed password), and 8 expenses. Re-run to confirm no duplicate seed data.
