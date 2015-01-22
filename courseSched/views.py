import logging
from django.http import Http404
from django.http import HttpResponse
from apiclient.discovery import build
from django.shortcuts import render, get_object_or_404, get_list_or_404

from courses.models import Course, Content

from .models import CourseSched


# Create your views here.
def scheds(request, course_title):
    courses = Course.objects.all()
    course = get_object_or_404(Course, title = course_title)
    schedules = get_list_or_404(CourseSched, course=course)
    context = {'courses':courses, 'course':course, 'schedules':schedules, 'courseTitle':course_title}
    return render(request, 'courseSched/schedules.html', context)

def sched(request, course_title, sched_title):
    schedTitle = sched_title.replace("-", " ")
    courses = Course.objects.all()
    course = get_object_or_404(Course, title = course_title)
    schedules = get_list_or_404(CourseSched, course=course)
    schedule = get_object_or_404(CourseSched, title__icontains=schedTitle)
    #     Google calendar feed
    api_key = 'AIzaSyDbNTPNlyOgZDUQCF2pfDQ1YOGnxNiWIWI'
    service = build("calendar", "v3", developerKey=api_key)
    events = service.events()
    eventList = events.list(calendarId=schedule.calendar).execute()
    logging.info(eventList)
    #     context
    context = {'courses':courses, 'course':course, 'schedules':schedules, 
               'schedule':schedule, 'courseTitle':course_title,'eventList':eventList}
    return render(request, 'courseSched/schedule.html', context)
