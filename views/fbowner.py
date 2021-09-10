"""
=======================================================
FILEBASE OWNER VIEW

Test view, currently not used
=======================================================

Access Filebase data
"""
# from flask import (
#     Blueprint, redirect, render_template, request, session, url_for,
#     jsonify
# )


# bp = Blueprint('filebase', __name__, url_prefix='/filebase')


# from filebase import settings as fbSettings
# from filebase import owner as fbOwner
# from run import db


# @bp.route('/info/<id>', methods=['GET'])
# def info(id):
#     if request.method == 'GET':
#         if id == session.get("session_id"):
#             user = fbOwner.IOwner()
#             user.set_owner(fbSettings.s3Client)
#             name, uid = user.name(), user.uid()
#             return jsonify(name=name, id=uid)
            
#     return redirect(url_for("login.login"))