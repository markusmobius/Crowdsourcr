import boto.mturk.connection

class MTurkConnection(object):
    def __init__(self, access_key=None, secret_key=None, email=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.email = email
        self.mturk_conn = boto.mturk.connection.MTurkConnection(self.access_key,
                                                                self.secret_key)
    def try_auth(self, access_key=None, secret_key=None):
        return True if self.get_balance else False

    def get_balance(self):
        try:
            return self.mturk_conn.get_account_balance()
        except:
            return None

