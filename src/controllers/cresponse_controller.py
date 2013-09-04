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
    def append_completed_task_info(self, **d) :
        d['num_completed_tasks'] = self.db.cresponses.count()
        return d
    def get_reponse_info_by_worker(self, workerid):
        d = self.db.cresponses.find({'workerid' : workerid})
        return {'count' : len(d) }
    def get_hits_for_worker(self, workerid):
        d = self.db.cresponses.find({'workerid' : workerid}, {'hitid' : 1})
        return [r['hitid'] for r in d]
    def write_response_to_csv(self) :
        return ("%s\t%s\t%s\t%s\t%s" % (d['hitid'],
                                   d['taskid'],
                                   d['workerid'],
                                   str(d['submitted']),
                                   tornado.escape.json_encode(d['response']))
                for d in self.db.cresponses.find())
    def all_responses_by_task(self, taskid=None):
        d = self.db.cresponses.find({'taskid' : taskid}, {'workerid' : 1, 'response' : 1})
        module_responses = {} # module -> varname -> response -> [workerid]
        for row in d:
            for resp in row['response']:
                mod_name = resp['name']
                module_responses.setdefault(mod_name, {})
                for response in resp['responses']:
                    module_responses[mod_name].setdefault(response['varname'], {})
                    module_responses[mod_name][response['varname']].setdefault(response['response'], [])
                    module_responses[mod_name][response['varname']][response['response']].append(row['workerid'])
        return module_responses

            
        
