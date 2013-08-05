from question import Question

class CType(object) :
    def __init__(self, name=None, questions=[]) :
        self.name = name
        self.questions = questions
    @classmethod
    def from_dict(cls, d) :
        return CType(d['name'], [Question.deserialize(q) for q in d['questions']])
    def to_dict(self) :
        return {'name' : self.name,
                'questions' : [q.serialize() for q in self.questions]}
