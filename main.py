from flask import *
from sqlalchemy import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
conn_str = "mysql://root:AmariLegend1!@localhost/final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def index():
    return render_template("index.html")


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
        query2 = conn.execute(text("SELECT * FROM users WHERE username = :username AND password = :password").bindparams(username=username,password=password))
        result2 = query2.fetchone()
        if result:
            if result2:
                session['username'] = username
                user_info = conn.execute(text("SELECT * FROM users WHERE username = :username").bindparams(username=username)).fetchone()
                return render_template('MyCustomer.html')
            else:
                render_template("CustomerLogin.html", message='Incorrect Password')


if __name__ == '__main__':
    app.run(debug=True)
