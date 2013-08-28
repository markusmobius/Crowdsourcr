from models import MTurkConnection


class MTurkConnectionController(object):
    def __init__(self, db):
        self.db = db
        self.db.mturkconnections.ensure_index('email', unique=True)
    def create(self, d):
        mtconn = MTurkConnection(**d)
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

    def begin_run(self, email=None, max_assignments=1, url=""):
        mt_conn = self.get_by_email(email)
        is_authed = mt_conn.try_auth() if mt_conn else False
        if is_authed and mt_conn.begin_run(max_assignments=max_assignments,
                                           url=url):
            self.update(mt_conn)

    def end_run(self, email=None) :
        mt_conn = self.get_by_email(email)
        mt_conn.end_run()
        self.update(mt_conn)
        
    def make_payments(self, email=None):
        from controllers import CHITController
        mt_conn = self.get_by_email(email)
        submitted_assignments = mt_conn.get_payments_to_make()
        mt_conn.make_payments(assignment_ids=[a[0] for a in submitted_assignments if CHITController.secret_code_matches(db=self.db,worker_id=a[1], secret_code=a[2])])
            
