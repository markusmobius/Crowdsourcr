import re
import validators

class QTypeRegistry(type) :
    def __init__(cls, name, bases, dct) :
        if hasattr(cls, "typeName") :
            Question.qtype_subclasses[cls.typeName] = cls
        super(QTypeRegistry, cls).__init__(name, bases, dct)

class Question(object) :
    __metaclass__ = QTypeRegistry
    qtype_subclasses = {}
    def __init__(self, varname=None, condition=None, questiontext=None, helptext=None, options=None, valuetype=None, bonus=None, bonuspoints=None):
        def validate_bonus(bonus) :
            if bonus == None or bonus == 'linear':
                return bonus
            else :
                try :
                    split_bonus = bonus.split(':')
                    bthresh = int(split_bonus[1])
                    if bthresh > 100 or bthresh < 0 or split_bonus[0] != 'threshold':
                        raise Exception('bthresh')
                    else :
                        return bonus
                except:
                    raise Exception('Question bonus string %s improperly formatted.' % bonus)

        def validate_bonuspoints(bonuspoints, bonus=bonus):
            try:
                bonuspoints = float(bonuspoints)
            except:
                raise Exception('bonus points for question %s must be coercible to float' % self.varname)

            if bonus is None and (bonuspoints is not None and bonuspoints != 0.0):
                raise Exception("Bonus points specified without a bonus type for question %s" % self.varname)

            if not bonuspoints >= 0:
                raise Exception('bonus points for question %s must be larger than 0' % self.varname)
            else:
                return bonuspoints

        self.varname = varname
        self.questiontext = questiontext
        self.helptext = helptext
        self.options = options
        self.bonus = validate_bonus(bonus)
        self.bonuspoints = validate_bonuspoints(bonuspoints)
        self.condition = condition
        self.valuetype = valuetype
    @classmethod
    def deserialize(cls, d) :
        return cls.qtype_subclasses[d['valuetype']].deserialize(d)
    def serialize(self) :
        return {'valuetype' : self.valuetype,
                'varname' : self.varname,
				'condition' : self.condition,
				'bonuspoints' : self.bonuspoints,
                'questiontext' : self.questiontext,
                'helptext' : self.helptext,
                'options' : self.options,
                'content' : self.content,
                'bonus' : self.bonus}
    def get_bonus(self):
        if not self.bonus:
            return None
        elif self.bonus == 'linear':
            bonus_dict = { 'type' : 'linear' }
        else:
            split_bonus = self.bonus.split(':')
            bonus_dict =  { 'type' : 'threshold',
                            'threshold' : int(split_bonus[1]) }

        bonus_dict['bonuspoints'] = self.bonuspoints
        return bonus_dict

    def parse_condition(self, condition_string):
        """
        The only conditions that are allowed use "==" or "!=". Whitespace around
        the comparator is allowed
        """
        if condition_string is None:
            return None
        else:
            condition_pattern = re.compile(r'(?P<varname>\b\S+\b)\s*(?P<comparator>==|!=)\s*(?P<value>\b\S+\b)')
            return condition_pattern.finditer(condition_string).next().groupdict()
    def satisfies_condition(self, module_responses):
        condition_dict = self.parse_condition(self.condition)
        if condition_dict is None:
            return True
        else:
            # extract from the response the variable that is affected by the condition
            condition_variable = [r for r in module_responses if r['varname'] == condition_dict['varname']][0]

            if((condition_dict['comparator'] == '==') and (condition_variable['response'] == condition_dict['value'])):
                return True
            elif((condition_dict['comparator'] == '!=') and (condition_variable['response'] != condition_dict['value'])):
                return True
            else:
                return False
    def sanitize_response(self, response):
        return response
    def valid_response(self, response):
        return True
    def validate(self, response, module_responses) :
        """Takes a question response as transmitted via JSON and validates it 
           given its own response and that to the rest of the question list.
           The method calls satisfies_condition(), which checks whether the
           display condition for the question is met and valid_response(), which
           checks that the response to the question itself is valid. The latter
           method can be overridden in classes that inherit from Question."""

        if not self.satisfies_condition(module_responses):
            return True
        else:
            return self.valid_response(response)

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
    def valid_response(self, response) :
        return response.get('response', False)

class NumericQuestion(AbstractQuestion):
    typeName = 'numeric'
    @staticmethod
    def parse_content_from_xml(question_content=None):
        return []
    def valid_response(self, response) :
        try :
            v = float(response.get('response', False))
            return True
        except ValueError :
            return False
    
class TextQuestion(AbstractQuestion) :
    typeName = 'text'
    @staticmethod
    def parse_content_from_xml(question_content=None):
        return []
    def sanitize_response(self, response):
        response['response'] = response['response'].strip()
        return response
    def valid_response(self, response) :
        return response.get('response', False)

class URLQuestion(TextQuestion) :
    typeName = 'url'
    @staticmethod
    def stem_url(url):
        # strip protocols and 'www'
        url = re.sub(r"^https?:\/\/(www.)?", "", url)
        # strip trailing slashes
        url = re.sub(r"\/$", "", url)
        return url
    def sanitize_response(self, response):
        # run all the standard text response cleaning before stripping the URL down
        response['response'] = super(TextQuestion, self).sanitize_response(response['response'])
        response['response'] = response['response'].lower()
        response['response'] = self.stem_url(response['response'])
        return response
    def valid_response(self, response) :
        if not response.get('response', False):
            return False
        return validators.url(response.get('response', False), public = True)

class CommentQuestion(TextQuestion) :
    typeName = 'comment'
    def validate(self, response, module_responses):
        return True

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
