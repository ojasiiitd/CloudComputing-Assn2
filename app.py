from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "dev-secret-key"

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
        name = request.form["name"].strip()
        price_raw = request.form["price"].strip()
        description = request.form["description"].strip()

        if not name or not price_raw:
            flash("Name and price are required.", "danger")
            return render_template("add_product.html", form_data=request.form)

        try:
            price = float(price_raw)
        except ValueError:
            flash("Price must be a valid number.", "danger")
            return render_template("add_product.html", form_data=request.form)

        if price < 0:
            flash("Price cannot be negative.", "danger")
            return render_template("add_product.html", form_data=request.form)

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
            (name, price, description),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_product.html", form_data={})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
