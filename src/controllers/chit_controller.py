
from models import CHIT

class CHITController(object):
    def __init__(self, db):
        self.db = db
        self.db.chits.ensure_index('hitid', unique=True)
    def create(self, d):
        chit = CHIT.deserialize(d)
        self.db.chits.insert(chit.serialize())
        return chit
    def get_chit_by_id(self, hitid):
        d = self.db.chits.find_one({'hitid' : hitid})
        chit = CHIT.deserialize(d)
        return chit
    def get_next_chit_id(self):
        d = self.db.chits.find_one()
        return d['hitid']
