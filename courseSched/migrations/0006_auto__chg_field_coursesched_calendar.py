# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CourseSched.calendar'
        db.alter_column(u'courseSched_coursesched', 'calendar', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True))

    def backwards(self, orm):

        # Changing field 'CourseSched.calendar'
        db.alter_column(u'courseSched_coursesched', 'calendar', self.gf('django.db.models.fields.URLField')(default=datetime.datetime(2014, 6, 26, 0, 0), max_length=200, unique=True))

    models = {
        u'courseSched.coursesched': {
            'Meta': {'object_name': 'CourseSched'},
            'calendar': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'}),
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
        }
    }

    complete_apps = ['courseSched']