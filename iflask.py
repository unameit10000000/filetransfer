"""
=======================================================
FLASK INTERFACE CLASS
=======================================================
"""
from flask import (
    Flask, request, redirect, url_for
)

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import os

class IFlask:
    db = None
    app = None

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        CORS(self.app, supports_credentials=True)

        port = str(os.getenv("MYSQL_PORT"))
        if not port or port is None:
            port = 3306 # Defaults to this
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db-0:"+port+"/main"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.secret_key = 'super secret key'
        self.app.config['SESSION_TYPE'] = 'filesystem'