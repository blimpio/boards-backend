# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InvitedUser.role'
        db.delete_column('invitations_inviteduser', 'role')

        # Adding M2M table for field board_collaborators on 'InvitedUser'
        m2m_table_name = db.shorten_name('invitations_inviteduser_board_collaborators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('inviteduser', models.ForeignKey(orm['invitations.inviteduser'], null=False)),
            ('boardcollaborator', models.ForeignKey(orm['boards.boardcollaborator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['inviteduser_id', 'boardcollaborator_id'])


    def backwards(self, orm):
        # Adding field 'InvitedUser.role'
        db.add_column('invitations_inviteduser', 'role',
                      self.gf('django.db.models.fields.CharField')(default='read', max_length=25),
                      keep_default=False)

        # Removing M2M table for field board_collaborators on 'InvitedUser'
        db.delete_table(db.shorten_name('invitations_inviteduser_board_collaborators'))


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'null': 'True', 'to': "orm['accounts.EmailDomain']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'accounts.emaildomain': {
            'Meta': {'object_name': 'EmailDomain'},
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'boards.board': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'Board'},
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
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'BoardCollaborator'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['invitations.InvitedUser']", 'blank': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['users.User']", 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'invitations.inviteduser': {
            'Meta': {'object_name': 'InvitedUser'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'board_collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'null': 'True', 'to': "orm['boards.BoardCollaborator']", 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviteduser_created_by'", 'to': "orm['users.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['users.User']", 'blank': 'True'})
        },
        'invitations.signuprequest': {
            'Meta': {'object_name': 'SignupRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'gtalk_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'skype_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'token_version': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'windows_live_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['invitations']