# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.twitter_username'
        db.delete_column('users_user', 'twitter_username')

        # Deleting field 'User.skype_username'
        db.delete_column('users_user', 'skype_username')

        # Deleting field 'User.facebook_id'
        db.delete_column('users_user', 'facebook_id')

        # Deleting field 'User.windows_live_id'
        db.delete_column('users_user', 'windows_live_id')

        # Deleting field 'User.aim_username'
        db.delete_column('users_user', 'aim_username')

        # Deleting field 'User.gtalk_username'
        db.delete_column('users_user', 'gtalk_username')


    def backwards(self, orm):
        # Adding field 'User.twitter_username'
        db.add_column('users_user', 'twitter_username',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)

        # Adding field 'User.skype_username'
        db.add_column('users_user', 'skype_username',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)

        # Adding field 'User.facebook_id'
        db.add_column('users_user', 'facebook_id',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)

        # Adding field 'User.windows_live_id'
        db.add_column('users_user', 'windows_live_id',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)

        # Adding field 'User.aim_username'
        db.add_column('users_user', 'aim_username',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)

        # Adding field 'User.gtalk_username'
        db.add_column('users_user', 'gtalk_username',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'default': "'127.0.0.1'", 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '36', 'default': "'0b30221a-0590-4fae-a342-9e607ad33eaa'"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['users']