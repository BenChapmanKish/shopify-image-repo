from flask import Flask, render_template, redirect
import sqlite3 as sql

app = Flask(__name__)

@app.route("/reset")
def reset():
    initialize()
    return render_template("message.html", message="Database reset.")

def initialize():
    conn = sql.connect("database.db")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT, price INTEGER, stock INTEGER)")
    cur.execute("""INSERT INTO products (name, imgpath, price, stock) VALUES \
        ('Guitar', 'images/guitar.jpg', 12000, 8), \
        ('Couch', 'images/couch.jpg', 24000, 2), \
        ('Plant', 'images/plant.jpg', 1800, 34), \
        ('Phone', 'images/phone.png', 85000, 0)
    """)

    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("CREATE TABLE transactions (timestamp TEXT, productid INTEGER, value INTEGER)")
    
    conn.commit()
    print("Initialized database")

@app.route("/products")
@app.route("/")
def home_page():
    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()

    print("Retrieved " + str(len(rows)) + " database entries")
    
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/" + row[2],
            "price": "$" + str(row[3]/100.0),
            "stock": str(row[4]) + " left",
        })
    
    cur.execute("SELECT SUM(value) FROM transactions")
    result = cur.fetchone()[0]
    earnings = 0

    if result:
        earnings = result/100.0

    return render_template("index.html", products = products, earnings = earnings)

@app.route("/purchase_complete")
def purchase_complete():
    return render_template("purchase_complete.html")

@app.route("/buy/<product_id>")
def buy(product_id):
    if not product_id:
        return render_template("message.html", message="Invalid product ID!")

    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT rowid, price, stock FROM products WHERE rowid = " + str(product_id))
    result = cur.fetchone()
    if not result:
        return render_template("message.html", message="Invalid product ID!")

    (rowid, price, stock) = result

    if (stock > 0):
        print("Processed transaction of value $" + str(price/100.0))
        cur.execute("INSERT INTO transactions (timestamp, productid, value) VALUES " + \
            "(datetime(), "+str(rowid)+", "+str(price)+")")

        cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = " + str(product_id))
        conn.commit()
        return render_template("message.html", message="Purchase successful!")
    
    return render_template("message.html", message="Insufficient stock!")

if __name__ == '__main__':
    initialize()
    app.run(debug = True)