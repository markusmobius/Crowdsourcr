from models import CType

class CTypeController(object) :
    def __init__(self, db) :
        self.db = db
        self.db.ctypes.ensure_index('name', unique=True)
    def get_names(self) :
        res = self.db.ctypes.find({}, {'name' : True})
        return [r['name'] for r in res]
    def get_by_name(self, name) :
        d = self.db.ctypes.find_one({'name' : name})
        return CType.from_dict(d)
    def create(self, d) :
        c = CType.from_dict(d)
        self.db.ctypes.insert(c.to_dict())
        return c
