
class CHIT(object):
    def __init__(self, hitid=None, tasks=[]):
        self.hitid = hitid
        self.tasks = tasks
    @classmethod
    def deserialize(cls, d):
        return cls(d['hitid'], d['tasks'])
    def serialize(self):
        return {'hitid' : self.hitid,
                'tasks' : self.tasks}
