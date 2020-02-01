from .question import Question

class CType(object) :
    def __init__(self, name=None, header=None, contentUpdate=None, questions=[]) :
        self.name = name
        self.header = header
        self.contentUpdate=contentUpdate
        self.questions = questions
    @classmethod
    def from_dict(cls, d) :
        return CType(d['name'], d['header'], d['contentUpdate'],[Question.deserialize(q) for q in d['questions']])
    def to_dict(self) :
        return {'name' : self.name,
                'header' : self.header,
                'contentUpdate': self.contentUpdate,
                'questions' : [q.serialize() for q in self.questions]}
    def filter_bonus_questions(self, response_info={}):
        bonus_questions = {q.varname : q.get_bonus() for q in self.questions if q.bonus}
        filtered_info = {}
        for varname in response_info :
            if varname not in bonus_questions :
                continue
            filtered_info[varname] = response_info[varname]
            filtered_info[varname]['__bonus__'] = bonus_questions[varname]
        return filtered_info
    def evaluate_conditions(self, response_info={}):
        worker_conditions = {}
        for workerid, responses in response_info.items():
            worker_conditions[workerid] = {q.varname : q.satisfies_condition(responses) for q in self.questions}
        return worker_conditions

    def sanitize_response(self, response) :
        questions = {q.varname : q for q in self.questions}

        sanitize_response = response
        module_responses = sanitize_response['responses']
        for r in module_responses :
            r = questions[r['varname']].sanitize_response(r) 
        return sanitize_response
                
    def validate(self, response) :
        """Validates a response for this module as given by JSON from the client."""
        questions = {q.varname : q for q in self.questions}
        valids = set()
        module_responses = response['responses']
        for r in module_responses :
            if r.get('varname', None) not in questions :
                return False
            if not questions[r['varname']].validate(r, module_responses) :
                return False
            valids.add(r['varname'])
        if valids != set(questions.keys()) :
            return False
        return True

