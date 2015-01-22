# -*- coding: utf-8 -*-
from django.db import models

from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseSched'
        db.create_table(u'courseSched_coursesched', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Calendar'])),
        ))
        db.send_create_signal(u'courseSched', ['CourseSched'])


    def backwards(self, orm):
        # Deleting model 'CourseSched'
        db.delete_table(u'courseSched_coursesched')


    models = {
        u'courseSched.coursesched': {
            'Meta': {'object_name': 'CourseSched'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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