'''
Created on Jun 26, 2014

@author: lenka
'''
from django.conf import settings
from django.views.generic import TemplateView

from django.conf.urls import patterns, url

from plus import views


urlpatterns = patterns('',
                        (r'^plus$', 'plus.views.index'),
                        (r'^cal$', 'plus.views.cal'),
                        (r'^cal2$', 'plus.views.cal2'),
                        (r'^yt$', 'plus.views.yt'),
                        (r'^oauth2callback', 'plus.views.auth_return'),
                        (r'^accounts/login/$', 'django.contrib.auth.views.login', 
                                            {'template_name': 'plus/login.html'}),
                       )