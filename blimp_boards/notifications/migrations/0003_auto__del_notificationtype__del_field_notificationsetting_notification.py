# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.delete_unique('notifications_notificationsetting', ['user_id', 'notification_type_id', 'medium'])

        # Deleting model 'NotificationType'
        db.delete_table('notifications_notificationtype')

        # Deleting field 'NotificationSetting.notification_type'
        db.delete_column('notifications_notificationsetting', 'notification_type_id')

        # Adding unique constraint on 'NotificationSetting', fields ['user', 'medium']
        db.create_unique('notifications_notificationsetting', ['user_id', 'medium'])


    def backwards(self, orm):
        # Removing unique constraint on 'NotificationSetting', fields ['user', 'medium']
        db.delete_unique('notifications_notificationsetting', ['user_id', 'medium'])

        # Adding model 'NotificationType'
        db.create_table('notifications_notificationtype', (
            ('display', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('notifications', ['NotificationType'])


        # User chose to not deal with backwards NULL issues for 'NotificationSetting.notification_type'
        raise RuntimeError("Cannot reverse this migration. 'NotificationSetting.notification_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NotificationSetting.notification_type'
        db.add_column('notifications_notificationsetting', 'notification_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.NotificationType']),
                      keep_default=False)

        # Adding unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.create_unique('notifications_notificationsetting', ['user_id', 'notification_type_id', 'medium'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.notification': {
            'Meta': {'object_name': 'Notification', 'ordering': "('-date_modified', '-date_created')"},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_action_object'", 'null': 'True', 'blank': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_actor'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'info'"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['users.User']"}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_target'", 'null': 'True', 'blank': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.notificationsetting': {
            'Meta': {'object_name': 'NotificationSetting', 'unique_together': "(('user', 'medium'),)"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'send': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'default': "'127.0.0.1'", 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'default': "'0701a237-afac-4605-a3a5-9849935ebab9'", 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['notifications']