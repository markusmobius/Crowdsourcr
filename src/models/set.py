
class SET(object):
    def __init__(self, name=None, members=[]):
        self.name = name
        self.members = members
    @classmethod
    def deserialize(cls, d):
        return cls(**d);
    def serialize(self):
        return {'name' : self.name,
                'members' : self.members}
