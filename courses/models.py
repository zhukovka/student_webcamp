from django.db import models
from django.utils.encoding import smart_unicode


# Create your models here.
class CourseManager(models.Manager):
    def createCourse(self, title):
        course = self.create(title=title)
        return course

class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    subscribers = models.PositiveIntegerField(default=0)
    objects = CourseManager()
    
    def __unicode__(self):
        return smart_unicode(self.title)

# course = Course.objects.createCourse(title)

class ContentManager(models.Manager):
    def createContent(self, course, name):
        content = self.create(course=course, name=name)
        return content

class Content(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return smart_unicode(self.name)
