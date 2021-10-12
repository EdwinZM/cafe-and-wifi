from flask import Flask, request
from flask.templating import render_template
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


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

class CafeForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    map_url = StringField(label="Google Maps URL", validators=[DataRequired()])
    img_url = StringField(label="Image URL", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_sockets = BooleanField(label="Has Sockets", validators=[DataRequired()])
    has_toilet = BooleanField(label="Has Toilet", validators=[DataRequired()])
    has_wifi = BooleanField(label="Has WiFi", validators=[DataRequired()])
    can_take_calls = BooleanField(label="Can Take Calls", validators=[DataRequired()])
    seats = StringField(label="Seats")
    coffee_price = StringField(label="Coffee Price")
    submit = SubmitField(label="Create")

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


@login_required
@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_cafe = Cafe(
                name = form.name.data,
                map_url = form.map_url.data,
                img_url = form.img_url.data,
                location = form.location.data,
                has_sockets = form.has_sockets.data,
                has_toilet = form.has_toilet.data,
                has_wifi = form.has_wifi.data,
                can_take_calls = form.can_take_calls.data,
                seats = form.seats.data,
                coffee_price = form.coffee_price.data
            )

            db.session.add(new_cafe)
            db.session.commit()

            return redirect("/")
    return render_template("/add_cafe.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)