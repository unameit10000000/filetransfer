"""
=======================================================
FILEBASE BUCKET INTERFACE CLASS
=======================================================

This class uses the Python AWS SDK Boto3 to communicate
with the Filebase API
"""
import boto3
import time


class IBucket:
    exist = False

    def __init__(self, bucket_name, s3_client, s3_resource):
        self.name = bucket_name
        self.s3_client = s3_client
        self.s3_resource = s3_resource

    # Initialize using an existing bucket or creating a new one
    def init(self):
        try:
            # Check provided bucket str len
            bstrlen = self.get_name_len()
            if self.name is not None and bstrlen >= 3 and bstrlen <= 63:
                self.s3_resource.create_bucket(Bucket=self.name)
            else:
                # Link the first bucket if any exists
                self.check_first_bucket()
            
            # Check first bucket str len
            bstrlen = self.get_name_len()
            if self.name is not None and bstrlen >= 3 and bstrlen <= 63: 
                self.bucket = self.s3_resource.Bucket(self.name)
            else:
                raise

            # Give the Filebase server time before validating..
            time.sleep(2)
            self.validate()
        except:
            # The bucket might already exist
            return -1
        return 0

    # Check if the provided or newly created bucket exists on Filebase
    def validate(self):
        response = self.s3_client.list_buckets()
        buckets = response['Buckets']
        for b in buckets:
            if self.name == b['Name']:
                self.info = b
                self.exist = True
                break
            self.exist = False

    # Find the first available bucket
    def check_first_bucket(self):
        response = self.s3_client.list_buckets()
        buckets = response['Buckets']
        if len(buckets) > 0:
            self.name = buckets[0]['Name']
        else:
            self.name = None

    def name(self):
        return self.name

    def get_name_len(self):
        if self.name and self.name is not None:
            return len(str(self.name))
        else:
            return 0

    def set_name(self, bucketname):
        self.name = bucketname

    def upload_file_obj(self, src, filename):
        if self.exist:
            with open(src, "rb") as data:
                self.bucket.upload_fileobj(data, filename)
            return 0
        return -1

    def download(self, filename, dst):
        if self.exist:
            try:
                self.s3_resource.Bucket(self.name).download_file(filename, dst)
            except:
                return -1
        return 0
