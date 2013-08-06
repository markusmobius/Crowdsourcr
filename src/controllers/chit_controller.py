import uuid
from models import CHIT

class CHITController(object):
    def __init__(self, db):
        self.db = db
        self.db.chits.ensure_index('hitid', unique=True)
    def create(self, d):
        d['completed_hits'] = []
        chit = CHIT.deserialize(d)
        self.db.chits.insert(chit.serialize())
        return chit
    def get_chit_by_id(self, hitid):
        d = self.db.chits.find_one({'hitid' : hitid})
        chit = CHIT.deserialize(d)
        return chit
    def get_next_chit_id(self):
        d = self.db.chits.find_one({'$where' : 'this.completed_hits.length < 1'})
        return d['hitid'] if d else None
    def add_completed_hit(self,chit=None, worker_id=None):
        hit_info = ({'worker_id' : worker_id,
                     'turk_verify_code' : uuid.uuid4().hex[:16]})
        self.db.chits.update({'hitid' : chit.hitid},
                             {'$push' : {'completed_hits' : hit_info}})
        return hit_info
 
