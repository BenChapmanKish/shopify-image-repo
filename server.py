from flask import Flask, render_template, redirect
import sqlite3 as sql

app = Flask(__name__)

@app.route("/initialize")
def initialize():
    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT, price INTEGER, stock INTEGER)")
    cur.execute("INSERT INTO products (name, imgpath, price, stock) VALUES ('Guitar', '/images/guitar.jpg', 12000, 6)")
    return redirect('/')

@app.route("/products")
@app.route("/")
def home_page():
    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    return render_template("index.html", products = rows)

@app.route("/purchase_complete")
def purchase_complete():
    return render_template("purchase_complete.html")

@app.route("/buy/<product_id>", methods=['POST'])
def buy(product_id):
    if not product_id:
        return "<p>Invalid product ID!</p>"

    conn = sql.connect("database.db")
    
    cur = conn.cursor()
    cur.execute("SELECT stock FROM products WHERE rowid = " + str(product_id))
    stock = cur.fetchone()[0]

    if (stock.isdigit() and int(stock) > 0):
        # If this was a real app, this is where we'd process the money transaction
        cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = " + str(product_id))
        return redirect('/purchase_complete')
    
    return "<p>Insufficient stock!</p>"

if __name__ == '__main__':
   app.run(debug = True)