import uuid
from models import CHIT
import bson.code
import datetime

class CHITController(object):
    def __init__(self, db):
        self.db = db
        self.db.chits.ensure_index('hitid', unique=True)
        self.sum_map = bson.code.Code("function() { emit(1, this.num_completed_hits); }")
        self.sum_reduce = bson.code.Code("function(key, vals) { return Array.sum(vals); }")
        
    def create(self, d):
        chit = CHIT.deserialize(d)
        self.db.chits.insert(chit.serialize())
        return chit
    def get_chit_by_id(self, hitid):
        d = self.db.chits.find_one({'hitid' : hitid})
        chit = CHIT.deserialize(d)
        return chit
    def get_next_chit_id(self, exclusions=[], workerid=None):
        cl = self.db.chitloads.find({'hitid' : {'$exists' : True}}, {'hitid' : 1})
        loaded_chits = [c['hitid'] for c in cl] if cl else []
        d = self.db.chits.find_one({'$and' : 
                                    [{ 'num_completed_hits' : {'$lt' : 1} },
                                     { 'exclusions' : {'$nin' : exclusions}},
                                     { 'hitid' : {'$nin' : loaded_chits} } ] },
                                   {'hitid' : 1})
        if d and workerid :
            self.db.chitloads.insert({'workerid' : workerid,
                                      'time' : datetime.datetime.utcnow(),
                                      'hitid' : d['hitid']})

        return d['hitid'] if d else None
    def get_chit_ids(self) :
        ds = self.db.chits.find({}, {'hitid' : True})
        return [d['hitid'] for d in ds]
    def get_agg_hit_info(self):
        result = self.db.chits.map_reduce(self.sum_map, self.sum_reduce, "chit_mapreducesum_results")
        num_completed_hits = result.find_one()
        num_total_hits = self.db.chits.count()
        return {'num_complete' : num_completed_hits['value'] if num_completed_hits else 0,
                'num_total' : num_total_hits}
    def add_completed_hit(self,chit=None, worker_id=None):
        hit_info = {'worker_id' : worker_id,
                    'turk_verify_code' : uuid.uuid4().hex[:16]}
        self.db.chits.update({'hitid' : chit.hitid},
                             {'$push' : {'completed_hits' : hit_info},
                              '$inc' : {'num_completed_hits' : 1}})
        return hit_info
    # static wasn't working ... ?
    # utility method called by MTurkConnecitonController.make_payments
    @classmethod
    def secret_code_matches(cls, db=None, worker_id=None, secret_code=None):
        hit_info = [{'worker_id' : worker_id,
                    'turk_verify_code' : secret_code}]
        #ugly hack. TODO: improve storage struture for easier searching
        d = db.chits.find_one({'$and' : 
                               [{'num_completed_hits' : {"$gte" : 1}},
                                {'completed_hits' : hit_info}]})
        return True if d else False
 
