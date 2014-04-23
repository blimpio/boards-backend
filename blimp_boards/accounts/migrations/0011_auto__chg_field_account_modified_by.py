# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Account.modified_by'
        db.alter_column('accounts_account', 'modified_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], default=1))

    def backwards(self, orm):

        # Changing field 'Account.modified_by'
        db.alter_column('accounts_account', 'modified_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.User']))

    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'disqus_shortname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.EmailDomain']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_color': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'account_modified_by'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'", 'blank': 'True', 'unique': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'accounts.accountcollaborator': {
            'Meta': {'object_name': 'AccountCollaborator', 'unique_together': "(('account', 'user'),)"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
        },
        'accounts.emaildomain': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'EmailDomain'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15', 'default': "'127.0.0.1'"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True', 'unique': 'True', 'default': "'b42042dd-867f-42fa-9cf1-90bb55a1db65'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['accounts']