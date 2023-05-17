from flask import *
from sqlalchemy import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
conn_str = "mysql://root:AmariLegend1!@localhost/final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        session.pop('username', None)
        return render_template("index.html")


@app.route('/Customer', methods=['GET', 'POST'])
def cus():
    if request.method == 'GET':
        return render_template("Customer.html")
    else:
        session.pop('username', None)
        return render_template("Customer.html")


@app.route('/Vendor', methods=['GET', 'POST'])
def ven():
    if request.method == 'GET':
        return render_template("Vendor.html")
    else:
        session.pop('username', None)
        return render_template("Vendor.html")


@app.route('/Admin', methods=['GET', 'POST'])
def Admin():
    if request.method == 'GET':
        return render_template("Admin.html")
    else:
        session.pop('username', None)
        return render_template("Admin.html")


@app.route('/CustomerSignUp', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'GET':
        return render_template("CustomerSignUp.html")
    else:
        username = request.form['username']
        query = conn.execute(text("select * from users where username = :username").bindparams(username=username))
        result = query.fetchone()
        email = request.form['email']
        query2 = conn.execute(text("select * from users where email = :email").bindparams(email=email))
        result2 = query2.fetchone()
        if result:
            return render_template('CustomerSignUp.html', message='This username is already exist')
        if result2:
            return render_template('CustomerSignUp.html', message='There is already an account with this email')
        else:
            conn.execute(text(
                "INSERT INTO users (name, email, username, password, user_type) VALUES (:name, :email,:username, :password, 'customer')"),
                request.form)
            conn.commit()
            return render_template('CustomerSignUp.html', message='Account Creation Successful')


@app.route('/VendorSignUp', methods=['GET', 'POST'])
def create_vendor():
    if request.method == 'GET':
        return render_template("VendorSignUp.html")
    else:
        username = request.form['username']
        query = conn.execute(text("select * from users where username = :username").bindparams(username=username))
        result = query.fetchone()
        email = request.form['email']
        query2 = conn.execute(text("select * from users where email = :email").bindparams(email=email))
        result2 = query2.fetchone()
        if result:
            return render_template('VendorSignUp.html', message='This username is already exist')
        if result2:
            return render_template('VendorSignUp.html', message='There is already an account with this email')
        else:
            conn.execute(text(
                "INSERT INTO users (name, email, username, password, user_type) VALUES (:name, :email,:username, :password, 'vendor')"),
                request.form)
            conn.commit()
            return render_template('VendorSignUp.html', message='Account Creation Successful')


@app.route('/CustomerLogin', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template("CustomerLogin.html")
    else:
        username = request.form['username']
        password = request.form['password']
        query = conn.execute(text("SELECT * FROM users WHERE username = :username").bindparams(username=username))
        result = query.fetchone()
        query2 = conn.execute(
            text("SELECT * FROM users WHERE username = :username AND user_type = 'vendor'").bindparams(
                username=username))
        result2 = query2.fetchone()
        if result:
            if result2:
                return render_template('CustomerLogin.html', message='Incorrect Account Type')
            else:
                if conn.execute(
                        text(
                            "SELECT password FROM users WHERE username = :username AND user_type = 'customer'").bindparams(
                            username=username)).fetchone()[0] == password:
                    session['username'] = username
                    user_id = conn.execute(text("SELECT user_id from users WHERE username = :username").bindparams(
                        username=username)).fetchone()[0]
                    session['id'] = user_id
                    user = conn.execute(
                        text("SELECT * FROM users WHERE user_id = :user_id").bindparams(user_id=user_id)).fetchone()
                    return render_template('MyCustomer.html', user=user)
                else:
                    return render_template('CustomerLogin.html', message='Invalid password')
        else:
            return render_template('CustomerLogin.html', message='Invalid username')


@app.route('/VendorLogin', methods=['GET', 'POST'])
def vendor_login():
    if request.method == 'GET':
        return render_template("VendorLogin.html")
    else:
        username = request.form['username']
        password = request.form['password']
        query = conn.execute(text("SELECT * FROM users WHERE username = :username").bindparams(username=username))
        result = query.fetchone()
        query2 = conn.execute(
            text("SELECT * FROM users WHERE username = :username AND user_type = 'customer'").bindparams(
                username=username))
        result2 = query2.fetchone()
        if result:
            if result2:
                return render_template('VendorLogin.html', message='Incorrect Account Type')
            else:
                if conn.execute(
                        text(
                            "SELECT password FROM users WHERE username = :username AND user_type = 'vendor'").bindparams(
                            username=username)).fetchone()[0] == password:
                    session['username'] = username
                    user_id = conn.execute(text("SELECT user_id from users WHERE username = :username").bindparams(
                        username=username)).fetchone()[0]
                    session['id'] = user_id
                    vendor = conn.execute(
                        text("SELECT * FROM users WHERE user_id = :user_id").bindparams(user_id=user_id)).fetchone()
                    return render_template('MyVendor.html', vendor=vendor)
                else:
                    return render_template('VendorLogin.html', message='Invalid password')
        else:
            return render_template('VendorLogin.html', message='Invalid username')


@app.route('/MyVendor', methods=['GET', 'POST'])
def my_vendor():
    if 'username' in session:
        username = session['username']
        user_id = conn.execute(
            text("SELECT user_id from users WHERE username = :username").bindparams(username=username)).fetchone()[0]
        vendor = conn.execute(
            text("SELECT * FROM users WHERE user_id = :user_id").bindparams(user_id=user_id)).fetchone()
        return render_template("MyVendor.html", vendor=vendor)
    else:
        return redirect('/VendorLogin')


@app.route('/MyUser', methods=['GET', 'POST'])
def my_user():
    if 'username' in session:
        username = session['username']
        user = \
            conn.execute(
                text("SELECT * from users WHERE username = :username").bindparams(username=username)).fetchone()[0]
        return render_template("MyCustomer.html", user=user)
    else:
        return render_template("CustomerLogin.html")


@app.route('/Shop', methods=['GET', 'POST'])
def shop():
    items = conn.execute(text("SELECT * FROM items NATURAL JOIN variants;"))
    conn.commit()
    return render_template('Store.html', items=items)


@app.route('/AddItem', methods=['GET', 'POST'])
def additem():
    if request.method == 'GET':
        return render_template("AddItem.html")
    else:
        item_title = request.form['item_title']
        query = conn.execute(
            text("select * from items where item_title = :item_title").bindparams(item_title=item_title))
        result = query.fetchone()
        if result:
            return render_template('AddItem.html', message='This already an item with this name')
        else:
            if 'username' in session:
                username = session['username']
                vendor_id = conn.execute(text("SELECT user_id from users WHERE username = :username").bindparams(
                    username=username)).fetchone()[0]
                conn.execute(text(
                    "INSERT INTO items (vendor_id ,item_title, item_description, item_category) VALUES (:vendor_id, :item_title, :item_description, :item_category)").bindparams(
                    vendor_id=vendor_id), request.form)
                conn.commit()
                return render_template('AddItem.html', message='Item Added Successfully')
            else:
                return render_template('VendorLogin.html', message='You must login to add an item')


@app.route('/AddVariant', methods=['GET', 'POST'])
def addvariant():
    if request.method == 'GET':
        return render_template("AddVariant.html")
    if 'username' in session:
        username = session['username']
        vendor_id = conn.execute(text("SELECT user_id from users WHERE username = :username").bindparams(
            username=username)).fetchone()[0]
        conn.execute(text(
            "INSERT INTO variants (item_id, vendor_id, image, size, color, price, inventory_count) VALUES (:item_id, :vendor_id, :image, :size, :color, :price, :inventory_count)").bindparams(
            vendor_id=vendor_id),
            request.form)
        conn.commit()
        return render_template('AddItem.html', message='Item Added Successfully')
    else:
        return render_template('VendorLogin.html', message='You must login to add an item')


@app.route('/EditItem', methods=['GET', 'POST', 'UPDATE'])
def edititem():
    if request.method == 'GET':
        return render_template("EditItem.html")
    else:
        item_title = request.form['item_title']
        query = conn.execute(
            text("select * from items where item_title = :item_title").bindparams(item_title=item_title))
        result = query.fetchone()
        if result:
            return render_template('EditItem.html', message='This already an item with this name')
        else:
            if 'username' in session:
                conn.execute(text(
                    "UPDATE items SET item_title = :item_title, item_description = :item_description,item_category = :item_category WHERE item_id = :item_id"),
                    request.form)
                conn.commit()
                return render_template('EditItem.html', message='Edit Added Successfully')
            else:
                return render_template('VendorLogin.html', message='You must login to edit an item')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    inventory_count = \
        conn.execute(text("SELECT inventory_count FROM variants WHERE variant_id = :variant_id"),
                     request.form).fetchone()[
            0]
    if inventory_count == 0:
        flash('Item out of stock')
        return redirect(url_for("shop"))
    id = session['id']
    result = conn.execute(
        text("SELECT * FROM carts WHERE user_id = :id AND variant_id = :variant_id").bindparams(id=id), request.form)
    if result.rowcount == 1:
        flash('Item already in cart')
        return redirect(url_for("shop"))
    else:
        conn.execute(text(
            "INSERT INTO carts (user_id, vendor_id, item_id, variant_id, quantity, price, color, size, image, item_title) VALUES (:id, :vendor_id, :item_id, :variant_id, :quantity, :price, :color, :size, :image, :item_title)").bindparams(
            id=id), request.form)
        conn.commit()
        flash('Item added to cart')
        return redirect(url_for("shop"))


@app.route('/Cart', methods=['GET'])
def cartitems():
    if 'username' in session:
        id = session['id']
        items = conn.execute(text("SELECT * FROM carts WHERE user_id = :id").bindparams(id=id))
        return render_template("Cart.html", items=items)
    else:
        return render_template('CustomerLogin.html')


@app.route('/order', methods=['POST'])
def order():
    id = session['id']
    conn.execute(text(
        "INSERT INTO orders (user_id, vendor_id, title, price, size, color, image, order_status) VALUES (:id, :vendor_id, :item_title, :price, :size, :color, :image, 'pending')").bindparams(
        id=id), request.form)
    conn.execute(text("DELETE FROM Carts Where user_id = :id AND variant_id = :variant_id").bindparams(id=id),
                 request.form)
    conn.commit()
    return redirect(url_for("cartitems"))


@app.route('/Orders', methods=['GET'])
def showorders():
    id = session['id']
    items = conn.execute(text("SELECT * FROM orders WHERE user_id = :id").bindparams(id=id))
    return render_template('Orders.html', items=items)


@app.route('/VendorOrders', methods=['GET'])
def vendorders():
    id = session['id']
    items = conn.execute(text("SELECT * FROM orders WHERE vendor_id = :id").bindparams(id=id))
    return render_template('VendorOrders.html', items=items)


@app.route('/approve', methods=['POST'])
def approve():
    conn.execute(text("UPDATE orders set order_status = 'confirmed' WHERE order_id = :order_id"), request.form)
    conn.commit()
    return redirect(url_for("vendorders"))


@app.route('/Products', methods=['GET'])
def products():
    id = session['id']
    products = conn.execute(text("SELECT * FROM variants WHERE vendor_id = :id").bindparams(id=id))
    return render_template("Products.html", products=products)


@app.route('/AdminSignUp', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'GET':
        return render_template("AdminSignUp.html")
    else:
        username = request.form['username']
        query = conn.execute(text("select * from users where username = :username").bindparams(username=username))
        result = query.fetchone()
        email = request.form['email']
        query2 = conn.execute(text("select * from users where email = :email").bindparams(email=email))
        result2 = query2.fetchone()
        if result:
            return render_template('AdminSignUp.html', message='This username is already exist')
        if result2:
            return render_template('AdminSignUp.html', message='There is already an account with this email')
        else:
            conn.execute(text(
                "INSERT INTO users (name, email, username, password, user_type) VALUES (:name, :email,:username, :password, 'Admin')"),
                request.form)
            conn.commit()
            return render_template('AdminSignUp.html', message='Account Creation Successful')


@app.route('/AdminLogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("AdminLogin.html")
    else:
        username = request.form['username']
        password = request.form['password']
        query = conn.execute(text("SELECT * FROM users WHERE username = :username").bindparams(username=username))
        result = query.fetchone()
        query2 = conn.execute(
            text("SELECT * FROM users WHERE username = :username AND user_type = 'vendor'").bindparams(
                username=username))
        result2 = query2.fetchone()
        if result:
            if result2:
                return render_template('AdminLogin.html', message='Incorrect Account Type')
            else:
                if conn.execute(
                        text(
                            "SELECT password FROM users WHERE username = :username AND user_type = 'admin'").bindparams(
                            username=username)).fetchone()[0] == password:
                    session['username'] = username
                    user_id = conn.execute(text("SELECT user_id from users WHERE username = :username").bindparams(
                        username=username)).fetchone()[0]
                    session['id'] = user_id
                    user = conn.execute(
                        text("SELECT * FROM users WHERE user_id = :user_id").bindparams(user_id=user_id)).fetchone()
                    return render_template('MyAdmin.html', user=user)
                else:
                    return render_template('AdminLogin.html', message='Invalid password')
        else:
            return render_template('AdminLogin.html', message='Invalid username')


@app.route('/DeleteItem', methods=['GET','POST'])
def display():
    if request.method == 'GET':
        return render_template("DeleteItem.html")
    else:
        conn.execute(text("DELETE FROM Items where item_id = :item_id"), request.form)
        conn.commit()
        return render_template("DeleteItem.html")


@app.route('/AddItemAdmin', methods=['GET', 'POST'])
def adminadditem():
    if request.method == 'GET':
        return render_template("AdminAddItem.html")
    else:
        item_title = request.form['item_title']
        query = conn.execute(
            text("select * from items where item_title = :item_title").bindparams(item_title=item_title))
        result = query.fetchone()
        if result:
            return render_template('AddItemAdmin.html', message='This already an item with this name')
        else:
            if 'username' in session:
                username = session['username']
                conn.execute(text(
                    "INSERT INTO items (vendor_id ,item_title, item_description, item_category) VALUES (:vendor_id, :item_title, :item_description, :item_category)"),
                    request.form)
                conn.commit()
                return render_template('AdminAddItem.html', message='Item Added Successfully')
            else:
                return render_template('AdminLogin.html', message='You must login to add an item')


@app.route('/OrdersAdmin', methods=['GET'])
def adminorders():
    items = conn.execute(text("SELECT * FROM orders"))
    return render_template("AdminOrders.html", items=items)


@app.route('/approve2', methods=['POST'])
def approve2():
    conn.execute(text("UPDATE orders set order_status = 'confirmed' WHERE order_id = :order_id"), request.form)
    conn.commit()
    return redirect(url_for("adminorders"))


@app.route('/MyAdmin', methods=['GET'])
def my_admin():
    if 'username' in session:
        username = session['username']
        user_id = conn.execute(
            text("SELECT user_id from users WHERE username = :username").bindparams(username=username)).fetchone()[0]
        user = conn.execute(
            text("SELECT * FROM users WHERE user_id = :user_id").bindparams(user_id=user_id)).fetchone()
        return render_template("MyAdmin.html", user=user)
    else:
        return redirect('/AdminLogin')


@app.route('/return1', methods=['POST'])
def return1():
    conn.execute(text(
        "INSERT INTO returns (order_id, user_id, vendor_id, title, color, size, price, image) VALUES ( :order_id, :user_id, :vendor_id, :title, :color, :size, :price, :image) "),
        request.form)
    conn.commit()
    return redirect(url_for("showorders"))


@app.route('/VendorReturns', methods=['GET'])
def return2():
    if 'username' in session:
        username = session['username']
        user_id = conn.execute(
            text("SELECT user_id from users WHERE username = :username").bindparams(username=username)).fetchone()[0]
        returns = conn.execute(text("SELECT * FROM returns WHERE vendor_id = :user_id").bindparams(user_id=user_id))
        return render_template("VendorReturns.html", returns=returns)


@app.route('/deny', methods=['POST'])
def deny():
    conn.execute(text("DELETE FROM returns where return_id = :return_id "), request.form)
    conn.commit()
    return redirect(url_for("adminorders"))


@app.route('/ReturnsAdmin', methods=['GET'])
def return3():
    returns = conn.execute(text("SELECT * FROM returns"))
    return render_template("AdminReturns.html", returns=returns)


@app.route('/review', methods=['POST'])
def review():
    conn.execute(text(
        "INSERT INTO REVIEWS (order_id, user_id, vendor_id, title, color, size, price, image, review_message, rating) VALUES ( :order_id, :user_id, :vendor_id, :title, :color, :size, :price, :image, :review_message, :rating) "),
        request.form)
    conn.commit()
    return redirect(url_for("showorders"))


@app.route('/Reviews', methods=['GET'])
def reviews():
    reviews = conn.execute(text("SELECT * FROM reviews"))
    return render_template("Reviews.html", reviews=reviews)


@app.route('/AdminProducts', methods=['GET'])
def getprods():
    products = conn.execute(text("SELECT * FROM variants"))
    return render_template('AdminProducts.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
