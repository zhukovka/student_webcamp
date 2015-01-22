'''
Created on Jun 4, 2014

@author: lenka
'''
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^courses/(?P<course_title>\w+)/$', views.course, name='course'),
                       url(r'^fullcalendar/', TemplateView.as_view(template_name="courses/fullcalendar.html"),),
                       )
