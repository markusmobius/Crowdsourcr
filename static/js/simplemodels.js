/*global jQuery Model _ $*/

"use scrict";

jQuery.fn.CType = function(params) {
    return new CType(this[0], params);
};

var CType = Model.extend({
    constructor : function(el, params) {
	params = params || {};
	this.el = $(el);
	this.display_template = $('#ctype-display-template').html();
	this.name = params.name || '';
	this.header = params.header || '';
	this.questionlist = new QuestionList(params.questions || []);
	this.el.empty();
    },
    renderDisplay : function() {
	var self = this;
	var sub_disp = $(document.createElement('div'));
	sub_disp.html(self.display_template);
	this.el_display_props = sub_disp.find('[data-prop]');
	this.question_container = sub_disp.find('.question-display-container:first');
	this.questionlist.renderDisplay(this.question_container);
	this.el.append(sub_disp);
	this.updateDisplay();
    },
    objectifyDisplay : function() {
	return {
	    name : this.name,
	    header : this.header
	};
    }
});


var QuestionList = Model.extend({
    constructor : function(questions) {
	this.questions = questions || [];
	this.display_template = $('#questionlist-display-template').html();
    },
    renderDisplay : function(el) {
        this.el = $(el);
	this.el.empty();
	console.log(this.questions);
	for (var i = 0; i < this.questions.length; i++) {
	    var question_holder = $(document.createElement('li'));	    
	    new Question(question_holder, this.questions[i]).renderDisplay();
	    this.el.append(question_holder);
	}	
    }
});

var Question = Model.extend({
    constructor : function(el, question) {
	switch (question.valuetype) {
	    case 'numeric':
                return new NumericQuestion(el, question);
	    case 'categorical':
	    	 return new CategoricalQuestion(el, question);
            default:
		throw "Error: could not find type "+question.valuetype;
	}	
    }
});

var NumericQuestion = Question.extend({
    constructor : function(el, question) {
        this.el = $(el);
	this.display_template = $('#numericquestion-display-template').html();
	this.valuetype = question.valuetype;
	this.questiontext = question.questiontext;
	this.varname = question.varname;
	this.content = question.content;
    },
    renderDisplay : function() {
        this.el.empty();
        this.el.html(_.template(this.display_template, this.serialize()));
    },
    serialize : function() {
        return {valuetype : this.valuetype,
	        questiontext : this.questiontext,
 		varname : this.varname,
		content : this.content};
    }   
});

var CategoricalQuestion = Question.extend({
    constructor : function(el, question) {
        this.el = $(el);
	this.display_template = $('#catquestion-display-template').html();
	this.valuetype = question.valuetype;
	this.questiontext = question.questiontext;
	this.varname = question.varname;
	this.content = question.content;
    },
    renderDisplay : function() {
        this.el.empty();
        this.el.html(_.template(this.display_template, this.serialize()));
    },
    serialize : function() {
        return {valuetype : this.valuetype,
	        questiontext : this.questiontext,
 		varname : this.varname,
		content : this.content};
    } 
});