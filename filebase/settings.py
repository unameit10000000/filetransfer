"""
=======================================================
FILEBASE SETTINGS FILE
=======================================================

This file holds the settings and objects used
to connect to the Filebase API
"""
import boto3
import os, time


key_id = os.getenv("FB_ACCESS_KEY")
key_secret = os.getenv("FB_ACCESS_KEY_SECRET")
endpoint = os.getenv("FB_API_ENDPOINT")
default_bucket_name = os.getenv("FB_DEFAULT_BUCKET")

s3Client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=key_secret,
        endpoint_url=endpoint
)

s3Resource = boto3.resource(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=key_secret,
        endpoint_url=endpoint
)