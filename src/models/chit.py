
class CHIT(object):
    def __init__(self, hitid=None, exclusions=[], tasks=[], completed_hits=[], num_completed_hits=None, **kwargs):
        self.hitid = hitid
        self.tasks = tasks
        self.completed_hits = completed_hits
        self.exclusions = exclusions
        self.num_completed_hits = num_completed_hits
    @classmethod
    def deserialize(cls, d):
        return cls(**d);
    def serialize(self):
        return {'hitid' : self.hitid,
                'tasks' : self.tasks,
                'exclusions' : self.exclusions,
                'completed_hits' : self.completed_hits,
                'num_completed_hits' : len(self.completed_hits)}
