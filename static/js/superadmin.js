/*global jQuery $ _*/

$(function() {
    reloadAdminList();

    $('#create-new-admin-form').submit(function(evt) {
	evt.preventDefault();
	var new_admin_email = $(this).find('input:first').val();
	$(this)[0].reset();
	$.post('/admin/new', {data : JSON.stringify({email : new_admin_email})}, function() {
	    reloadAdminList();
	});
    });
    
});

function reloadAdminList() {
    $.get('/admin/all', function(data) {
	var admin_view_holder = $('div.all-admin-view');
	var admin_list = $(document.createElement('ul')).addClass('pretty-list');
	for (var i = 0; i < data.length; i++) {
	    var anchor_holder = $(document.createElement('a')).attr('href', '#').html(data[i]);
            admin_list.append($(document.createElement('li')).html(anchor_holder));
	}
	admin_view_holder.html(admin_list);
    });
}
