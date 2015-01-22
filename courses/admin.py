from django.contrib import admin

from .models import Course, Content


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course

class ContentAdmin(admin.ModelAdmin):
    class Meta:
        model = Content

admin.site.register(Course, CourseAdmin)
admin.site.register(Content, ContentAdmin)