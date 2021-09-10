"""
=======================================================
FILEBASE OWNER CLASS
=======================================================

This class represents the owner
of the Filebase account
"""
import botocore


class IOwner:
    username = None
    userid = None

    def __init__(self):
        self.key_owner = 'Owner'
        self.key_name = 'DisplayName'
        self.key_id = 'ID'

    # Link the owner based on the provided access keys 
    def set_owner(self, client):
        try:
            response = client.list_buckets()
            owner = response[self.key_owner]
            self.username = owner[self.key_name]
            self.userid = owner[self.key_id]
        except botocore.exceptions.ClientError as error:
            return error
        return 0

    # Get the current owners DisplayName
    def name(self):
        return self.username

    # Get the current owners ID
    def uid(self):
        return self.userid