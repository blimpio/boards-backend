# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailDomain'
        db.create_table('accounts_emaildomain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('domain_name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('accounts', ['EmailDomain'])

        # Adding model 'Account'
        db.create_table('accounts_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(blank=True, max_length=50, populate_from='name', unique=True, unique_with=())),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('allow_signup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('logo_color', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('disqus_shortname', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='account_modified_by', to=orm['users.User'])),
        ))
        db.send_create_signal('accounts', ['Account'])

        # Adding M2M table for field email_domains on 'Account'
        m2m_table_name = db.shorten_name('accounts_account_email_domains')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['accounts.account'], null=False)),
            ('emaildomain', models.ForeignKey(orm['accounts.emaildomain'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'emaildomain_id'])

        # Adding model 'AccountCollaborator'
        db.create_table('accounts_accountcollaborator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('is_owner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['AccountCollaborator'])

        # Adding unique constraint on 'AccountCollaborator', fields ['account', 'user']
        db.create_unique('accounts_accountcollaborator', ['account_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'AccountCollaborator', fields ['account', 'user']
        db.delete_unique('accounts_accountcollaborator', ['account_id', 'user_id'])

        # Deleting model 'EmailDomain'
        db.delete_table('accounts_emaildomain')

        # Deleting model 'Account'
        db.delete_table('accounts_account')

        # Removing M2M table for field email_domains on 'Account'
        db.delete_table(db.shorten_name('accounts_account_email_domains'))

        # Deleting model 'AccountCollaborator'
        db.delete_table('accounts_accountcollaborator')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'allow_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'disqus_shortname': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'email_domains': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'symmetrical': 'False', 'to': "orm['accounts.EmailDomain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_color': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_modified_by'", 'to': "orm['users.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'blank': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique': 'True', 'unique_with': '()'}),
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
            'Meta': {'object_name': 'EmailDomain', 'ordering': "('-date_modified', '-date_created')"},
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
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'gravatar_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'null': 'True', 'max_length': '15', 'default': "'127.0.0.1'"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'UTC'"}),
            'token_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'unique': 'True', 'default': "'58594147-1611-40cd-a331-88cdee1db8f1'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        }
    }

    complete_apps = ['accounts']