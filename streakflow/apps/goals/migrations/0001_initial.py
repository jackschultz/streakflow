# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Goal'
        db.create_table(u'goals_goal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goals', to=orm['members.Member'])),
            ('goal_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('num_per_frame', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('time_frame_len', self.gf('django.db.models.fields.CharField')(default='d', max_length=1)),
            ('activated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 19, 0, 0), blank=True)),
        ))
        db.send_create_signal(u'goals', ['Goal'])

        # Adding model 'TimeFrame'
        db.create_table(u'goals_timeframe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_per_frame', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('begin_time', self.gf('django.db.models.fields.DateTimeField')(default=None, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=None, blank=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='time_frames', to=orm['goals.Goal'])),
        ))
        db.send_create_signal(u'goals', ['TimeFrame'])

        # Adding model 'Objective'
        db.create_table(u'goals_objective', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_completed', self.gf('django.db.models.fields.DateTimeField')(default=None, blank=True)),
            ('time_frame', self.gf('django.db.models.fields.related.ForeignKey')(related_name='objectives', to=orm['goals.TimeFrame'])),
        ))
        db.send_create_signal(u'goals', ['Objective'])


    def backwards(self, orm):
        # Deleting model 'Goal'
        db.delete_table(u'goals_goal')

        # Deleting model 'TimeFrame'
        db.delete_table(u'goals_timeframe')

        # Deleting model 'Objective'
        db.delete_table(u'goals_objective')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'goals.goal': {
            'Meta': {'object_name': 'Goal'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': u"orm['members.Member']"}),
            'num_per_frame': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 19, 0, 0)', 'blank': 'True'}),
            'time_frame_len': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'})
        },
        u'goals.objective': {
            'Meta': {'object_name': 'Objective'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_completed': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'blank': 'True'}),
            'time_frame': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objectives'", 'to': u"orm['goals.TimeFrame']"})
        },
        u'goals.timeframe': {
            'Meta': {'object_name': 'TimeFrame'},
            'begin_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'blank': 'True'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'time_frames'", 'to': u"orm['goals.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_per_frame': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'members.member': {
            'Meta': {'object_name': 'Member'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['goals']