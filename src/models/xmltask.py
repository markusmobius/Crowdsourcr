try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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
                                                'questiontext' : question.find('questiontext').text,
                                                'helptext' : get_help_text(question),
                                                'valuetype' : question.find('valuetype').text,
                                                'options' : self.get_options(question),
                                                'content' : XMLQuestion.parse(question.find('valuetype').text,
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
        for hit in self.hits.iter('hit'):
            yield {'hitid' : hit.find('hitid').text,
                   'tasks' : hit.find('tasks').text.split()}
    def get_documents(self) :
        docs = {}
        if self.documents :
            for doc in self.documents.iter('document') :
                docs[doc.find('name').text.strip()] = doc.find('content').text
        return docs

class XMLQuestionRegistry(type):
    def __init__(cls, name, bases, dct) :
        if hasattr(cls, "typeName") :
            XMLQuestion.question_types[cls.typeName] = cls
        super(XMLQuestionRegistry, cls).__init__(name, bases, dct)

class XMLQuestion(object):
    __metaclass__ = XMLQuestionRegistry
    question_types = {}
    @classmethod
    def parse(cls, question_type, question_content):
        return cls.question_types[question_type].parse(question_content)

class XMLCategoricalQuestion(XMLQuestion):
    typeName = 'categorical'
    @staticmethod
    def parse(question_content):
        all_categories = []
        for category in question_content.find('categories').iter('category'):
            all_categories.append({'text' : category.find('text').text,
                                   'value' : category.find('value').text})
        return all_categories

class XMLNumericQuestion(XMLQuestion):
    typeName = 'numeric'
    @staticmethod
    def parse(question_content=None):
        return []

class XMLTextQuestion(XMLQuestion):
    typeName = 'text'
    @staticmethod
    def parse(question_content=None):
        return []
