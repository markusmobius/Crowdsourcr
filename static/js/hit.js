/*global $ jQuery _*/

$(onLoad);

function getAdminTask() {
    var hash = $(window.location).attr('hash');
    var prefix = '#task=';
    if (hash.slice(0, prefix.length) === prefix) {
        return hash.slice(prefix.length);
    } else {
        return undefined;
    }
}

var haveUsedForcedHit = false;
function getForcedHit() {
    if (haveUsedForcedHit) return undefined;
    haveUsedForcedHit = true;
    var hash = $(window.location).attr('hash');
    var prefix = '#id=';
    if (hash.slice(0, prefix.length) === prefix) {
        return hash.slice(prefix.length);
    } else {
        return undefined;
    }
}

function ping() {
    $.post('/worker/ping', {}, function(data) {
        $("#ping-error").hide();
        setTimeout(ping, 5000);
    }).fail(function () {
        if (!$("#ping-error").is(":visible")) {
          $("#ping-error").show();
          scrollToTop($("#hit-modules-scroll"));
        }
        setTimeout(ping, 5000);
    });
}

function scrollToTop($div) {
  $div.animate({scrollTop : 0}, 500);
}
function scrollToBottom($div) {
  $div.animate({scrollTop : $div[0].scrollHeight}, 500);
}

var currentTypeGroup = null;

function showWithData(task, modules) {
    $('#survey-panel').show();
    $('#login-card').hide();
    var iframe = $('<iframe src="about:blank" frameborder="0" border="0" cellspacing="0"/>');
    $('#hit-content').empty().append(iframe);
    _.defer(function () {
		iframe.contents()[0].write('<head><meta charset="utf-8" /><link rel="stylesheet" href="/static/css/bootstrap.min.css" type="text/css"/><script src="/static/js/jquery-3.4.1.min.js"></script><script src="/static/js/bootstrap.min.js"></script></head><body>');
        iframe.contents()[0].write(task.content);
		iframe.contents()[0].write('</body>');
    });
    currentTypeGroup = new CTypeGroup();
    $('#hit-modules').empty();
    for (var i = 0; i < task.modules.length; i++){
        var dest = $('<div/>').appendTo($('#hit-modules'));
        registerModule(i, modules[task.modules[i]], dest);
    }
}

var hitLoadingTime = undefined;
var maxWaitingTime = 45 * 1000;

function requestNextTask(response) {
    // Response is from the server indicating whether validation succeeded.
    $("#next-task-button").attr('disabled', false);
    if (response && response.error) {
	      switch (response.explanation) {
	      case 'no_cookies' :
            $("#next-task-button").attr('disabled', true);
            $("#other-error").show().text('Your cookies were cleared and you are no longer authenticated. Please reload this page and login with your worker id again.');
            scrollToTop($("#hit-modules-scroll"));
	          break;
	      case 'not_logged_in' :
            $("#next-task-button").attr('disabled', true);
            $("#other-error").show().text('You are not logged in. Please reload this page and login with your worker id again.');
            scrollToTop($("#hit-modules-scroll"));
	          break;
	      case 'invalid_response' :
            $("#validation-error").show();
            scrollToBottom($("#hit-modules-scroll"));
            break;
        default :
            $('#unknown-error').show();
            scrollToBottom($("#hit-modules-scroll"));
            break;
	      };
	      return;
    }

    if (hitLoadingTime === undefined) {
	      hitLoadingTime = Date.now();
    }
    if (getAdminTask() !== undefined) {
        $('#next-task-button').attr('disabled', true);
        $('#return-hit').attr('disabled', true);
        $('#hit-progress').text("Single task view");
        $.get('/admin/tasks/' + getAdminTask(), function (data) {
            $('.loading-holder').hide();
            showWithData(data.task, data.modules);
        });
        return;
    }
    var getData = {};
    var forcedId = getForcedHit();
    if (forcedId !== undefined) {
        getData['force'] = true;
        getData['hitid'] = forcedId;
        getData['workerid'] = $('#workerID').val();
    }
    $.post('/HIT/view/', getData, function(data) {
	      $('.loading-holder').hide();
	      if (data.no_hits) {
	          $('#survey-panel').hide();
	          $('#login-card').hide();
	          $('#turk-verify-content').hide();
	          if (data.unfinished_hits && (Date.now() - hitLoadingTime) < 45000) {
		            $('.loading-holder').show();
		            setTimeout(requestNextTask, 5000);
	          } else {
		            $('#turk-no-hits').show();
	          }
	          return;
	      }

	      if (data.needs_login) {
	          if (data.reforce) {
                haveUsedForcedHit = false;
            }
	          $('#login-card').show();
            $('#login-card').find('input').focus();
	          return;
	      }
	      
	      $('#survey-panel').show();
	      $('#login-card').hide();

	      if (data.reload_for_first_task) {
	          requestNextTask();
	      } else if (data.completed_hit) {
	          $('#survey-panel').hide();
	          $('#login-card').hide();
	          $('#secret-code').val(data.verify_code);
	      } else {
            $('#hit-progress').text("You are on task " + (+data.task_num + 1) + " of " + data.num_tasks  + ".");
            showWithData(data.task, data.modules);
	      }
    });
}

function onLoad() {
    ping();

    $('#return-hit').click(function(e) {
	      e.preventDefault();
	      if (window.confirm('Are you sure you want to return this HIT? You will lose all of your progress and this HIT will be assigned to another worker.')) {
	          window.location.href = '/HIT/return';
	      }
    });

    $('#next-task-button').click(function(evt) {
	      evt.preventDefault();
        $("#validation-error").hide();
        $("#unknown-error").hide();
        if (currentTypeGroup.validate()) {
	          submitTask(requestNextTask);
        } else {
            var invalidQ = $(".question-invalid");
            if (invalidQ) {
                $("#hit-modules-scroll").prop("scrollTop", invalidQ.prop("offsetTop")-16*5);
            }
        }
    });

    $('#worker-login-submit').click(function(evt) {
	      evt.preventDefault();
	      $.post('/worker/login/', {'workerid' : $('#workerID').val()}, requestNextTask);
    });

    $('body').on('click', function (e) {
        var target = $(e.target);
        if (!target.hasClass('popover') && !target.parent().hasClass('popover') && !target.hasClass('help')) {
            $('.help').each(function() {
		            $(this).popover('hide');
            });
        }
    });

	$('#secret-code-copy').click(function(evt) {
		var copyText = document.getElementById("secret-code");
		copyText.select();
		copyText.setSelectionRange(0, 99999); /*For mobile devices*/
		/* Copy the text inside the text field */
		document.execCommand("copy");		
    });
	
    requestNextTask();
}

function submitTask(callback) {
    $("#next-task-button").attr('disabled', true);
    $.post('/HIT/submit/', {data : JSON.stringify(serializeModules())}, callback)
     .fail(function () {
        $('#unknown-error').show();
        scrollToBottom($("#hit-modules-scroll"));
        $("#next-task-button").attr('disabled', false);
     });
}

function serializeModules() {
    return currentTypeGroup.serialize();
}

function registerModule(i, data, dest) {
	console.log(data);
    var module_container = $(document.createElement('div'));
	console.log("hello1");
    var module = module_container.CType(currentTypeGroup, data);
	console.log("hello2");
	console.log(module);
    module.renderDisplay();
	console.log("hello3");	
    dest.append($(document.createElement('li')).html(module_container));
    if (i == 0) {
        currentTypeGroup.showType(module);
    }
}
