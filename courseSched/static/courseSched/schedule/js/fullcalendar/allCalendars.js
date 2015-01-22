$(document).ready(function() {
	$.expr[":"].contains = $.expr.createPseudo(function(arg) {
	    return function( elem ) {
	        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
	    };
	});

	$.each($('.calendars'), function(index, element) {
		 /* iterate through array or object */

		 var title = $(this).attr('data-title').toLowerCase();
		 // var title = 'basic';
		 var ref = $(this).attr('href');
		var feed = $.getJSON('http://www.google.com/calendar/feeds/'+element.id+'/public/full?alt=json', function(json, textStatus) {
				/*optional stuff to do after success */
				$.getScript( "/static/courseSched/schedule/js/fullcalendar/googlecal.js" )
				  .done(function( script, textStatus ) {
				    agendaInsert(json);
					$( "p:contains('" + title + "')>span" ).replaceWith($('<a href="'+ref+'">'+title+'</a>'));
				  });
		});
		
	});

	
});