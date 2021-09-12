"""
=======================================================
ENTRYPOINT OF THE APPLICATION
=======================================================
"""
from iflask import *


###
# CREATE/CONFIG APP
###
iflask = IFlask()
app = iflask.app

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
