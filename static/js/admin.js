      var seenEvents = {};

      $(onReady);

      function nocache() {
          return "?nocache=" + new Date().getTime();
      }
      function onReady() {
          $('#upload-btn').click(function(evt) {
              evt.preventDefault();
              uploadXML();
          });
          
          $('#begin-recruiting-button').click(function(evt) {
              evt.preventDefault();
              beginRecruiting();
          });
          
          $('#admin-begin-run').click(function(evt) {
              evt.preventDefault();
              beginRun();
          });
          
          $('#admin-end-run').click(function(evt) {
				evt.preventDefault();
				$('#admin-end-run').hide();
				$('#admin-end-run-submitting').show();		  
				$.post('/admin/recruit/end/', {}).always(function () {
					$.get('/admin/info/' + nocache(), function(data) {
					try {
						updateStatus(data,false);
						$('#admin-end-run').show();
						$('#admin-end-run-submitting').hide();
						$('#admin-end-run-original').hide();
						$('#admin-begin-run-original').show();				  
						$('#endRunModal').modal('hide');				  						
					}finally {}});
				});
          });			  						
          
          $('#download-data-btn').click(function(evt) {
              evt.preventDefault();
              window.location.href = '/admin/download/';
          });
          $('#download-bonusinfo-btn').click(function(evt) {
              evt.preventDefault();
              window.location.href = '/admin/bonusinfo/';
          });
          
          getStatus(true);
          getHITs();
      }
      
      function getHITs() {
          $.get('/admin/hits' + nocache(), function (data) {
              $('#admin-hits').hide();
              $('#admin-hit-tasks').hide();
              if (data.ids !== undefined) {
                  var ids = data.ids.slice();
                  ids.sort();
                  var $d = $('#admin-hits-dest');
                  $d.empty();
                  var sep = "";
                  for (var i = 0, hid; hid = ids[i]; i++) {
                      $d.append(sep);
                      sep = ", ";
                      var $a = $('<a href="#"/>').text(hid).attr('hit-id', hid);
                      (function (hid) {
                          $a.on("click", function (e) {
                              e.preventDefault();
                              showTasks(hid);
                              return false;
                          });
                      })(hid);
                      $d.append($a);
                  }
                  $('#admin-hits').show();
              }
          });
      }
      
      function beginRun(callback) {
          $('#admin-begin-run').hide();
          $('#admin-begin-run-submitting').show();		  
          $.post('/admin/recruit/begin', {}, callback).always(function () {
					$.get('/admin/info/' + nocache(), function(data) {
					try {
						updateStatus(data,false);
						$('#admin-begin-run').show();
						$('#admin-begin-run-submitting').hide();
						$('#admin-begin-run-original').hide();
						$('#admin-end-run-original').show();				  
						$('#beginRunModal').modal('hide');				  
					}finally {}});
              });
      }
      
      function getStatus(updateTurkInfo) {
          $.get('/admin/info/' + nocache(), function(data) {
              try {
				  updateStatus(data,updateTurkInfo);
              } finally {
                  setTimeout(getStatus, 5000);
              }
          }).fail(function () {
              $('#admin-server-info').html('<span class="error">Error updating server information</span>').show();
              setTimeout(getStatus, 5000);
          });
      }
	  
	  function updateStatus(data,updateTurkInfo){
                  if (data.authed) {
                      $('#admin-login-info').text('Logged in as ' + data.full_name + ' (' + data.email + ').');
                      $('#admin-server-info').text('Server is running in '+data.environment+' mode.');
                      $('#admin-superadmin').toggle(data.superadmin);
                      $('#admin-task-info').html(data.hitinfo.num_hits + ' HITs ('+ data.hitinfo.num_tasks +' tasks) loaded. ' + data.hitinfo.num_completed_hits + ' HITs ('+ data.hitinfo.num_completed_tasks +' tasks) complete. ');
                      if (!data.turkinfo || !data.turkbalance) {
                          $('#admin-turk-info').html('Could not authenticate with MTurk.');
                          $('#upload-btn').attr("disabled", false);
                          $('#upload-btn-title').attr("title", "");
                      } else {
                          $('#admin-turk-info').html('MTurk authenticated. Current balance: ' + data.turkbalance);
                          if (updateTurkInfo) {
                              var mturk_form = $('#admin-mturk-cred-form');
                              mturk_form.find('input[name="hit_payment"]:first').val(data.turkinfo.hitpayment);
                              mturk_form.find('input[name="hit_title"]:first').val(data.turkinfo.title);
                              var textarea = mturk_form.find('textarea[name="hit_description"]:first').val(data.turkinfo.description);
                              window.setTimeout(function () { textarea.trigger("scroll"); }, 0);
                              mturk_form.find('input[name="hit_keywords"]:first').val(data.turkinfo.keywords);
                              mturk_form.find('input[name="hit_bonus"]:first').val(data.turkinfo.bonus);
                          }
                          if (data.turkinfo.running) {
                              var amazonLink = data.turkinfo.admin_host + "/mturk/manageHIT?HITId=" + data.turkinfo.hitid;
                              $('#admin-turk-info').html('HIT id:  <a href="' + amazonLink + '" target="_blank">' + data.turkinfo.hitid + '</a>.');
                              $('#admin-hit-info').show();
                              $('#admin-hit-info').html('<a href="'+data.turkinfo.preview+'" target="_blank">View HIT</a>.');
                              $('#admin-begin-run-original').hide();
                              $('#admin-end-run-original').show();
                              $('#upload-btn').attr("disabled", true);
                              $('#upload-btn-title').attr("title", "An experiment is running.");
                              $('#download-bonusinfo-btn').attr("disabled", true);
                              $('#download-bonusinfo-btn-title').attr("title", "Stop the experiment to ensure MTurk workers are paid their bonuses.");
                          } else {
                              var amazonLink = data.turkinfo.admin_host + "/mturk/manageHITs";
                              $('#admin-turk-info').append('<p> Not currently running. <a href="' + amazonLink + '" target="_blank">Manage HITs</a></p>');
                              $('#admin-hit-info').hide();
                              $('#admin-end-run-original').hide();
                              $('#admin-begin-run-original').show();
                              $('#upload-btn').attr("disabled", false);
                              $('#upload-btn-title').attr("title", "");
                              $('#download-bonusinfo-btn').attr("disabled", false);
                              $('#download-bonusinfo-btn-title').attr("title", "");
                          }
                          
                      }
                      $('#admin-xml-upload').show();
                      $('#admin-mturk-cred').show();
                  } else {
                      if (data.reason === 'not_admin') {
                          $('#admin-login-info').html('You are not an admin.  Talk to a superadmin to add you to the admins.');
                      } else if (data.reason === 'no_login') {
                          // Not authenticated. Just redirect to the login page.
                          window.location = "/admin/login";
                      } else {
                          $('#admin-login-info').html('You cannot see this for some unknown reason.');
                      }
                  }

                  var resolvedStatuses = {};
                  var outstanding = data.hitstatus.outstanding || [];
                  for (var i = 0; i < outstanding.length; i++) {
                      resolvedStatuses[outstanding[i]] = 'outstanding';
                  }
                  var completed = data.hitstatus.completed || [];
                  for (var i = 0; i < completed.length; i++) {
                      resolvedStatuses[completed[i]] = 'completed';
                  }
                  $('[hit-id]').each(function () {
                      var hid = $(this).attr('hit-id');
                      var status = "unseen";
                      if (Object.prototype.hasOwnProperty.call(resolvedStatuses, hid)) {
                          status = resolvedStatuses[hid];
                      }
                      var fontweight = 'normal';
                      var fontstyle = 'normal';
                      var color = 'orange';
                      switch (status) {
                      case "outstanding" :
                          fontweight = "bold";
                          color = 'red';
                          break;
                      case "completed" :
                          fontstyle = 'italic';
                          color = 'green';
                          break;
                      case "unseen" :
                          // fallthrough
                      default :
                          break;
                      }
                      $(this).css({
                          'font-weight' : fontweight,
                          'font-style' : fontstyle,
                          'color' : color
                      });
                  });
                  var $aed = $('#admin-events-dest');
                  var events = data.events || [];
                  var newEvents = false;
                  for (var i = 0; i < events.length; i++) {
                      if (!seenEvents.hasOwnProperty(events[i].date)) {
                          seenEvents[events[i].date] = true;
                          newEvents = true;
                          var date = new Date(events[i].date);
                          var $el = $('<div class="event">');
                          $el.append($('<div class="event-date">').text(''+date));
                          $el.append($('<div class="event-text">').text(events[i].event));
                          $aed.append($el);
                      }
                  }
                  if (newEvents) {
                      $aed.scrollTop($aed[0].scrollHeight);
                  }
	  }
      
      function showTasks(hid) {
          var $h = $('#admin-hit-tasks');
          $h.hide().empty();
          $.get('/admin/hits/' + hid + nocache(), function (data) {
              $h.append($('<p/>').text("Tasks for " + hid));
              var $dest = $('<p/>').appendTo($h);
              var sep = "";
              for (var i = 0, tid; tid = data.tasks[i]; i++) {
                  $dest.append(sep);
                  sep = ", ";
                  var $a = $('<a target="_blank"/>').text(tid).attr('href', '/HIT/#task=' + tid);
                  $dest.append($a);
              }
              $h.append($("<p/>").append($("<a/>").text("Show HIT").attr('target', '_blank').attr('href', '/HIT/#id=' + hid)));
              $h.slideDown();
          });
      }
      
      function beginRecruiting(callback) {
          var form_elem = $('#admin-mturk-cred-form');
          var mturk_info = {hitpayment : parseFloat(form_elem.find('input[name="hit_payment"]:first').val()),
                            title : form_elem.find('input[name="hit_title"]').val(),
                            description : form_elem.find('textarea[name="hit_description"]').val(),
                            keywords : form_elem.find('input[name="hit_keywords"]').val(),
                            bonus : form_elem.find('input[name="hit_bonus"]').val()};
          for (var key in mturk_info) {
              if (mturk_info.hasOwnProperty(key) && !mturk_info[key]) {
                  alert('You must specify all fields.');
                  return;
              }
          }
          $.post('/admin/recruit/', {data : JSON.stringify(mturk_info)}, callback);
      }
      
	  // Add the following code if you want the name of the file appear on select
	  $(".xml-upload-file").on("change", function() {	
		var fileName = $(this).val().split("\\").pop();
		$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
      });

      function uploadXML() {
          $('#upload-btn').attr("disabled", true);
          $("#xml-upload-error").hide();
          $("#xml-upload-success").hide();
          var data = new FormData();
          data.append('file', $('#xml-upload-file')[0].files[0]);
          $("#xml-upload-message").text("Uploading...").fadeIn();
          $.ajax({
              url: '/admin/xmlupload/',
              data: data,
              cache: false,
              contentType: false,
              processData: false,
              type: 'POST',
              success: function(data){
                  $('#upload-btn').attr("disabled", false);
                  $("#xml-upload-message").hide();
                  if (data.success !== undefined) {
                      var $succ = $("#xml-upload-success");
                      $succ.text("Successfully uploaded.")
                      $succ.fadeIn();
                      //getStatus();
                  } else {
                      var $err = $("#xml-upload-error");
                      $err.text(data.error);
                      $err.fadeIn();
                  }
                  getHITs();
              },
              error: function () {
                  $('#upload-btn').attr("disabled", false);
              }
          });
      }
