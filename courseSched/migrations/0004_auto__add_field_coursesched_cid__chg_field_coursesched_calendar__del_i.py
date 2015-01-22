# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CourseSched.cid'
        db.add_column(u'courseSched_coursesched', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)


        # Renaming column for 'CourseSched.calendar' to match new field type.
        db.rename_column(u'courseSched_coursesched', 'calendar_id', 'calendar')
        # Changing field 'CourseSched.calendar'
        db.alter_column(u'courseSched_coursesched', 'calendar', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200))
        # Removing index on 'CourseSched', fields ['calendar']
        db.delete_index(u'courseSched_coursesched', ['calendar_id'])

        # Adding unique constraint on 'CourseSched', fields ['calendar']
        db.create_unique(u'courseSched_coursesched', ['calendar'])


    def backwards(self, orm):
        # Removing unique constraint on 'CourseSched', fields ['calendar']
        db.delete_unique(u'courseSched_coursesched', ['calendar'])

        # Adding index on 'CourseSched', fields ['calendar']
        db.create_index(u'courseSched_coursesched', ['calendar_id'])

        # Deleting field 'CourseSched.cid'
        db.delete_column(u'courseSched_coursesched', 'cid')


        # Renaming column for 'CourseSched.calendar' to match new field type.
        db.rename_column(u'courseSched_coursesched', 'calendar', 'calendar_id')
        # Changing field 'CourseSched.calendar'
        db.alter_column(u'courseSched_coursesched', 'calendar_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Calendar']))

    models = {
        u'courseSched.coursesched': {
            'Meta': {'object_name': 'CourseSched'},
            'calendar': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
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