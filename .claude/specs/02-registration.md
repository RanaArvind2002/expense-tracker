---
# Spec: Registration

## Overview
Implement user registration for Spendly. The `/register` route currently only renders the form (`register.html`). This step makes it functional: handle POST submissions, validate inputs, hash passwords with `werkzeug`, insert users into the SQLite `users` table via `database/db.py`, and redirect or show errors. This builds directly on Step 1 (DB setup) and is required before authentication flows (login/logout) can work.

## Depends on
- Step 1 (DB setup): `database/db.py` must have `get_db()`, `init_db()`, `seed_db()`; `users` table must exist with `email` UNIQUE and `password_hash`.

## Routes
- `GET /register` — render `register.html` (existing, modify to show errors/success messages)
- `POST /register` — process form, create user, redirect or return error — access: public

## Database changes
No new tables or columns needed. The `users` table from Step 1 is sufficient:
- `name` (TEXT NOT NULL)
- `email` (TEXT UNIQUE NOT NULL)
- `password_hash` (TEXT NOT NULL)
- `created_at` (TEXT DEFAULT datetime('now'))

## Templates
- **Modify:** `templates/register.html` — add `success` message display block; keep existing form and error display.
- **Create:** `templates/register_success.html` — optional confirmation page after successful registration (or redirect to `/login`).

## Files to change
- `app.py` — add POST handler for `/register`, import `get_db`, use parameterized queries, hash password with `werkzeug.security.generate_password_hash`
- `templates/register.html` — add success message block

## Files to create
- `.claude/specs/02-registration.md` (this spec)

## New dependencies
No new pip packages. Use existing `werkzeug.security` (already in `requirements.txt`).

## Rules for implementation
- No SQLAlchemy or ORMs — use `sqlite3` via `database/db.py`
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables from `style.css` — never hardcode hex values (e.g., `--ink`, `--paper-card`)
- All templates extend `base.html`
- Handle `sqlite3.IntegrityError` for duplicate emails gracefully (return error message, not crash)
- Route function has one responsibility: fetch data/process form, render template
- Never put DB logic in route functions — keep queries in `database/db.py` or call `get_db()` and use parameterized SQL

## Definition of done
- [ ] `GET /register` renders form with no errors when no form submitted
- [ ] `POST /register` creates a new user with hashed password in `spendly.db`
- [ ] Duplicate email shows an error message on `register.html` without crashing
- [ ] Invalid/missing fields are handled (basic validation: required fields present)
- [ ] Password is stored as a hash, not plain text
- [ ] All SQL uses parameterized queries
- [ ] Template extends `base.html` and uses CSS variables
- [ ] App runs on port 5001 without errors (`python app.py`)
