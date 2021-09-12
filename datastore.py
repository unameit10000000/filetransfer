"""
=======================================================
DATASTORE CLASS

Contains the database models used throughout the app
=======================================================
"""
from flask_sqlalchemy import SQLAlchemy
from run import app

db = SQLAlchemy(app)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128), unique=True)
    access_key = db.Column(db.String(128), unique=True)
    access_key_secret = db.Column(db.String(128), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class FilebaseDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fb_bucket = db.Column(db.String(63))    # Bucketnames on Filebase must be 3 to 63 chars long
    filename = db.Column(db.String(192))
    sharedlink = db.Column(db.String(64), unique=True)
    reallink = db.Column(db.String(256))

    def __init__(self, fb_bucket, filename, sharedlink, reallink):
        self.fb_bucket = fb_bucket
        self.filename = filename
        self.sharedlink = sharedlink
        self.reallink = reallink

    def __repr__(self):
        return '<User %r>' % self.sharedlink