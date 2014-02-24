# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.slug'
        db.add_column('cards_card', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=50, default='card-1393273953'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.slug'
        db.delete_column('cards_card', 'slug')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account', 'ordering': "('-date_modified', '-date_created')"},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['accounts.EmailDomain']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'accounts.emaildomain': {
            'Meta': {'object_name': 'EmailDomain', 'ordering': "('-date_modified', '-date_created')"},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'boards.board': {
            'Meta': {'object_name': 'Board', 'ordering': "('-date_modified', '-date_created')"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'cards.card': {
            'Meta': {'object_name': 'Card', 'ordering': "('-date_modified', '-date_created')"},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['boards.Board']"}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['cards.Card']", 'blank': 'True', 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file_extension': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumbnail_lg_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_md_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumbnail_sm_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_path': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'default': "'127.0.0.1'", 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'default': "'82c950a9-f09d-470b-8416-922b013a30f0'", 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['cards']