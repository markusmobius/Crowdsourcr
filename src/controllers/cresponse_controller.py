import tornado.escape
from models import CResponse

class CResponseController(object):
    def __init__(self, db):
        self.db = db
        self.db.cresponses.ensure_index([('taskid', 1), ('workerid', 1)],
                                    unique=True)
    def create(self, d):
        cresponse = CResponse.deserialize(d)
        self.db.cresponses.insert(cresponse.serialize())
        return cresponse
    def get_reponse_info_by_worker(self, workerid):
        d = self.db.cresponses.find({'workerid' : workerid})
        return {'count' : len(d) }
    def get_hits_for_worker(self, workerid):
        d = self.db.cresponses.find({'workerid' : workerid}, {'hitid' : 1})
        return [r['hitid'] for r in d]
    def write_response_to_csv(self) :
        return ("%s\t%s\t%s\t%s" % (d['hitid'],
                                   d['taskid'],
                                   d['workerid'],
                                   tornado.escape.json_encode(d['response']))
                for d in self.db.cresponses.find())

            
        
