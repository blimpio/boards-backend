# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SignupRequest'
        db.create_table('invitations_signuprequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('invitations', ['SignupRequest'])

        # Adding model 'InvitedUser'
        db.create_table('invitations_inviteduser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['users.User'], null=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inviteduser_created_by', to=orm['users.User'])),
        ))
        db.send_create_signal('invitations', ['InvitedUser'])


    def backwards(self, orm):
        # Deleting model 'SignupRequest'
        db.delete_table('invitations_signuprequest')

        # Deleting model 'InvitedUser'
        db.delete_table('invitations_inviteduser')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['accounts.EmailDomain']", 'symmetrical': 'False', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'accounts.emaildomain': {
            'Meta': {'object_name': 'EmailDomain'},
            'domain_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'invitations.inviteduser': {
            'Meta': {'object_name': 'InvitedUser'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviteduser_created_by'", 'to': "orm['users.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['users.User']", 'null': 'True'})
        },
        'invitations.signuprequest': {
            'Meta': {'object_name': 'SignupRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'aim_username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '255'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'gtalk_username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'default': "'127.0.0.1'", 'null': 'True', 'max_length': '15'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '40'}),
            'skype_username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '36'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'windows_live_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['invitations']