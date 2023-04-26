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


@app.route('/signup', methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        username = request.form['username']
        query = conn.execute(text("select * from users where username = :username").bindparams(username=username))
        result = query.fetchone()
        email = request.form['email']
        query2 = conn.execute(text("select * from users where email = :email").bindparams(email=email))
        result2 = query2.fetchone()
        if result:
            return render_template('signup.html', message='This username is already exist')
        if result2:
            return render_template('signup.html', message='There is already an account with this email')
        else:
            conn.execute(text("INSERT INTO users (name, email, username, password, user_type) VALUES (:name, :email,:username, :password, 'customer')"), request.form)
            conn.commit()
            return render_template('signup.html', message='Account Creation Successful')


if __name__ == '__main__':
    app.run(debug=True)

