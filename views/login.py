"""
=======================================================
LOGIN VIEW
=======================================================
"""
from flask import (
    Blueprint, redirect, render_template, request, session, url_for,
    jsonify
)


bp = Blueprint('login', __name__, url_prefix='/admin', template_folder="templates")


import os
from run import db, UserModel


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        try:
            results = db.session.query(UserModel).all()
            if not results:
                raise
            else:
                return render_template("login.html", message="Login")
        except:
            return render_template("login.html", message="Initial Login")

    error = None
    if request.method == 'POST':

        uname = request.form['username']
        passw = request.form['password']

        # Save data in db
        results = None
        try:
            results = db.session.query(UserModel).all()
            if not results:
                raise
        except:
            model = UserModel(uname, passw)
            db.create_all()
            db.session.add(model)
            db.session.commit()
            UserModel.query.all()
            return login_session()

        if results:
            validated = False
            for result in results:
                if result.username == uname:
                    if result.password == passw:
                        validated = True
            if validated:
                return login_session()
            else:
                return render_template("login.html", message="Login", error="Wrong username and/or password!")
        return jsonify(success=False)
    else:
        return jsonify(success=False)

def login_session():
    import uuid
    session_id = uuid.uuid4().hex
    session.clear()
    session["session_id"] = session_id
    return redirect(url_for('upload.upload', id=session_id))
