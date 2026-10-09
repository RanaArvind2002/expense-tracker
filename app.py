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
        return redirect(url_for("landing"))
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
                        return redirect(url_for("landing"))
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
    return "Profile page — coming in Step 4"


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
