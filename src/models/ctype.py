from question import Question

class CType(object) :
    def __init__(self, name=None, header=None, questions=[]) :
        self.name = name
        self.header = header
        self.questions = questions
    @classmethod
    def from_dict(cls, d) :
        return CType(d['name'], d['header'], [Question.deserialize(q) for q in d['questions']])
    def to_dict(self) :
        return {'name' : self.name,
                'header' : self.header,
                'questions' : [q.serialize() for q in self.questions]}
