"""
=======================================================
DOWNLOAD VIEW
=======================================================
"""
from flask import (
    Blueprint, redirect, render_template, request, session, url_for,
    jsonify, send_file
)


bp = Blueprint('download', __name__, url_prefix='/')


import os, io, requests
from os.path import exists
from run import db, FilebaseDataModel
from filebase import settings as fbSettings
from filebase import owner as fbOwner
from filebase.bucket import IBucket


@bp.route('/download/<ref>', methods=['GET', 'POST'])
def download(ref):
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
            return render_template('download.html')

    # ************************************
    # FILEBASE IMPLEMENTATION end
    # ************************************

    if request.method == 'GET':
        filename = None
        results = None
        try:
            results = db.session.query(FilebaseDataModel).all()
            if results:
                for fbdata in results:
                    if ref == fbdata.sharedlink:
                        filename = fbdata.filename
        except:
            print("Err: Could not query the database")

        return render_template('download.html', filename=filename, sharedlink=ref)

    if request.method == 'POST':
        bucketname = None
        filename = None
        # reallink = None # NOTE: Not used in this demo
        results = None
        try:
            results = db.session.query(FilebaseDataModel).all()
            if results:
                for fbdata in results:
                    if ref == fbdata.sharedlink:
                        bucketname = fbdata.fb_bucket
                        filename = fbdata.filename
                        # reallink = fbdata.reallink # NOTE: Not used in this demo
        except:
            print("Err: Could not query the database")

        # ************************************
        # FILEBASE IMPLEMENTATION start
        # ************************************
        # NOTE: If the provided bucket name doesn't exist a new bucket will be created!
        
        if bucketname is None:
            bucketname = fbSettings.default_bucket_name
        
        fileBucket = IBucket(bucketname, fbSettings.s3Client, fbSettings.s3Resource)
        
        # NOTE: The bucket might already exist
        if fileBucket.init() != 0:
            # Validating to link "your" existing bucket
            fileBucket.validate()

        currpath = "."
        dwnlpath = "/transferred/download/"
        dst = currpath+"/transferred/download/"+filename

        if fileBucket.exist:
            if fileBucket.download(filename, dst) != 0:
                return render_template('download.html')

        file_contents = None
        if exists(dst):
            try:
                FILE = open(dst)
                if not FILE.closed:
                    with open(dst, 'rb') as fbytes:
                        file_contents = fbytes.read()
                FILE.close()

                # Remove file from transferred/download/ folder
                os.unlink(dst)
                os.remove(dst)
            except:
                # TODO: Err handling here..
                pass

        if file_contents:
            return send_file(
                io.BytesIO(file_contents),
                as_attachment=True,
                attachment_filename=filename)

        # NOTE: In this demo the constructed 'reallink' isn't used since it requires-
        # buckets to be set to public, either manually on Filebase or somehow using the boto3 AWS SDK

        # --------------------------------/
        # if reallink:
        #     print(reallink)
        #     r = requests.get(reallink, allow_redirects=False)
        #     return send_file(
        #         io.BytesIO(r.content),
        #         as_attachment=True,
        #         attachment_filename=filename)
        # --------------------------------/

        # ************************************
        # FILEBASE IMPLEMENTATION end
        # ************************************

    return render_template('download.html')
    