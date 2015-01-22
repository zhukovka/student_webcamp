from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.http import Http404
from courses.models import Course, Content
from courseSched.models import CourseSched
# Create your views here.

def index(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request, 'courses/index.html', context)

def course(request, course_title):
    print(request.path, "here")
    courses = Course.objects.all()
    course = get_object_or_404(Course, title = course_title)
    contents = get_list_or_404(Content, course__title=course.title)
    schedules = CourseSched.objects.filter(course=course)
    context = {'courses':courses, 'contents':contents, 'courseTitle':course_title, 'schedules':schedules}
    return render(request, 'courses/course.html', context)