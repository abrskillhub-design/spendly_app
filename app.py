import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
DB_FILE = "database.db"
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    if not os.path.exists(DB_FILE):
        conn = get_db_connection()
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
@app.route("/")
def index():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses ORDER BY created_at DESC").fetchall()
    total = sum(item["amount"] for item in expenses)
    conn.close()
    return render_template("index.html", expenses=expenses, total=total)
@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title")
    amount = request.form.get("amount")
    category = request.form.get("category")
    if title and amount and category:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
            (title, float(amount), category)
        )
        conn.commit()
        conn.close()
    return redirect(url_for("index"))
@app.route("/delete/<int:id>")
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
if __name__ == "__main__":
    init_db()
    app.run(debug=True)