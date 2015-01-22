import datetime
from django.db import models
from django.utils.encoding import smart_unicode


from courses.models import Course


# Create your models here.
class CourseSched(models.Model):
    title = models.CharField(max_length=100, unique=True)
    calendar = models.CharField(max_length=100, null=True, unique=True)
    course = models.ForeignKey(Course)
    def __unicode__(self):
        return smart_unicode(self.title)