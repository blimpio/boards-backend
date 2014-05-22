# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Card.thumbnail_xs_path'
        db.alter_column('cards_card', 'thumbnail_xs_path', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Card.mime_type'
        db.alter_column('cards_card', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Card.thumbnail_sm_path'
        db.alter_column('cards_card', 'thumbnail_sm_path', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Card.content'
        db.alter_column('cards_card', 'content', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Card.origin_url'
        db.alter_column('cards_card', 'origin_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Card.thumbnail_lg_path'
        db.alter_column('cards_card', 'thumbnail_lg_path', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Card.thumbnail_md_path'
        db.alter_column('cards_card', 'thumbnail_md_path', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'Card.thumbnail_xs_path'
        db.alter_column('cards_card', 'thumbnail_xs_path', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Card.mime_type'
        db.alter_column('cards_card', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, default=''))

        # Changing field 'Card.thumbnail_sm_path'
        db.alter_column('cards_card', 'thumbnail_sm_path', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Card.content'
        db.alter_column('cards_card', 'content', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Card.origin_url'
        db.alter_column('cards_card', 'origin_url', self.gf('django.db.models.fields.URLField')(max_length=200, default=''))

        # Changing field 'Card.thumbnail_lg_path'
        db.alter_column('cards_card', 'thumbnail_lg_path', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Card.thumbnail_md_path'
        db.alter_column('cards_card', 'thumbnail_md_path', self.gf('django.db.models.fields.TextField')(default=''))

    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'disqus_shortname': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.EmailDomain']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_color': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'account_modified_by'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'blank': 'True', 'unique_with': '()', 'max_length': '50', 'populate_from': "'name'", 'unique': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'accounts.emaildomain': {
            'Meta': {'ordering': "('-date_modified', '-date_created')", 'object_name': 'EmailDomain'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
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
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('account',)", 'max_length': '50', 'populate_from': "'name'"}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_xs_path': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'cards.card': {
            'Meta': {'ordering': "['position']", 'object_name': 'Card'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.Card']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'+'", 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'data': ('jsonfield.fields.JSONField', [], {'blank': 'True', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'related_name': "'card_modified_by'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'blank': 'True', 'unique_with': "('board',)", 'max_length': '50', 'populate_from': "'name'"}),
            'stack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.Card']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumbnail_xs_path': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'unique': 'True'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'max_length': '15', 'default': "'127.0.0.1'", 'null': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'max_length': '36', 'default': "'312871be-f59d-4fd4-9f64-e946563ac6ca'", 'db_index': 'True', 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['cards']