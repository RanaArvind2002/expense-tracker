import random
from datetime import datetime, timedelta
from database.db import get_db

user_id = 2
count = 3
months = 5

categories = {
    "Food": (50, 800, 0.25),
    "Transport": (20, 500, 0.15),
    "Bills": (200, 3000, 0.15),
    "Health": (100, 2000, 0.08),
    "Entertainment": (100, 1500, 0.07),
    "Shopping": (200, 5000, 0.15),
    "Other": (50, 1000, 0.15),
}

descriptions = {
    "Food": ["Lunch at canteen", "Dinner with family", "Street food", "Breakfast", "Groceries"],
    "Transport": ["Auto ride", "Bus pass", "Train ticket", "Petrol", "Cab fare"],
    "Bills": ["Electricity bill", "Internet recharge", "Mobile recharge", "Water bill", "Rent"],
    "Health": ["Doctor visit", "Pharmacy", "Lab test", "Check-up"],
    "Entertainment": ["Movie ticket", "Concert", "Subscription", "Event entry"],
    "Shopping": ["Clothes", "Electronics", "Shoes", "Accessories"],
    "Other": ["Gift", "Donation", "Stationery", "Miscellaneous"],
}

def pick_category():
    r = random.random()
    cumulative = 0.0
    for cat, (_, _, prob) in categories.items():
        cumulative += prob
        if r <= cumulative:
            return cat
    return "Food"

now = datetime.now()
expenses_data = []
for _ in range(count):
    cat = pick_category()
    min_amt, max_amt, _ = categories[cat]
    amount = round(random.uniform(min_amt, max_amt), 2)
    desc = random.choice(descriptions[cat])
    delta_days = random.randint(1, months * 30)
    date_str = (now - timedelta(days=delta_days)).strftime("%Y-%m-%d")
    expenses_data.append((user_id, amount, cat, date_str, desc))

conn = get_db()
try:
    for data in expenses_data:
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            data
        )
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Insert failed, rolled back: {e}")
    raise
finally:
    inserted_count = conn.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()[0]
    sample = conn.execute(
        "SELECT id, amount, category, date, description FROM expenses WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,)
    ).fetchall()
    date_range = conn.execute(
        "SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()

print(f"Inserted: {len(expenses_data)} expenses")
print(f"Date range: {date_range[0]} to {date_range[1]}")
print("Sample (5 records):")
for row in sample:
    print(f"  id={row['id']} amount={row['amount']} category={row['category']} date={row['date']} description={row['description']}")
