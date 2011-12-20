# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Office'
        db.create_table('main_app_office', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('adress', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('main_app', ['Office'])

        # Adding model 'fieldUserProfile'
        db.create_table('main_app_fielduserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('last_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('last_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('imei_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('phone_numer', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('home_adress', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.Office'])),
        ))
        db.send_create_signal('main_app', ['fieldUserProfile'])

        # Adding model 'Task'
        db.create_table('main_app_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fieldUserProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.fieldUserProfile'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('assign_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('finish_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('supervisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main_app', ['Task'])


    def backwards(self, orm):
        
        # Deleting model 'Office'
        db.delete_table('main_app_office')

        # Deleting model 'fieldUserProfile'
        db.delete_table('main_app_fielduserprofile')

        # Deleting model 'Task'
        db.delete_table('main_app_task')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main_app.fielduserprofile': {
            'Meta': {'object_name': 'fieldUserProfile'},
            'home_adress': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'last_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'last_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main_app.Office']"}),
            'phone_numer': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'main_app.office': {
            'Meta': {'object_name': 'Office'},
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'main_app.task': {
            'Meta': {'object_name': 'Task'},
            'assign_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fieldUserProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main_app.fieldUserProfile']"}),
            'finish_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['main_app']
