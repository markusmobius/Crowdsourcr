from models import MTurkConnection


class MTurkConnectionController(object):
    def __init__(self, db):
        self.db = db
        self.db.mturkconnections.ensure_index('email', unique=True)
    def create(self, d):
        mtconn = MTurkConnection(access_key=d['access_key'],
                                 secret_key=d['secret_key'],
                                 email=d['email'])
        self.db.mturkconnections.update({'email' : mtconn.email}, 
                                        {'$set' : { 'access_key' : mtconn.access_key,
                                                    'secret_key' : mtconn.secret_key }},
                                        upsert=True )
        return mtconn
    def get_by_email(self, email):
        d = self.db.mturkconnections.find_one({'email' : email})
        if not d:
            return None
        else:
            return MTurkConnection(access_key=d['access_key'],
                                   secret_key=d['secret_key'],
                                   email=d['email'])


        
            
