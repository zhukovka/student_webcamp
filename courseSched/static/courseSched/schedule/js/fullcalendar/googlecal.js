	function agendaInsert(root) {
	 	var feed = root.feed;
    	var entries = feed.entry || [];
    	courseDays = [];
		var daysToDelete = [];
    	for (var i = 0; i < entries.length; ++i) {
		      var entry = entries[i];
		      var title = (entry.title.type == 'text') ? entry.title.$t : escape(entry.title.$t);
		      var published = moment(entry.published['$t']);
		      if(entry['gd$originalEvent']){
		      		daysToDelete.push(moment(entry['gd$originalEvent']['gd$when'].startTime));
		      }
		      if(entry['gd$when']){
		      	var start = moment(entry['gd$when'][0].startTime);
		      	var end = moment(entry['gd$when'][0].endTime);
		      	var duration = end.diff(start, 'hours');
		      	var day = new courseDay(start, end, duration, title);
		      	courseDays.push(day);
		      } else if(entry['gd$recurrence']){
		      	var recurCourseDays = getFromRecurence(entry, title);
		      	courseDays = courseDays.concat(recurCourseDays);
		      }
		      else{
		      	$('#agenda').append('<p><a class="dateList">'+title+'</a></p>');
		      }
		      
		    }

		if(daysToDelete){courseDays = deleteFromOriginal(daysToDelete, courseDays)};
		courseDays.sort(function(obj1, obj2) {
					// Ascending: first date less than the previous
						return obj1.start - obj2.start;
				});
		var courses = {};
		var now = moment();
		for (var i = 0; i < courseDays.length; i++) {
			courseDays[i].title = courseDays[i].title.replace(/\d+/g, "");
			eachCourse(courseDays[i], courses);
			if(isNearest(courseDays[i], now)){
				htmlCourseDays(courseDays[i], $('#agenda'), title);
			}
		};
		for(course in courses){
			if(isCurrentCourse(courses[course], now)){
				htmlCourse(course, courses[course], $('#current'));
			}
			else if(isNextCourse(courses[course], now)){
				htmlCourse(course, courses[course], $('#next'));
			}
		}

	 }

	 

	function getFromRecurence(obj, title) {
		/*make array of courseDay object from google calendar 
		reccurance string
	 	@obj - GC event (JSON), has property gd$recurrence 
	 	-> one string $t
		returns array of courseDays obj-s
	 	*/
	 	var recData = obj['gd$recurrence']['$t'];

	 	var recObj = parseRecuranceString(recData);
	 	var startMoment = recObj.startMoment;
	 	var endMoment = recObj.endMoment;
	 	var lastMoment = recObj.lastMoment;
	 	var daysRepeat = recObj.daysRepeat;
	 	
	 	var duration = endMoment.diff(startMoment, 'hours');
	 	//recur() - momentJs recur plugin func
	 	var recurrence = startMoment.recur({start:startMoment, end:lastMoment}).every(daysRepeat).daysOfWeek();
	 	var allDates = recurrence.all("L");
	 	var days = [];
	 	for (var i = 0; i < allDates.length; i++) {
	 		var day = moment(allDates[i], 'MM-DD-YYYY');
	 		var startHour = startMoment.hours();
		 	var startMinutes = startMoment.minutes();
	 		var courseDayStart = day.add('hours', startHour).add('minutes', startMinutes);
	 		var courseDayEnd = courseDayStart.clone().add(duration, 'hours');
	 		var CourseDay = new courseDay(courseDayStart, courseDayEnd, duration, title);
	 		days.push(CourseDay);
	 	}
	 	return days;
	}

	function parseRecuranceString(recData){
		/*
			parses recurance string from google calendar event obj
			@recData - recurance string from google calendar event obj
			returns object {
			startMoment - first day start date and time, 
			endMoment - first day end date and time, 
			lastMoment - last day start date and time, 
			daysRepeat - weekdays names of recurance} 
		 */
		var recDataArray = recData.split('\n')
		/*@re - regex to match time like 20140627T143000*/
	 	var re = /\d{8}\T\d{6}/g;
	 	for (var i = 0; i < recDataArray.length; i++) {
	 		if(recDataArray[i].indexOf('DTSTART;')>=0){
	 			var startMoment = moment((recDataArray[i].match(re))[0], 'YYYY-MM-DD HH:mm'); 
	 			}
	 		else if(recDataArray[i].indexOf('DTEND;')>=0){
	 			var endMoment = moment((recDataArray[i].match(re))[0], 'YYYY-MM-DD HH:mm');
	 		}
	 		else if(recDataArray[i].indexOf('UNTIL')>=0){
	 			var lastMoment = moment((recDataArray[i].match(re))[0], 'YYYY-MM-DD HH:mm Z');
		 		if(recDataArray[i].indexOf('BYDAY=')>=0){
		 			var fromIndex = recDataArray[i].lastIndexOf('=')+1;
		 			var daysRepeat = recDataArray[i].slice(fromIndex).split(',');
		 		}
	 		}
	 	}

	 	return {
	 		startMoment:startMoment, 
	 		endMoment:endMoment, 
	 		lastMoment:lastMoment, 
	 		daysRepeat:daysRepeat
	 	} 
	}

	function deleteFromOriginal(daysToDelete, courseDays) {
		/*removes duplicate events
			@daysToDelete - array of momentJs objs days to delete
			@courseDays - array of courseDay objs to delete days from
			return new array without daysToDelete
		*/
		var courseDaysCopy = courseDays.slice(0);
		for (var i = 0; i < courseDaysCopy.length; i++) {
			for (var j = 0; j < daysToDelete.length; j++) {
				if((courseDaysCopy[i].start).isSame(daysToDelete[j])){
					courseDays.splice(courseDays.indexOf(courseDaysCopy[i]), 1);
				}
			};
		};
		return courseDays;
	}

	function eachCourse (courseDay, courses) {
		/*gets one course and makes @courses obj*/
		if(!courses[courseDay.title]){
			courses[courseDay.title] = {};
			courses[courseDay.title]["lessons"] = [courseDay];
			courses[courseDay.title]["duration"] =  courseDay.duration;
			courses[courseDay.title]["start"] =  courseDay.start;
			courses[courseDay.title]["end"] =  courseDay.start;
			courseDay.title += ' '+1;
		}
		else{
			courses[courseDay.title]["lessons"].push(courseDay);
			courses[courseDay.title]["end"] =  courseDay.start;
			courseDay.title += ' '+courses[courseDay.title]["lessons"].length;
		}
	}


	function courseDay(startMoment, endMoment, duration, title) {
		/*Creates courseDay object 
			@startMoment - MomentJs obj: start of the event
			@endMoment - MomentJs obj: end of the event
			@duration - int: the event duration in hours
		*/
		this.start = startMoment;
		this.end = endMoment;
		this.duration = duration;
		this.title = title;
	}

	function isNearest (courseDay, today) {
		/*checks if time range of courseDay start
			@courseDay - courseDay obj
		*/
		var nextMonth = today.clone().add('weeks', 8);
		
		return ((courseDay.start).isAfter(today) 
			&& (courseDay.start).isBefore(nextMonth));
	}
	
	function htmlCourseDays(courseDay, el, title) {
		 /*htmlRecurance make html from object
		 @courseDay - courseDay object
		 @el - html element to fill with content from obj*/
		 	var start = courseDay.start;
		 	var end = courseDay.end;
		 	var newP = document.createElement("p");
		 	el.append(newP);
		 	$(newP).append('<a class="dateList" data-start="'+start.format()+'" data-end="'+end.format()+'">'+courseDay.title+'</a>');
	 }
	
	function isCurrentCourse (course, today) {
		/*is current course from courses obj*/
		return course.start.isBefore(today) && course.end.isAfter(today);
	}
	function isNextCourse (course, today) {
		/*is current course from courses obj*/
		return course.start.isAfter(today);
	}

	function htmlCourse(title, course, el){
		var content = ['<p class="course-title"> Курс: <span>'+ title+'</span></p>',
			'<p class="start"> Первое занятие: <span>'+ course.start.lang('ru').format("dddd MMMM Do YYYY, HH:mm")+'</span></p>',
			'<p class="end"> Последнее занятие: <span>'+ course.end.lang('ru').format("dddd MMMM Do YYYY, HH:mm")+'</span></p>',
			'<p> Всего занятий: '+ course.lessons.length+'</p>',
			'<p> Занятие длится: '+ moment.duration(course.duration, 'hours').lang('ru').humanize()+'</p>']
			el.append(content);
	}

