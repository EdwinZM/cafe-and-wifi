from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_url = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    has_sockets = db.Column(db.Boolean(), nullable=False)
    has_toilet = db.Column(db.Boolean(), nullable=False)
    has_wifi = db.Column(db.Boolean(), nullable=False)
    can_take_calls = db.Column(db.Boolean(), nullable=False)
    seats = db.Column(db.String(), nullable=False)
    coffee_price = db.Column(db.String(), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")

app.run(debug=True)