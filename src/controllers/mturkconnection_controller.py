from models import MTurkConnection


class MTurkConnectionController(object):
    def __init__(self, db):
        self.db = db
        self.db.mturkconnections.ensure_index('email', unique=True)
    def create(self, d):
        mtconn = MTurkConnection(access_key=d['access_key'],
                                 secret_key=d['secret_key'],
                                 email=d['email'],
                                 hitpayment=d['hitpayment'])
        print mtconn.hitpayment
        self.update(mtconn)
        return mtconn
    def update(self, mtconn):
        self.db.mturkconnections.update({'email' : mtconn.email}, 
                                        {'$set' : mtconn.serialize()},
                                        upsert=True )
        
    def get_by_email(self, email):
        d = self.db.mturkconnections.find_one({'email' : email})
        if not d:
            return None
        else:
            return MTurkConnection.deserialize(d)

    def begin_run(self, email=None, max_assignments=1):
        mt_conn = self.get_by_email(email)
        is_authed = mt_conn.try_auth() if mt_conn else False
        if is_authed and mt_conn.begin_run(max_assignments):
            self.update(mt_conn)


        
            
