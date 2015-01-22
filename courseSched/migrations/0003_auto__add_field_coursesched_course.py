# -*- coding: utf-8 -*-
from django.db import models

from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CourseSched.course'
        db.add_column(u'courseSched_coursesched', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['courses.Course']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CourseSched.course'
        db.delete_column(u'courseSched_coursesched', 'course_id')


    models = {
        u'courseSched.coursesched': {
            'Meta': {'object_name': 'CourseSched'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['courseSched']