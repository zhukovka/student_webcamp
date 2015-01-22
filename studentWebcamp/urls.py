from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
#         url(r'^$', 'studentWebcamp.views.home', name='home'),
    # Example:
    url(r'', include('plus.urls')),
    url(r'', include('courses.urls')),
    url(r'', include('courseSched.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
