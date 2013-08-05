
class CHITController(object):
    def __init__(self, db):
        self.db = db
        self.db.chits.ensure_index('hitid', unique=True)
    def create(self, d):
        from models import CHIT
        chit = CHIT.deserialize(d)
        self.db.chits.insert(chit.serialize())
        return chit
