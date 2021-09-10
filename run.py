"""
=======================================================
ENTRYPOINT OF THE APPLICATION
=======================================================
"""
from flask import (
    Flask, request, redirect, url_for
)

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import os


###
# CREATE/CONFIG APP
###
app = Flask(__name__)

CORS(app)
CORS(app, supports_credentials=True)

port = str(os.getenv("MYSQL_PORT"))
if not port or port is None:
    port = 3306 # Defaults to this
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db-0:"+port+"/main"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

###
# DEFINE DB MODELS
###
db = SQLAlchemy(app)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128), unique=True)

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

###
# SET BLUEPRINTS
###
from views import login
from views import upload
from views import download
# from views import fbowner # NOTE: Currently not used

app.register_blueprint(login.bp)
app.register_blueprint(upload.bp)
app.register_blueprint(download.bp)
# app.register_blueprint(fbowner.bp) # NOTE: Currently not used

###
# MOUNT
###
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login.login'))
