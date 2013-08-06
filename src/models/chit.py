
class CHIT(object):
    def __init__(self, hitid=None, tasks=[], completed_hits=[]):
        self.hitid = hitid
        self.tasks = tasks
        self.completed_hits = completed_hits
    @classmethod
    def deserialize(cls, d):
        return cls(hitid=d['hitid'], 
                   tasks=d['tasks'])
    def serialize(self):
        return {'hitid' : self.hitid,
                'tasks' : self.tasks,
                'completed_hits' : self.completed_hits,
                'num_completed_hits' : len(self.completed_hits)}
