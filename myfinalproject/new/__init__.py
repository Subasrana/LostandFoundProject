#Import packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

#direction to define the path for database to be created
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Items Class/Model
class Items(db.Model):
    __tablename__ = "FoundItems"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(100))
    description = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    date = db.Column(db.Integer)

    def __init__(self, name, location,description, picture, date):
        self.name = name
        self.location = location
        self.description = description
        self.picture = picture
        self.date = date

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location','description', 'picture', 'date')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# User Class/Model
class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(50), unique = True)



    def __init__(self, firstname, lastname ,email , password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname','email', 'password')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Registering blueprints

from new.lostandfound.routes import lostandfound
app.register_blueprint(lostandfound)

from new.users.user_routes import users
app.register_blueprint(users)

from new.CSV_upload.route import csv
app.register_blueprint(csv)
