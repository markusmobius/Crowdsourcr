import tornado.escape
from models import CResponse

class CResponseController(object):
    def __init__(self, db):
        self.db = db
        #self.db.cresponses.ensure_index([('taskid', 1), ('workerid', 1)],
        #                                unique=True)
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
    def write_response_to_csv(self, csvwriter, completed_workers=[]) :
        for d in self.db.cresponses.find() :
            if d['workerid'] in completed_workers :
                csvwriter.writerow([d['hitid'], d['taskid'], d['workerid'], str(d['submitted']),
                                    tornado.escape.json_encode(d['response'])])
    def all_responses_by_task(self, taskid=None, workerids=[]):
        d = self.db.cresponses.find({'taskid' : taskid,
                                     'workerid' : {'$in' : workerids}}, 
                                    {'workerid' : 1, 
                                     'response' : 1})
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

    def validate(self, taskid, response, task_controller, module_controller) :
        task = task_controller.get_task_by_id(taskid)

        received_modules = set(m['name'] for m in response)
        required_modules = set(task.modules)
        if received_modules != required_modules :
            return False

        for m in response :
            module = module_controller.get_by_name(m['name'])
            if not module.validate(m) :
                return False
        return True
