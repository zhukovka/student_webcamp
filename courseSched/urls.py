'''
Created on Jun 23, 2014

@author: lenka
'''
from django.conf import settings
from django.views.generic import TemplateView

from django.conf.urls import patterns, url

from courseSched import views


urlpatterns = patterns('',
                       url(r'^courses/(?P<course_title>\w+)/schedules/$', views.scheds, name='shedules'),
                        url(r'^courses/(?P<course_title>\w+)/schedules/(?P<sched_title>\w+(-\w+)+)/', views.sched, name='shedule'),
                       )