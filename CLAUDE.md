# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Spendly (Flask expense tracker)

Single-file Flask app (`app.py`) with Jinja2 templates (`templates/`), static CSS (`static/css/`), and a placeholder SQLite module (`database/db.py`). No README; see `PROJECT.md` for full structure and route table.

## Architecture
```
spendly/
├── app.py              # All routes — single file, no blueprints
├── database/
│   └── db.py           # SQLite helpers: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html       # Shared layout — all templates must extend this
│   └── *.html          # One template per page
├── static/
│   ├── css/
│   │   ├── style.css       # Global styles
│   │   └── landing.css     # Landing-page-only styles
│   └── js/
│       └── main.js         # Vanilla JS only
└── requirements.txt
```

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Page-specific styles → new `.css` file, not inline `<style>` tags

---

## Subagent Policy
- Always use a builtin explore subagent for codebase exploration 
  before implementing any new feature
- Always use a subagent to verify test results 
  after any implementation
- When asked to plan, delegate codebase research 
  to a subagent before presenting the plan
- always use a builtin plan subagent in plan mode

---

## Code style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders) — never f-strings in SQL
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

---

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and `match` statements are fine

---

## Architecture

- `app.py`: All routes defined explicitly. Auth (`/register`, `/login`), legal (`/terms`, `/privacy`), landing (`/`), and placeholder expense routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`).
- `templates/base.html`: Shared layout with navbar, footer links to `/terms` and `/privacy`, and `{% block scripts %}` for page-specific JS.
- `templates/landing.html`: Hero with mock stats card, category bars, and a vanilla-JS video modal (`#videoModal`) triggered by `openModal()`; closes via backdrop click, `×` button, or `Escape`. Closing resets the iframe `src` so the YouTube video stops.
- `templates/privacy.html` / `terms.html`: Card-styled legal pages with inline CSS matching theme variables (`--ink`, `--paper-card`, `--border`, etc.).
- `database/db.py`: Skeleton only. Students implement `get_db()`, `init_db()`, `seed_db()`.
- `static/css/style.css`: Global theme (variables, navbar, buttons, footer). `landing.css`: Hero, mock card, modal overlay styles.

## Design Theme (from `style.css` variables)

Colors: `#0f0f0f` (ink), `#1a472a` (deep green accent), `#f7f6f3` (paper background), `#e4e1da` (soft borders). Fonts: `DM Serif Display` (headings), `DM Sans` (body).

## Development Notes

- No `.cursor`, `.github/copilot-instructions.md`, `.gemini/`, `.codex/`, or `README.md` exists.
- `PROJECT.md` is the authoritative reference for routes, flow diagram, and feature history.
- Placeholder routes return plain strings; implement them as needed.
- Video modal uses no libraries — pure vanilla JS (`openModal`, `closeModal`, `closeModalOnBackdrop`, `keydown` listener).

## Commands
```bash
# Setup
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server (port 5001)
python app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

---

## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**

---

## Warnings and things to avoid

- **Never use raw string returns for stub routes** once a step is implemented — always render a template
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** mid-feature without flagging it — keep `requirements.txt` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **`database/db.py` is currently empty** — do not assume helpers exist until the step that implements them
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run `PRAGMA foreign_keys = ON` on every connection
- The app runs on **port 5001**, not the Flask default 5000 — don't change this