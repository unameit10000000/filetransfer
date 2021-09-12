"""
=======================================================
UPLOAD VIEW
=======================================================
"""
from flask import (
    Blueprint, redirect, render_template, request, session, url_for,
    jsonify
)


bp = Blueprint('upload', __name__, url_prefix='/')


from werkzeug.wrappers.request import Request
from werkzeug.exceptions import HTTPException, NotFound

import os, re, uuid, hashlib
from datastore import db, FilebaseDataModel
from filebase import settings as fbSettings
from filebase import owner as fbOwner
from filebase.bucket import IBucket


@bp.route('/upload/<id>', methods=['GET','POST'])
def upload(id):
    host = os.getenv("APPLICATION_HOST")
    port = str(os.getenv("APPLICATION_PORT"))

    # ************************************
    # FILEBASE IMPLEMENTATION start
    # ************************************
    
    owner, uid = None, None
    if request.method == 'GET' or request.method == 'POST':
        user = fbOwner.IOwner()
        res = user.set_owner(fbSettings.s3Client)
        if res is 0:
            owner, uid = user.name(), user.uid()
        else:
            print("Err: "+str(res))
            return render_template("upload.html", host=host, port=port, session_id=session.get('session_id'))

    # ************************************
    # FILEBASE IMPLEMENTATION end
    # ************************************

    if request.method == 'GET':
        if id == session.get('session_id'):
            return render_template("upload.html", host=host, port=port, session_id=session.get('session_id'), username=owner)

    if request.method == 'POST':
        if id == session.get('session_id'):

            files = request.files
            assert files, "No files found!"
            filekey = request.form.get('filekey') or str(uuid.uuid1())
            assert re.compile(r'^[a-zA-Z0-9-]+$').match('filekey'), 'Unacceptable file key'
            
            # Temporarly save file to transferred/upload/
            fileobj = None
            filename = None
            filepath = ""
            for k in files.keys():
                filename = k
                fileobj = files.get(k)
                filepath = "./transferred/upload/"+filename
                fileobj.save(filepath)

            if fileobj:
                
                # ************************************
                # FILEBASE IMPLEMENTATION start
                # ************************************
                # NOTE: A new bucket will be created using the provided name unless it already exists.
                # If no buckets exist on Filebase and no name is provided,-
                # a unique bucketname will be generated for the bucket instead
                
                defBucket = False
                fileBucket = None
                bucketname = fbSettings.default_bucket_name
                if not bucketname or bucketname is None:

                    # No bucketname env variables retrieved
                    # Retry getting env defined in Dockerfile
                    bucketname = os.getenv("FB_DEFAULT_BUCKET")

                    # If all didn't work use a unique id for bucketname
                    if not bucketname or bucketname is None:

                        # Again, no bucketname env variables retrieved
                        # Continue to check if there are any existing buckets on Filebase to use
                        # If err = -1, no buckets could be found. Create and init a new bucket
                        fileBucket = IBucket(None, fbSettings.s3Client, fbSettings.s3Resource)
                        if fileBucket.init() == -1:
                            bucketname = uuid.uuid1().hex
                            fileBucket = IBucket(bucketname, fbSettings.s3Client, fbSettings.s3Resource)
                            fileBucket.init()
                        else:
                            bucketname = fileBucket.name
                    else:
                        # Retrieved bucketname from env variables
                        defBucket = True
                else:
                    # Retrieved bucketname from env variables
                    defBucket = True
                    
                # The provided bucketname has been found, create a new bucket using this env: 'FB_DEFAULT_BUCKET'
                if defBucket:
                    fileBucket = IBucket(bucketname, fbSettings.s3Client, fbSettings.s3Resource)
                    fileBucket.init()

                if fileBucket.exist and bucketname is not None:
                    fileBucket.upload_file_obj(filepath, filename)
                else:
                    try:
                        return view(request)
                    except HTTPException as e:
                        return e
                

                # Remove file from transferred/upload/ folder
                os.remove(filepath)

                crypt = hashlib.sha256()
                crypt.update(str.encode(filekey))

                sharedReference = crypt.hexdigest()

                # NOTE: In this demo the constructed 'reallink' below isn't used in the actual download section -
                # of the of the sourcecode (views/downloads.py) since it requires buckets to be set to public -
                # either manually on Filebase or somehow via the boto3 AWS SDK. Instead the IBucket 'download()' function -
                # is used to retrieve public and private files

                # --------------------------------/
                # reallink = "https://"+bucketname+".s3.filebase.com/"+filename
                # --------------------------------/

                # ************************************
                # FILEBASE IMPLEMENTATION end
                # ************************************

                # Save data in db 
                results = None
                try:
                    results = db.session.query(FilebaseDataModel).all()
                    if not results:
                        raise
                    else:
                        model = FilebaseDataModel(filename, sharedReference, "reallink")
                        db.session.add(model)
                        db.session.commit()
                        return jsonify(ref=sharedReference, file=filename, username=owner)
                except:
                    model = FilebaseDataModel(bucketname, filename, sharedReference, "reallink")
                    db.create_all()
                    db.session.add(model)
                    db.session.commit()
                    FilebaseDataModel.query.all()
                    return jsonify(ref=sharedReference, file=filename, username=owner)
            else:
                return jsonify(ref=None)

    return redirect(url_for("login.login"))

def view(request):
    raise NotFound()
