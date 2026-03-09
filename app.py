from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "products.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]

        if not name or not price:
            return "Invalid input"

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
            (name, price, description),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_product.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)