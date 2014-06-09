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
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=('account',), populate_from='name', max_length=50)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], related_name='board_modified_by')),
            ('is_shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('color', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('thumbnail_xs_path', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('thumbnail_sm_path', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('thumbnail_md_path', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('thumbnail_lg_path', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('boards', ['Board'])

        # Adding model 'BoardCollaborator'
        db.create_table('boards_boardcollaborator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boards.Board'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['users.User'])),
            ('invited_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['invitations.InvitedUser'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], related_name='boardcollaborator_created_by')),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], related_name='boardcollaborator_modified_by')),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('boards', ['BoardCollaborator'])

        # Adding unique constraint on 'BoardCollaborator', fields ['board', 'user']
        db.create_unique('boards_boardcollaborator', ['board_id', 'user_id'])

        # Adding unique constraint on 'BoardCollaborator', fields ['board', 'invited_user']
        db.create_unique('boards_boardcollaborator', ['board_id', 'invited_user_id'])

        # Adding model 'BoardCollaboratorRequest'
        db.create_table('boards_boardcollaboratorrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['users.User'])),
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

        # Removing unique constraint on 'BoardCollaborator', fields ['board', 'invited_user']
        db.delete_unique('boards_boardcollaborator', ['board_id', 'invited_user_id'])

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
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'disqus_shortname': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['accounts.EmailDomain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_color': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'account_modified_by'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'blank': 'True', 'unique': 'True', 'unique_with': '()', 'populate_from': "'name'", 'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'accounts.emaildomain': {
            'Meta': {'object_name': 'EmailDomain', 'ordering': "('-date_modified', '-date_created')"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'boards.board': {
            'Meta': {'object_name': 'Board'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'color': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'board_modified_by'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('account',)", 'populate_from': "'name'", 'max_length': '50'}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_xs_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'})
        },
        'boards.boardcollaborator': {
            'Meta': {'object_name': 'BoardCollaborator', 'unique_together': "(('board', 'user'), ('board', 'invited_user'))"},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'boardcollaborator_created_by'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['invitations.InvitedUser']"}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'boardcollaborator_modified_by'"}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['users.User']"})
        },
        'boards.boardcollaboratorrequest': {
            'Meta': {'object_name': 'BoardCollaboratorRequest', 'unique_together': "(('email', 'board'), ('user', 'board'))"},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['users.User']"})
        },
        'invitations.inviteduser': {
            'Meta': {'object_name': 'InvitedUser', 'unique_together': "(('account', 'email'),)"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'board_collaborator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['boards.BoardCollaborator']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'inviteduser_created_by'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['users.User']"})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'default': "'127.0.0.1'", 'null': 'True', 'max_length': '15'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'default': "'9eba06fe-0537-4d90-9092-0da1f0616ab9'", 'unique': 'True', 'db_index': 'True', 'max_length': '36'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['boards']