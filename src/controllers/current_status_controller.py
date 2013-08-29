
class CurrentStatusController(object):
    def __init__(self, db):
        self.db = db
        self.db.currentstatus.ensure_index('workerid', unique=True)
    def create_or_update(self, workerid=None, hitid=None, taskindex=None) :
        self.db.currentstatus.update({'workerid' : workerid},
                                     {'workerid' : workerid,
                                      'hitid' : hitid,
                                      'taskindex' : taskindex},
                                     {'upsert' : 1})
    def remove(self, workerid=None):
        self.db.currentstatus.remove({'workerid' : workerid})
    def get_current_status(self, workerid):
        d = self.db.currentstatus.find_one({'workerid' : workerid})
        return d if d else None
