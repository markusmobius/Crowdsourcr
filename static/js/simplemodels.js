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
    },
    serialize : function() {
	return {
	    name : this.name,
	    responses : this.questionlist.serialize()
	};	    
    }
});


var QuestionList = Model.extend({
    constructor : function(questions) {
	this.questions = questions || [];
	this.display_template = $('#questionlist-display-template').html();
	this.renderedquestions = [];
    },
    renderDisplay : function(el) {
        this.el = $(el);
	this.el.empty();
	for (var i = 0; i < this.questions.length; i++) {
	    var question_holder = $(document.createElement('li'));	    
	    var question = new Question(question_holder, this.questions[i]);
	    question.renderDisplay();
	    this.el.append(question_holder);
	    this.renderedquestions.push(question);
	}	
    },
    serialize : function() {
	var all_question_responses = [];
	for (var i = 0; i < this.renderedquestions.length; i++) {
	    all_question_responses.push(this.renderedquestions[i].serialize());
	}
	return all_question_responses;
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
    },
    serialize : function() {
	return { 
	    varname : this.varname,
	    response : this.response()
	};
    },
    serializeForDisplay : function() {
	return {
	    questiontext : this.questiontext,
	    valuetype : this.valuetype,
	    varname : this.varname,
	    content : this.content
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
        this.el.html(_.template(this.display_template, this.serializeForDisplay()));
    },
    response : function() {
	return this.el.find('input:first').val();
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
        this.el.html(_.template(this.display_template, this.serializeForDisplay()));
    },
    response : function() {
	return this.el.find('input:checked').val();
    } 
});