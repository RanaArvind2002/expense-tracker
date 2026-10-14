import pytest
from app import app
from database.db import get_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_insert_expense_valid():
    conn = get_db()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    from database.db import insert_expense
    insert_expense(1, 50.0, "Food", "2026-03-20", "Lunch")
    row = conn.execute("SELECT * FROM expenses WHERE user_id = ?", (1,)).fetchone()
    assert row is not None
    assert row["amount"] == 50.0
    assert row["category"] == "Food"
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()


def test_insert_expense_no_description():
    conn = get_db()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    from database.db import insert_expense
    insert_expense(1, 30.0, "Transport", "2026-03-21", None)
    row = conn.execute("SELECT * FROM expenses WHERE user_id = ?", (1,)).fetchone()
    assert row is not None
    assert row["description"] is None
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()


def test_get_expense_unauthenticated(client):
    resp = client.get("/expenses/add")
    assert resp.status_code == 302
    assert "/login" in resp.headers.get("Location", "")


def test_get_expense_authenticated(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.get("/expenses/add")
    assert resp.status_code == 200
    assert b"<form" in resp.data
    assert b"method=\"POST\"" in resp.data or b"method='POST'" in resp.data
    assert b'<select' in resp.data


def test_post_expense_unauthenticated(client):
    resp = client.post("/expenses/add", data={})
    assert resp.status_code == 302
    assert "/login" in resp.headers.get("Location", "")


def test_post_expense_valid(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (1,))
    conn.commit()
    conn.close()
    resp = client.post(
        "/expenses/add",
        data={"amount": "50.0", "category": "Food", "date": "2026-03-20", "description": "Lunch"},
    )
    assert resp.status_code == 302
    assert "/profile" in resp.headers.get("Location", "")
    conn = get_db()
    row = conn.execute("SELECT * FROM expenses WHERE user_id = ?", (1,)).fetchone()
    assert row is not None
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (1,))
    conn.commit()
    conn.close()


def test_post_expense_missing_amount(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.post("/expenses/add", data={"category": "Food", "date": "2026-03-20"})
    assert resp.status_code == 200
    assert b"Amount" in resp.data or b"required" in resp.data or b"amount" in resp.data.lower()


def test_post_expense_amount_zero(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.post("/expenses/add", data={"amount": "0", "category": "Food", "date": "2026-03-20"})
    assert resp.status_code == 200


def test_post_expense_non_numeric_amount(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.post("/expenses/add", data={"amount": "abc", "category": "Food", "date": "2026-03-20"})
    assert resp.status_code == 200


def test_post_expense_invalid_category(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.post("/expenses/add", data={"amount": "10", "category": "Invalid", "date": "2026-03-20"})
    assert resp.status_code == 200


def test_post_expense_invalid_date(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    resp = client.post("/expenses/add", data={"amount": "10", "category": "Food", "date": "bad-date"})
    assert resp.status_code == 200


def test_post_expense_no_description(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (1,))
    conn.commit()
    conn.close()
    resp = client.post(
        "/expenses/add",
        data={"amount": "20", "category": "Transport", "date": "2026-03-21", "description": ""},
    )
    assert resp.status_code == 302
    conn = get_db()
    row = conn.execute("SELECT * FROM expenses WHERE user_id = ?", (1,)).fetchone()
    assert row is not None
    assert row["description"] is None
    conn.execute("DELETE FROM expenses WHERE user_id = ?", (1,))
    conn.commit()
    conn.close()
