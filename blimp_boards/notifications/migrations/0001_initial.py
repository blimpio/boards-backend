# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotificationType'
        db.create_table('notifications_notificationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('notifications', ['NotificationType'])

        # Adding model 'NotificationSetting'
        db.create_table('notifications_notificationsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('notification_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.NotificationType'])),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('send', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('notifications', ['NotificationSetting'])

        # Adding unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.create_unique('notifications_notificationsetting', ['user_id', 'notification_type_id', 'medium'])

        # Adding model 'Notification'
        db.create_table('notifications_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(default='info', max_length=20)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['users.User'])),
            ('unread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('actor_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_actor', to=orm['contenttypes.ContentType'])),
            ('actor_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_target', to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('target_object_id', self.gf('django.db.models.fields.CharField')(null=True, max_length=255, blank=True)),
            ('action_object_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_action_object', to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('action_object_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['Notification'])


    def backwards(self, orm):
        # Removing unique constraint on 'NotificationSetting', fields ['user', 'notification_type', 'medium']
        db.delete_unique('notifications_notificationsetting', ['user_id', 'notification_type_id', 'medium'])

        # Deleting model 'NotificationType'
        db.delete_table('notifications_notificationtype')

        # Deleting model 'NotificationSetting'
        db.delete_table('notifications_notificationsetting')

        # Deleting model 'Notification'
        db.delete_table('notifications_notification')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.notification': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'Notification'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_action_object'", 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
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
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_target'", 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.notificationsetting': {
            'Meta': {'unique_together': "(('user', 'notification_type', 'medium'),)", 'object_name': 'NotificationSetting'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.NotificationType']"}),
            'send': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
        },
        'notifications.notificationtype': {
            'Meta': {'object_name': 'NotificationType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'d6b25fde-8562-42cc-8d58-c1ac2888270c'", 'max_length': '36', 'unique': 'True', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['notifications']