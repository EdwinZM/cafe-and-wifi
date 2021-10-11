from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from werkzeug.utils import redirect

app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'skdfaskdfhdfawei38209320hwkdwdf'


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    map_url = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    has_sockets = db.Column(db.Boolean(), nullable=False)
    has_toilet = db.Column(db.Boolean(), nullable=False)
    has_wifi = db.Column(db.Boolean(), nullable=False)
    can_take_calls = db.Column(db.Boolean(), nullable=False)
    seats = db.Column(db.String(), nullable=False)
    coffee_price = db.Column(db.String(), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    cafes = Cafe.query.all()
    
    if current_user.is_authenticated:
        authenticated = True
    else:
        authenticated = False
        print(current_user)
    return render_template("index.html", cafes=cafes, auth = authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":

        users = User.query.all()

        email = request.form["email"]
        password = request.form["password"]

        for user in users:
            if user.email == email:
                is_password = check_password_hash(user.password, password)
                
                if is_password:
                    login_user(user)
                    print("logged in")
                    return redirect("/")
                else:
                    error = "Incorrect password"
                    return render_template("login.html", error=error)
        
        error = "User not found!"

    print(request.method)
    return render_template("login.html", error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        users = User.query.all()
        
        email = request.form["email"]
        password = request.form["password"]

        for user in users:
            if user.email == email:
                error = "User already exists!"
                return render_template("signup.html", error=error)

        pw_hash = generate_password_hash(password).decode("utf-8")

        new_user = User(email=email, password=pw_hash)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect("/")
    return render_template("signup.html", error = error)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

app.run(debug=True)