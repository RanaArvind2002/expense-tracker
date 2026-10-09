---
# Spec: Login and Logout

## Overview
Implement the `/login` POST handler and complete `/logout` for Spendly. Currently `/login` only renders the form (GET); it needs to validate email and password, check the user against the SQLite `users` table (via `database/db.py`), compare password hashes with `werkzeug.security.check_password_hash`, and either redirect to `/profile` or show an error. `/logout` must clear the user session and redirect to `/`. This enables basic authentication flow after Step 2 (registration) and is required before profile/expense routes (Steps 4+).

## Depends on
- Step 2 (registration): `users` table must exist with `email` UNIQUE, `password_hash` stored via `werkzeug`
- `database/db.py` with `get_db()` working and `PRAGMA foreign_keys = ON`

## Routes
- `GET /login` — render `login.html` (existing, keep)
- `POST /login` — validate email/password, check user, redirect or show error — access: public
- `GET /logout` — clear session, redirect to `/` — access: logged-in (or public, safe either way)

## Database changes
No new tables or columns. Uses existing `users` table:
- `email` (TEXT UNIQUE NOT NULL)
- `password_hash` (TEXT NOT NULL)

## Templates
- **Modify:** `templates/login.html` — ensure error message block is present (already there); keep form action `/login` with method POST
- **Modify:** `templates/base.html` — add `profile` link in navbar when user is logged in (optional, or keep simple for this step)
- **Create:** None required (logout redirects; no dedicated page needed)

## Files to change
- `app.py` — add POST `/login`, implement `/logout` with session clearing
- `templates/login.html` — verify error/success display works

## Files to create
- `.claude/specs/03-login-logout.md` (this spec)

## New dependencies
No new pip packages. Use existing:
- `flask` (already installed)
- `werkzeug.security.check_password_hash` (already installed)
- `sqlite3` (standard library)

## Rules for implementation
- No SQLAlchemy or ORMs — use `sqlite3` via `database/db.py`
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values (e.g., `--ink`, `--paper-card`)
- All templates extend `base.html`
- Route functions: one responsibility (fetch data/process form, render/redirect)
- Never put DB logic in route functions — call `get_db()` and use parameterized SQL directly or through DB helpers
- Handle missing user (email not found) gracefully — show error, do not crash
- Handle wrong password gracefully — show error, do not reveal which field is wrong
- `abort()` for HTTP errors, not bare string returns

## Definition of done
- [ ] `GET /login` renders `login.html` with no errors
- [ ] `POST /login` validates inputs (email present, password present)
- [ ] `POST /login` checks `users` table for email; if not found shows error
- [ ] `POST /login` compares `password_hash` using `check_password_hash`; if mismatch shows error
- [ ] `POST /login` on success starts a session (e.g., `session['user_id']`) and redirects to `/profile`
- [ ] `GET /logout` clears session (`session.clear()` or `session.pop('user_id')`) and redirects to `/`
- [ ] `GET /logout` no longer returns a raw string; it performs a redirect
- [ ] `POST /login` uses parameterized queries only
- [ ] `POST /login` does not store or log plain-text passwords
- [ ] App runs on port 5001 without errors (`python app.py`)
