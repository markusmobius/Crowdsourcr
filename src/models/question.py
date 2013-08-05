
class QTypeRegistry(type) :
    def __init__(cls, name, bases, dct) :
        if hasattr(cls, "typeName") :
            Question.qtype_subclasses[cls.typeName] = cls
        super(QTypeRegistry, cls).__init__(name, bases, dct)

class Question(object) :
    __metaclass__ = QTypeRegistry
    qtype_subclasses = {}
    def __init__(self, varname=None, text=None, valuetype=None):
        self.varname = varname
        self.text = text
        self.valuetype = valuetype
    @classmethod
    def deserialize(cls, d) :
        return cls.qtype_subclasses[d['valuetype']].deserialize(d)
    def serialize(self) :
        return {"type" : self.typeName,
                "text" : self.text,
                "content" : self.to_dict()}


class AbstractQuestion(Question):
    def __init__(self, varname=None, text=None, valuetype=None, options=[]) :
        Question.__init__(self, varname, text, valuetype)
        self.options = options
    @classmethod
    def deserialize(cls, dct={}):
        return cls(d['varname'],
                   d['text'], 
                   d['valuetype'],
                   d['content'])
    def serialize(self):
        return {'varname' : self.varname,
                'text' : self.text,
                'valuetype' : self.valuetype,
                'content' : self.content}


class CategoricalQuestion(AbstractQuestion):
    typeName = 'categorical'

class NumericalQuestion(AbstractQuestion):
    typeName = 'numerical'
    






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
