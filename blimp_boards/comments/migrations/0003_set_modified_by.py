# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for comment in orm['comments.Comment'].objects.all():
            comment.modified_by = comment.created_by
            comment.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_modified_by'", 'blank': 'True', 'null': 'True', 'to': "orm['users.User']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15', 'default': "'127.0.0.1'"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '36', 'default': "'3060ded1-37d3-4447-8729-afbfa386099a'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['comments']
    symmetrical = True
