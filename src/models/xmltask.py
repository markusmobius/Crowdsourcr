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
    def get_modules(self):
        for module in self.modules.iter('module'):
            module_out = {'header' : module.find('header').text,
                          'name' : module.find('name').text,
                          'questions' : []}
            for question in module.find('questions').iter('question'):
                module_out['questions'].append({'varname' : question.find('varname').text,
                                                'questiontext' : question.find('questiontext').text,
                                                'valuetype' : question.find('valuetype').text,
                                                'content' : XMLQuestion.parse(question.find('valuetype').text,
                                                                                 question.find('content'))})
            yield module_out

    def get_tasks(self):
        for task in self.tasks.iter('task'):
                 yield {'content' : task.find('content').text,
                        'taskid' : task.find('taskid').text,
                        'modules' : task.find('modules').text.split()}
    def get_hits(self):
        for hit in self.hits.iter('hit'):
            yield {'hitid' : hit.find('hitid').text,
                   'tasks' : hit.find('tasks').text.split()}

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
