import random
from datetime import datetime
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db

# Common Indian first/last names across regions
first_names = [
    "Rahul", "Priya", "Arjun", "Anjali", "Vikram", "Neha", "Karan",
    "Meera", "Rohan", "Sanya", "Amit", "Deepa", "Suresh", "Lakshmi",
    "Dev", "Pooja", "Raj", "Kavita", "Nikhil", "Isha"
]
last_names = [
    "Sharma", "Patel", "Singh", "Verma", "Reddy", "Nair", "Joshi",
    "Mehta", "Iyer", "Chopra", "Bhat", "Kulkarni", "Rao", "Gupta",
    "Kumar", "Das", "Roy", "Banerjee", "Mishra", "Yadav"
]

def generate_user():
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"
    return name, email

init_db()

while True:
    name, email = generate_user()
    conn = get_db()
    cursor = conn.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone() is None:
        break
    conn.close()

password_hash = generate_password_hash("password123")
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = get_db()
conn.execute(
    "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
    (name, email, password_hash, created_at),
)
conn.commit()
user_row = conn.execute("SELECT id, name, email FROM users WHERE email = ?", (email,)).fetchone()
conn.close()

print(f"id: {user_row['id']}")
print(f"name: {user_row['name']}")
print(f"email: {user_row['email']}")
