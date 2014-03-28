# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'NotificationSetting', fields ['user', 'medium']
        db.delete_unique('notifications_notificationsetting', ['user_id', 'medium'])

        # Adding field 'NotificationSetting.notification_type'
        db.add_column('notifications_notificationsetting', 'notification_type',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Adding unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.create_unique('notifications_notificationsetting', ['user_id', 'notification_type', 'medium'])


    def backwards(self, orm):
        # Removing unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.delete_unique('notifications_notificationsetting', ['user_id', 'notification_type', 'medium'])

        # Deleting field 'NotificationSetting.notification_type'
        db.delete_column('notifications_notificationsetting', 'notification_type')

        # Adding unique constraint on 'NotificationSetting', fields ['user', 'medium']
        db.create_unique('notifications_notificationsetting', ['user_id', 'medium'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.notification': {
            'Meta': {'object_name': 'Notification', 'ordering': "('-date_modified', '-date_created')"},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'notify_action_object'", 'to': "orm['contenttypes.ContentType']", 'blank': 'True'}),
            'action_object_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_actor'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'info'", 'max_length': '20'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['users.User']"}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'notify_target'", 'to': "orm['contenttypes.ContentType']", 'blank': 'True'}),
            'target_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.notificationsetting': {
            'Meta': {'unique_together': "(('user', 'notification_type', 'medium'),)", 'object_name': 'NotificationSetting'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'send': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'default': "'127.0.0.1'", 'max_length': '15', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'252e7916-b3a5-4f18-a011-95ec69e79c58'", 'max_length': '36', 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['notifications']