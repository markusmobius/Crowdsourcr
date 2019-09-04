try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from question import Question

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
    def get_modules(self):
        def get_help_text(ent) :
            ment = ent.find('helptext')
            return ment.text if ment != None else None
        for module in self.modules.iter('module'):
            module_out = {'header' : module.find('header').text,
                          'name' : module.find('name').text,
                          'questions' : []}
            for question in module.find('questions').iter('question'):
                module_out['questions'].append({'varname' : question.find('varname').text,
                                                'condition' : question.find('condition').text if question.find('condition') != None else None,
                                                'questiontext' : question.find('questiontext').text,
                                                'helptext' : get_help_text(question),
                                                'bonus' : question.find('bonus').text if question.find('bonus') != None else None,
                                                'bonuspoints' : float(question.find('bonuspoints').text) if question.find('bonuspoints') != None else 0.0,
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
                for condition in taskconditions.iter('taskcondition'):
                    for i,taskid in enumerate(tasks):
                        if taskid==condition.find('taskid').text:
                            taskConditionList[i]=condition.find('condition').text
            yield {'hitid' : hit.find('hitid').text,
                   'exclusions' : get_exclusions(hit),
                   'tasks' : tasks,
                   'taskconditions': taskConditionList}
    def get_documents(self) :
        docs = {}
        if self.documents :
            for doc in self.documents.iter('document') :
                docs[doc.find('name').text.strip()] = doc.find('content').text
        return docs
