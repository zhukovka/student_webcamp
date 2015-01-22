$(document).ready(function() {
	// https://www.google.com/calendar/feeds/73o0f5i4q8moa4o1q3kabeeak0%40group.calendar.google.com/public/basic 
	// https://www.google.com/calendar/render?cid=bfj0ablplj22c39b0mbhikl8ng%40group.calendar.google.com
	var renderUrl = 'https://www.google.com/calendar/render?cid='+calUrl;
	$('#render').attr('href', renderUrl);
	var calFeed = 'https://www.google.com/calendar/feeds/'+calUrl+'/public/full';
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
// Qtip
	var tooltip = $('<div/>').qtip({
		id: 'calendar',
		prerender: true,
		content: {
			text: ' ',
			title: {
				button: true
			}
		},
		position: {
			my: 'bottom center',
			at: 'top center',
			target: 'mouse',
			viewport: $('#calendar'),
			adjust: {
				mouse: false,
				scroll: false
			}
		},
		show: false,
		hide: false,
		style: 'qtip-light'
	}).qtip('api');

// Fullcalendar
	$('#calendar').fullCalendar({
			header:{
				    left:   'title',
				    center: 'agendaDay,agendaWeek,month',
				    right:  'today prev,next'
				},
			lang:"ru",
			eventClick: function(data, event, view) {
				var content = '<h3>'+data.title+'</h3>' + 
					'<p><b>Начало:</b> '+data.start.format("MMMM Do YYYY, HH:mm")+'<br />' + 
					(data.end && '<p><b>Завершение:</b> '+data.end.format("MMMM Do YYYY, HH:mm")+'</p>' || '');

				tooltip.set({
					'content.text': content
				})
				.reposition(event).show(event);
			},
	        dayClick: function() { tooltip.hide() },
			viewDisplay: function() { tooltip.hide() },
		/*Calendars */

			eventSources: [
	            {events: courseDays,
	            	className: 'gcal-event',
	            },
	            {
	                url: 'https://www.google.com/calendar/feeds/en.ukrainian%23holiday%40group.v.calendar.google.com/public/basic',
	            	className: 'gcal-event',
	            	color: '#FE9F8B'
	            }
	        ],
	    /*View options*/
        	defaultView: "agendaWeek",
        	columnFormat:{
			    month: 'ddd',    // Mon
			    week: 'ddd MMM D', // Mon 9/7
			    day: 'dddd'      // Monday
			},
        	axisFormat: 'HH:mm',
        	firstDay: 1,
        	minTime: "11:00:00",
        	maxTime: "22:00:00",
        	timeFormat: 'HH:mm',

        /*Event render*/
		    eventRender: function(event, element) {
		    	element.qtip({
		    			content: {
						        title: event.title,
						        text: event.description
						    }
			        });
		    	
		        } 
		});


/* Extra funcs */

	var allEvents = $('.dateList');
	allEvents.click(function(event) {
		/* Act on the event */
		event.preventDefault();
		$('#calendar').fullCalendar('gotoDate', 
			$(this).attr('data-start'));
		var t = $.trim($(this).text());
		var lastClickedEv = $('#calendar').fullCalendar('clientEvents', 
			function(event){return event.className.indexOf("highlight")>=0})[0];
		var clickedEv = $('#calendar').fullCalendar('clientEvents', 
			function(event){return event.title==t})[0];
		if(lastClickedEv){
			lastClickedEv.className.splice(lastClickedEv.className.indexOf('highlight'), 1);
			$('#calendar').fullCalendar('updateEvent', lastClickedEv);
		};
		clickedEv.className.push('highlight');
		$('#calendar').fullCalendar('updateEvent', clickedEv);
	}).css('cursor', 'pointer');

});
