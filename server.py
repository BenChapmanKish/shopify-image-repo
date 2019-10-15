from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)

def get_cursor():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    return (cur, conn)

"""Initialize the sqlite database and fill up the `products` table with sample data."""
def initialize_db():
    (cur, conn) = get_cursor()

    # Create products table with sample data
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT, price INTEGER, stock INTEGER)")
    cur.execute("""INSERT INTO products (name, imgpath, price, stock) VALUES \
        ('Guitar', 'images/guitar.jpg', 12000, 8), \
        ('Couch', 'images/couch.jpg', 27000, 2), \
        ('Potted Plant', 'images/plant.jpg', 1850, 34), \
        ('Phone', 'images/phone.png', 85000, 0), \
        ('Fiction Book', 'images/book.png', 479, 3129)
    """)

    # Create empty transactions table
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("CREATE TABLE transactions (timestamp TEXT, productid INTEGER, value INTEGER)")
    
    # Commit the db changes
    conn.commit()
    print("Initialized database")

@app.route("/")
def home_page():
    (cur, _) = get_cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    print("Retrieved %d database entries" % len(rows))
    
    # Pre-process product info for HTML templates
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/%s" % (row[2]),
            "price": "$%.2f" % (row[3]/100.0),
            "stock": "%d left" % (row[4]),
        })
    
    # Display total sales so far
    cur.execute("SELECT SUM(value) FROM transactions")
    result = cur.fetchone()[0]
    earnings = result/100.0 if result else 0

    return render_template("index.html", products=products, earnings=earnings)

@app.route("/buy/<product_id>")
def buy(product_id):
    if not product_id:
        return render_template("message.html", message="Invalid product ID!")

    (cur, conn) = get_cursor()

    cur.execute("SELECT rowid, price, stock FROM products WHERE rowid = ?", (product_id,))
    result = cur.fetchone()

    if not result:
        return render_template("message.html", message="Invalid product ID!")
    (rowid, price, stock) = result

    if stock <= 0:
        return render_template("message.html", message="Insufficient stock!")

    print("Processed transaction of value $%.2f" % (price/100.0))
    cur.execute("INSERT INTO transactions (timestamp, productid, value) VALUES " + \
        "(datetime(), ?, ?)", (rowid, price))

    cur.execute("UPDATE products SET stock = stock - 1 WHERE rowid = ?", (product_id,))
    conn.commit()
    return render_template("message.html", message="Purchase successful!")
    

@app.route("/reset")
def reset():
    initialize_db()
    return render_template("message.html", message="Database reset.")

if __name__ == '__main__':
    initialize_db()
    app.run(debug = True)