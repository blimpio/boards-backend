# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.date_joined'
        db.delete_column('users_user', 'date_joined')

        # Adding field 'User.date_created'
        db.add_column('users_user', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'User.date_modified'
        db.add_column('users_user', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name('users_user_user_permissions'))

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name('users_user_groups'))


    def backwards(self, orm):
        # Adding field 'User.date_joined'
        db.add_column('users_user', 'date_joined',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'User.date_created'
        db.delete_column('users_user', 'date_created')

        # Deleting field 'User.date_modified'
        db.delete_column('users_user', 'date_modified')

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name('users_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['users.user'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name('users_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['users.user'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])


    models = {
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
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
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'3ad410a1-f356-4524-ab5d-04901f6b3154'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['users']