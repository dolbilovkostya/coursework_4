import calendar
import datetime
import jwt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

from constants import JWT_SECRET, JWT_ALGO

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    favorite_genre_id = db.Column(db.Integer)

# with app.app_context():
with db.session.begin():
    user = db.session.query(User).get(2)
    print(user.password)

    data = {
                "email": user.email,
                "password": user.password
            }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    print(data)

    # data = {'email': 'second@email.com', 'password': 'KsArkvcyJvaI1rCSXh9uK4Q5FEgYUVp/U3BvcPaGqZE=', 'exp': 1677157048}
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
    print(access_token)