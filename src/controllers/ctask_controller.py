
class CTaskController(object):
    def __init__(self, db):
        self.db = db
        self.db.ctasks.ensure_index('taskid', unique=True)
    def create(self, d):
        from models import CTask
        ctask = CTask.deserialize(d)
        self.db.ctasks.insert(ctask.serialize())
        return ctask







"""
class CTaskController(object) :
    def __init__(self, db) :
        self.db = db
        self.db.ctasks.ensure_index([('type_name', 1), ('name', 1)],
                                    unique=True)
    def get_names(self, type_name) :
        res = self.db.ctasks.find({'type_name' : type_name}, {'name' : True})
        return [r['name'] for r in res]
    def get_by_name(self, type_name, name) :
        d = self.db.ctasks.find_one({'type_name' : type_name,
                                     'name' : name})
        return CTask.from_dict(d)
    def set_live(self, task, is_live) :
        task.live = is_live
        self.db.ctasks.update({'type_name' : task.type_name,
                               'name' : task.name},
                              {'$set' : {'live' : task.live}})
        return task
    def create(self, ctype, name, content, live=False) :
        c = CTask(type_name=ctype.name,
                  created=datetime.datetime.now(),
                  responses=[],
                  name=name,
                  content=content,
                  live=live)
        self.db.ctasks.insert(c.to_dict())
        return c
    def add_response(self, task, worker_name, response) :
        r = CResponse(submitted=datetime.datetime.now(),
                     response=response,
                     worker_name=worker_name)
        self.db.ctasks.update({'type_name' : task.type_name,
                               'name' : task.name},
                              {'$push' : {'responses' : r.to_dict()}})
        return r
"""
