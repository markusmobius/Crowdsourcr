try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .question import Question
from helpers import CustomEncoder, Lexer, Status
import jsonpickle

class XMLTask(object) :
    def __init__(self, xml_path=None) :
        self.reader = ET.parse(xml_path)
        self.root = self.reader.getroot()
        assert self.root.tag == 'xml'
        self.modules = self.root.find('modules')
        self.tasks = self.root.find('tasks')
        self.hits = self.root.find('hits')
        self.documents = self.root.find('documents')
        self.docs = self.get_documents()
        self.sets = self.root.find('sets')
    def get_modules(self):
        def get_help_text(ent) :
            ment = ent.find('helptext')
            return ment.text if ment != None else None
        encounteredModuleNames={}        
        for module in self.modules.iter('module'):
            if module.find('name').text in encounteredModuleNames:
                raise Exception("Module "+module.find('name').text+" is defined more than once.")
            encounteredModuleNames.add(module.find('name').text)
            module_out = {'header' : module.find('header').text,
                          'name' : module.find('name').text,
                          'contentUpdate' : module.find('contentUpdate').text if module.find('contentUpdate') != None else None,
                          'questions' : []}
            encounteredVarNames={}                    
            for question in module.find('questions').iter('question'):
                if question.find('varname').text in encounteredVarNames:
                    raise Exception("Variable "+question.find('varname').text+"in module "+module.find('name').text+" is defined more than once.")
                encounteredVarNames.add(question.find('varname').text)
                lexedCondition=None
                if question.find('condition') != None:
                    conditionStr=question.find('condition').text
                    lex = Lexer()
                    status = Status()
                    if not lex.can_import(conditionStr, status):
                        raise Exception(status.error)
                    lexedCondition=jsonpickle.encode(lex)
                module_out['questions'].append({'varname' : question.find('varname').text,
                                                'condition' : lexedCondition,
                                                'questiontext' : question.find('questiontext').text,
                                                'helptext' : get_help_text(question),
                                                'bonus' : question.find('bonus').text if question.find('bonus') != None else None,
                                                'bonuspoints' : float(question.find('bonuspoints').text) if question.find('bonuspoints') != None else 1.0,
                                                'valuetype' : question.find('valuetype').text,
                                                'options' : self.get_options(question),
                                                'content' : Question.parse_content_from_xml(question.find('valuetype').text,
                                                                                            question.find('content'))})
            yield module_out
    def get_options(self, qelt) :
        opts = {}
        optelt = qelt.find('options')
        if not optelt : return {}
        for child in optelt :
            if child.tag.endswith("s") :
                opts.setdefault(child.tag, []).append(child.text)
            else :
                opts[child.tag] = child.text
        return opts
    def get_tasks(self):
        for task in self.tasks.iter('task'):
            # first see if there is a corresponding document
            content = task.find('content').text.strip()
            content = self.docs.get(content, content)
            yield {'content' : content,
                   'taskid' : task.find('taskid').text,
                   'modules' : task.find('modules').text.split()}
    def get_hits(self):
        def get_exclusions(hittag):
            exctag = hittag.find('exclusions')
            return exctag.text.split() if exctag != None else []
        for hit in self.hits.iter('hit'):
            tasks=hit.find('tasks').text.split()
            taskConditionList=[None] * len(tasks)
            taskconditions=hit.find('taskconditions')
            if taskconditions!=None:
                for taskcondition in taskconditions.iter('taskcondition'):
                    if taskcondition.find('taskid')==None:
                        raise Exception('taskid is not defined in taskcondition')
                    conditionStr=taskcondition.find('condition').text
                    for subtaskid in taskcondition.find('taskid').text.split(' '):
                        for i,taskid in enumerate(tasks):
                            if taskid==subtaskid:
                                if taskConditionList[i]==None:
                                    taskConditionList[i]=[]
                                taskConditionList[i].append("("+conditionStr+")")
                for i,tc in enumerate(taskConditionList):
                    if tc!=None:
                        lex = Lexer()
                        status = Status()
                        if not(lex.can_import("&".join(tc), status)):
                            #print("&".join(tc))
                            raise Exception(status.error)
                        taskConditionList[i]= jsonpickle.encode(lex)
                        #print(taskConditionList[i])
            yield {'hitid' : hit.find('hitid').text,
                   'exclusions' : get_exclusions(hit),
                   'tasks' : tasks,
                   'taskconditions': taskConditionList}
    def get_sets(self):
        if self.sets!=None:
            for set in self.sets.iter('set'):
                # first see if there is a corresponding document
                name = set.find('name').text.strip()
                members = set.find('members').text.split()
                for member in members:
                    yield {'name' : name,
                        'member' : str(member.strip())}
    def get_documents(self) :
        docs = {}
        if self.documents :
            for doc in self.documents.iter('document') :
                docs[doc.find('name').text.strip()] = doc.find('content').text
        return docs
