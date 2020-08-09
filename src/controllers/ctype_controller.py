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
    def get_by_names(self, names) :
        return {name : self.get_by_name(name) for name in names}
    def create(self, d) :
        c = CType.from_dict(d)
        self.db.ctypes.insert(c.to_dict())
        return c
    def evaluate_module_conditions(self, module_responses={}):
        # module -> workerid -> {varname: response_value}
        return {module : self.get_by_name(module).evaluate_conditions(module_responses[module]) for module in module_responses}
    def getModuleVarnameValuetype(self):
        #create crosswalk from module->varname->valuetype
        crosswalk={}
        d=self.db.ctypes.find({},{'name':1,'questions':1})
        for row in d:
            crosswalk[row['name']]={}
            for question in row['questions']:
                crosswalk[row['name']][question['varname']]={"valuetype":question['valuetype'],"aprioripermissable":[]}
                if question['valuetype']=="categorical":
                    for c in question['content']:
                        if 'aprioripermissable' in c:
                            if c['aprioripermissable']==True:
                                crosswalk[row['name']][question['varname']]["aprioripermissable"].append(c['value'])
        return crosswalk
