from django.contrib import admin

from .models import CourseSched


# Register your models here.
class CourseSchedAdmin(admin.ModelAdmin):
    class Meta:
        model = CourseSched

admin.site.register(CourseSched, CourseSchedAdmin)