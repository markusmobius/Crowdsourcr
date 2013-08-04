from model import Model

class QTypeRegistry(type) :
    def __init__(cls, name, bases, dct) :
        if hasattr(cls, "typeName") :
            QType.qtype_subclasses[cls.typeName] = cls
        super(QTypeRegistry, cls).__init__(name, bases, dct)

class QType(object) :
    __metaclass__ = QTypeRegistry
    qtype_subclasses = {}
    def __init__(self, text):
        self.text = text
    @classmethod
    def deserialize(cls, d) :
        return cls.qtype_subclasses[d['type']].from_dict(d['text'], d['content'])
    def serialize(self) :
        return {"type" : self.typeName,
                "text" : self.text,
                "content" : self.to_dict()}


class AbstractMultiQType(QType) :
    def __init__(self, text, options) :
        QType.__init__(self, text)
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

class ScaleQType(QType) :
    typeName = "scale"
    def __init__(self, text, scalecont, scalemin, scalemax, scalestep):
        QType.__init__(self, text)
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

class TextQType(QType) :
    typeName = "text"
    def __init__(self, text, textlength):
        QType.__init__(self, text)
        self.textlength = textlength
    @classmethod
    def from_dict(cls, text, d) :
        return cls(text,
                   textlength=d['textlength'])
    def to_dict(self) :
        return { 'textlength' : self.textlength }

class GridQType(QType) :
    typeName = "grid"
    def __init__(self, text, rowoptions, coloptions):
        QType.__init__(self, text)
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
