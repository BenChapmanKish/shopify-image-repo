# shopify-image-repo
### Shopify Winter 2020 Developer Intern Challenge Question
### Lovingly made by Ben Chapman-Kish :)

This is a demonstrative image repository with capacity for selling products.

This project has been implemented in Python using _Flask_ to serve a web interface
and _sqlite3_ to track product information and transactions. Please note that as
this is a backend interview role, I have invested no time whatsoever into making
a beautiful user interface, although I could have if time permitted. ;)

## Usage

To use this application, simply run `python3 server.py` from the command line.
This will create the appropriate database tables and start the Flask server.

After this, open a web browser at the address given by Flask (usually http://127.0.0.1:5000).
You will see a listing of products with associated data, such as their name, price, stock,
and, of course, the image for said product. All of this data is pulled directly from a DB
table and generated live with an HTML template. The images themselves are served from a static
images folder.

A user can also try to buy any product by clicking the BUY button next to its image. This will
verify that there are any left in stock, and will record the transaction (including time,
product, and value) in our transactions table, while decrementing the product's inventory
appropriately. Note that on the home page, we can see the total value of all transactions
we have processed to date.

## Possible Features

We could add a feature such as adding/removing products. This would be straightforward to
implement using a simple HTTP form that would POST an image and its data to our server,
allowing us to save the image to our images folder and update our products table. Another
complimentary form would let us remove products from the database and delete the image from
disk.

Another feature would be access control, allowing us to have different users of the image
repository. One such user could be a vendor and another could be a customer. We could verify
vendors by a login form that would give the browser an access token, allowing the application
to serve administrative tools to the user such as adding/removing products, viewing earnings,
and managing inventory. Customers could save payment information allowing them to easily buy
products without having to enter their payment data again each time.
