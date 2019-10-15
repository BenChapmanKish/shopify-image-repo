from flask import Flask, render_template, redirect
import sqlite3 as sql

app = Flask(__name__)

# Developer method, not for actual prod use
@app.route("/initialize")
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
    conn.commit()
    return render_template("message.html", message="Initialized database.")

@app.route("/products")
@app.route("/")
def home_page():
    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/" + row[2],
            "price": "$" + str(row[3]/100.0),
            "stock": str(row[4]) + " left",
        })
    
    for product in products:
        print(product)

    return render_template("index.html", products = products)

@app.route("/purchase_complete")
def purchase_complete():
    return render_template("purchase_complete.html")

@app.route("/buy/<product_id>")
def buy(product_id):
    if not product_id:
        return render_template("message.html", message="Invalid product ID!")

    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT stock FROM products WHERE rowid = " + str(product_id))
    stock = cur.fetchone()
    if not stock:
        return render_template("message.html", message="Invalid product ID!")

    if (stock[0] > 0):
        # If this was a real app, this is where we'd process the money transaction
        cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = " + str(product_id))
        conn.commit()
        return render_template("message.html", message="Purchase successful!")
    
    return render_template("message.html", message="Insufficient stock!")

if __name__ == '__main__':
   app.run(debug = True)