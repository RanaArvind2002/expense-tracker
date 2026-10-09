# Spendly — Expense Tracker Project Overview

## What is this?
A Flask (Python) web app called **Spendly** — a personal expense tracking application. It has a landing page, auth pages (login/register), legal pages (terms/privacy), and placeholder routes for future features.

---

## Project Structure

```
expense-tracker/
├── app.py                  # Flask routes
├── database/
│   ├── __init__.py
│   └── db.py              # Placeholder: get_db(), init_db(), seed_db()
├── static/
│   ├── css/
│   │   ├── style.css      # Global theme (variables, navbar, buttons, forms, footer)
│   │   └── landing.css    # Hero-specific + mock card + modal styles
│   └── js/
│       └── main.js        # (currently empty/minimal)
├── templates/
│   ├── base.html          # Base layout (navbar, footer, scripts block)
│   ├── landing.html       # Home / hero page
│   ├── login.html         # Sign in page
│   ├── register.html      # Create account page
│   ├── terms.html         # Terms & Conditions
│   └── privacy.html       # Privacy Policy
└── requirements.txt
```

---

## App Flow (Routes)

| Route | Method | Template | Purpose |
|---|---|---|---|
| `/` | GET | `landing.html` | Landing / marketing page |
| `/register` | GET | `register.html` | Account creation form |
| `/login` | GET | `login.html` | Sign in form |
| `/terms` | GET | `terms.html` | Terms of service |
| `/privacy` | GET | `privacy.html` | Privacy policy |
| `/logout` | GET | string | Placeholder (Step 3) |
| `/profile` | GET | string | Placeholder (Step 4) |
| `/expenses/add` | GET | string | Placeholder (Step 7) |
| `/expenses/<id>/edit` | GET | string | Placeholder (Step 8) |
| `/expenses/<id>/delete` | GET | string | Placeholder (Step 9) |

---

## Design Theme

- **Colors**: `#0f0f0f` (ink black), `#1a472a` (deep green accent), `#f7f6f3` (warm paper background), `#e4e1da` (soft borders)
- **Fonts**: `DM Serif Display` (display/headings), `DM Sans` (body)
- **Layout**: Sticky navbar, centered hero, 3-column features, centered CTA, dark footer
- **Components**: Card-style auth forms, pill badges, filled + outline buttons, mock expense card with bar charts

---

## Key Features Added Recently

### 1. Terms & Privacy Pages (`terms.html`, `privacy.html`)
- Match the site's card/theme styling
- Sections: Acceptance / Use / Data / Liability / Changes / Contact (terms); Data Collected / How Used / Storage / Third Parties / Your Rights / Cookies / Changes / Contact (privacy)

### 2. Footer Links (`base.html`)
- Terms → `/terms`
- Privacy → `/privacy` (was `#`)

### 3. Hero Redesign (`landing.html` + `landing.css`)
- Badge: `● Free to use · No credit card needed`
- Title: "Track every rupee." (black serif)
- Subtitle: "Know where it goes." (green serif)
- Description: "Spendly helps you log expenses..."
- Buttons: "Create free account" and "See how it works" (both dark, same size)
- Mock card: Window dots + 3 stat boxes (`This month`, `Budget left`, `Transactions`) + colored category bars (`Food`, `Travel`, `Bills`)

### 4. Video Modal (`landing.html` + `landing.css`)
- Trigger: "See how it works" button (`onclick="openModal()"`)
- Modal overlay (`#videoModal`) with backdrop blur
- Contains `iframe` YouTube embed (`youtubeVideo`)
- Close: `×` button, click outside overlay, `Escape` key
- When closing: `iframe.src` reset to empty then restored → video stops
- Vanilla JS only (no libraries)

---

## Database (Placeholder)
`database/db.py` is a skeleton. Students are meant to implement:
- `get_db()` — SQLite connection with `row_factory` and `foreign_keys`
- `init_db()` — `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — sample data insertion

---

## App Startup
```bash
python app.py       # runs on port 5001, debug=True
```

---

## Flow Diagram

```
User visits /
  → base.html layout + landing.html hero + landing.css styles
  → Click "See how it works"
    → openModal() shows #videoModal overlay
    → Click × / outside / Escape
    → closeModal() hides overlay + stops YouTube video
  → Click "Create free account"
    → /register (form)
  → Click footer links
    → /terms or /privacy (legal pages with card styling)
```
