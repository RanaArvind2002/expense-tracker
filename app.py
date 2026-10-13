import re
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-secret-key-2026"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    error = None
    success = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        errors = []
        if not name:
            errors.append("Full name is required.")
        elif len(name) < 2:
            errors.append("Full name must be at least 2 characters.")
        if not email:
            errors.append("Email is required.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Please enter a valid email address.")
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if not confirm_password:
            errors.append("Confirm password is required.")
        elif password != confirm_password:
            errors.append("Passwords do not match.")
        if errors:
            error = " ".join(errors)
        else:
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                conn.commit()
                success = "Account created successfully. You can now sign in."
            except sqlite3.IntegrityError:
                error = "An account with that email already exists."
            finally:
                conn.close()
    return render_template("register.html", error=error, success=success)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or not password:
            error = "Email and password are required."
        else:
            conn = get_db()
            try:
                row = conn.execute(
                    "SELECT id, email, password_hash FROM users WHERE email = ?", (email,)
                ).fetchone()
                if row is None:
                    error = "Invalid email or password."
                else:
                    if not check_password_hash(row["password_hash"], password):
                        error = "Invalid email or password."
                    else:
                        session["user_id"] = row["id"]
                        return redirect(url_for("profile"))
            finally:
                conn.close()
    return render_template("login.html", error=error)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user_id = session.get("user_id")
    conn = get_db()
    try:
        user_row = conn.execute("SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    finally:
        conn.close()
    user = {
        "name": user_row["name"] if user_row else "Unknown",
        "email": user_row["email"] if user_row else "",
        "initials": (user_row["name"][0] if user_row and user_row["name"] else "U").upper(),
        "member_since": user_row["created_at"] if user_row else "",
    }
    conn = get_db()
    try:
        total_row = conn.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        total_spent = total_row[0] if total_row[0] is not None else 0.0

        count_row = conn.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        transaction_count = count_row[0] if count_row[0] is not None else 0

        top_row = conn.execute(
            "SELECT category FROM expenses WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        top_category = top_row["category"] if top_row else None
    finally:
        conn.close()

    stats = {
        "total_spent": total_spent,
        "transaction_count": transaction_count,
        "top_category": top_category,
    }
    transactions = []
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT date, description, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 10",
            (session.get("user_id"),)
        ).fetchall()
        for row in rows:
            transactions.append({
                "date": row["date"],
                "description": row["description"],
                "category": row["category"],
                "amount": row["amount"],
            })
    finally:
        conn.close()
    categories = []
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? GROUP BY category",
            (user_id,),
        ).fetchall()
        for row in rows:
            categories.append({
                "name": row["category"],
                "total": float(row["total"]) if row["total"] is not None else 0.0,
            })
    finally:
        conn.close()
    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
