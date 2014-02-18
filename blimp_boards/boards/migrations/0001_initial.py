# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table('boards_board', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('is_shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thumbnail_sm_path', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thumbnail_md_path', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thumbnail_lg_path', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('boards', ['Board'])

        # Adding model 'BoardCollaborator'
        db.create_table('boards_boardcollaborator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boards.Board'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['users.User'], null=True)),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('boards', ['BoardCollaborator'])

        # Adding unique constraint on 'BoardCollaborator', fields ['board', 'user']
        db.create_unique('boards_boardcollaborator', ['board_id', 'user_id'])

        # Adding model 'BoardCollaboratorRequest'
        db.create_table('boards_boardcollaboratorrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['users.User'], null=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boards.Board'])),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('boards', ['BoardCollaboratorRequest'])

        # Adding unique constraint on 'BoardCollaboratorRequest', fields ['email', 'board']
        db.create_unique('boards_boardcollaboratorrequest', ['email', 'board_id'])

        # Adding unique constraint on 'BoardCollaboratorRequest', fields ['user', 'board']
        db.create_unique('boards_boardcollaboratorrequest', ['user_id', 'board_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BoardCollaboratorRequest', fields ['user', 'board']
        db.delete_unique('boards_boardcollaboratorrequest', ['user_id', 'board_id'])

        # Removing unique constraint on 'BoardCollaboratorRequest', fields ['email', 'board']
        db.delete_unique('boards_boardcollaboratorrequest', ['email', 'board_id'])

        # Removing unique constraint on 'BoardCollaborator', fields ['board', 'user']
        db.delete_unique('boards_boardcollaborator', ['board_id', 'user_id'])

        # Deleting model 'Board'
        db.delete_table('boards_board')

        # Deleting model 'BoardCollaborator'
        db.delete_table('boards_boardcollaborator')

        # Deleting model 'BoardCollaboratorRequest'
        db.delete_table('boards_boardcollaboratorrequest')


    models = {
        'accounts.account': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['accounts.EmailDomain']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'accounts.emaildomain': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'EmailDomain'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'boards.board': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'Board'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'boards.boardcollaborator': {
            'Meta': {'unique_together': "(('board', 'user'),)", 'object_name': 'BoardCollaborator'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['users.User']", 'null': 'True'})
        },
        'boards.boardcollaboratorrequest': {
            'Meta': {'unique_together': "(('email', 'board'), ('user', 'board'))", 'object_name': 'BoardCollaboratorRequest'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['users.User']", 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'aim_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'unique': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'gtalk_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'skype_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'1107edd0-682e-43ee-ad43-a4cae268b8c3'", 'max_length': '36', 'unique': 'True', 'db_index': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'windows_live_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['boards']