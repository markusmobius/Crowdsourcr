
class QTypeRegistry(type) :
    def __init__(cls, name, bases, dct) :
        if hasattr(cls, "typeName") :
            Question.qtype_subclasses[cls.typeName] = cls
        super(QTypeRegistry, cls).__init__(name, bases, dct)

class Question(object) :
    __metaclass__ = QTypeRegistry
    qtype_subclasses = {}
    def __init__(self, varname=None, questiontext=None, helptext=None, options=None, valuetype=None, bonus=None):
        def validate_bonus(bonus) :
            if bonus == None or bonus == 'linear':
                return bonus
            else :
                try :
                    split_bonus = bonus.split(':')
                    bthreth = int(split_bonus[1])
                    if bthresh > 100 or bthresh < 0 or split_bonus[0] != 'threshold':
                        raise Exception
                    else :
                        return bonus
                except:
                    raise Exception('Question bonus string %s improperly formatted.' % bonus)
        self.varname = varname
        self.questiontext = questiontext
        self.helptext = helptext
        self.options = options
        self.bonus = validate_bonus(bonus)
        self.valuetype = valuetype
    @classmethod
    def deserialize(cls, d) :
        return cls.qtype_subclasses[d['valuetype']].deserialize(d)
    def serialize(self) :
        return {'valuetype' : self.valuetype,
                'varname' : self.varname,
                'questiontext' : self.questiontext,
                'helptext' : self.helptext,
                'options' : self.options,
                'content' : self.content,
                'bonus' : self.bonus}
    def get_bonus(self):
        if not bonus:
            return None
        elif bonus == 'linear':
            return { 'type' : 'linear' }
        else:
            split_bonus = bonus.split(':')
            return { 'type' : 'threshold',
                     'threshold' : int(split_bonus[1]) }

    # Parses XML to get question 'content' (returns list).
    # Currently only used for categorical questions.
    @classmethod
    def parse_content_from_xml(cls, question_type, question_content):
        return cls.qtype_subclasses[question_type].parse_content_from_xml(question_content)

# Allows question-specific deserialization (not currently used).
# Otherwise unnecessary.
class AbstractQuestion(Question):
    def __init__(self, content=[], **kwargs) :
        Question.__init__(self, **kwargs)
        self.content = content
    @classmethod
    def deserialize(cls, d):
        return cls(**d)

class CategoricalQuestion(AbstractQuestion):
    typeName = 'categorical'
    @staticmethod
    def parse_content_from_xml(question_content):
        return [{'text' : category.find('text').text,
                 'value' : category.find('value').text}
                for category in question_content.find('categories').iter('category')]

class NumericQuestion(AbstractQuestion):
    typeName = 'numeric'
    @staticmethod
    def parse_content_from_xml(question_content=None):
        return []
    
class TextQuestion(AbstractQuestion) :
    typeName = 'text'
    @staticmethod
    def parse_content_from_xml(question_content=None):
        return []





"""
class AbstractMultiQType(Question) :
    def __init__(self, varname=None, text=None, valuetype=None, options=[]) :
        Question.__init__(self, varname, text, valuetype)
        self.options = options
    @classmethod
    def from_dict(cls, text, d) :
        return cls(text, d['options'])
    def to_dict(self) :
        return {'options' : self.options}

class RadioQType(AbstractMultiQType) :
    typeName = "radio"
class CheckboxQType(AbstractMultiQType) :
    typeName = "checkbox"
class SelectQType(AbstractMultiQType) :
    typeName = "select"

class ScaleQType(Question) :
    typeName = "scale"
    def __init__(self, text, scalecont, scalemin, scalemax, scalestep):
        Question.__init__(self, text)
        self.scalecont = scalecont
        self.scalemin = scalemin
        self.scalemax = scalemax
        self.scalestep = scalestep
    @classmethod
    def from_dict(cls, text, d) :
        return cls(text,
                   scalecont=d['scalecont'],
                   scalemin=d['scalemin'],
                   scalemax=d['scalemax'],
                   scalestep=d['scalestep'])
    def to_dict(self) :
        return { 'scalecont' : self.scalecont,
                 'scalemin' : self.scalemin,
                 'scalemax' : self.scalemax,
                 'scalestep' : self.scalestep }

class TextQType(Question) :
    typeName = "text"
    def __init__(self, text, textlength):
        Question.__init__(self, text)
        self.textlength = textlength
    @classmethod
    def from_dict(cls, text, d) :
        return cls(text,
                   textlength=d['textlength'])
    def to_dict(self) :
        return { 'textlength' : self.textlength }

class GridQType(Question) :
    typeName = "grid"
    def __init__(self, text, rowoptions, coloptions):
        Question.__init__(self, text)
        self.rowoptions = rowoptions
        self.coloptions = coloptions
    @classmethod
    def from_dict(cls, text, d) :
        return cls(text,
                   rowoptions=d['rowoptions'],
                   coloptions=d['coloptions'])
    def to_dict(self) :
        return { 'rowoptions' : self.rowoptions,
                 'coloptions' : self.coloptions }

"""
