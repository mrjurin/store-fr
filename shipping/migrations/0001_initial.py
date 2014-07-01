# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('address', '0007_auto__chg_field_useraddress_postcode'),
    )
    def forwards(self, orm):
        # Adding model 'OrderAndItemCharges'
        db.create_table(u'shipping_orderanditemcharges', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price_per_order', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=12, decimal_places=2)),
            ('price_per_item', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=12, decimal_places=2)),
            ('free_shipping_threshold', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'shipping', ['OrderAndItemCharges'])

        # Adding M2M table for field countries on 'OrderAndItemCharges'
        m2m_table_name = db.shorten_name(u'shipping_orderanditemcharges_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('orderanditemcharges', models.ForeignKey(orm[u'shipping.orderanditemcharges'], null=False)),
            ('country', models.ForeignKey(orm[u'address.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['orderanditemcharges_id', 'country_id'])

        # Adding model 'WeightBased'
        db.create_table(u'shipping_weightbased', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('upper_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2)),
            ('default_weight', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'shipping', ['WeightBased'])

        # Adding M2M table for field countries on 'WeightBased'
        m2m_table_name = db.shorten_name(u'shipping_weightbased_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('weightbased', models.ForeignKey(orm[u'shipping.weightbased'], null=False)),
            ('country', models.ForeignKey(orm[u'address.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['weightbased_id', 'country_id'])

        # Adding model 'WeightBand'
        db.create_table(u'shipping_weightband', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bands', to=orm['shipping.WeightBased'])),
            ('upper_limit', self.gf('django.db.models.fields.FloatField')()),
            ('charge', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'shipping', ['WeightBand'])


    def backwards(self, orm):
        # Deleting model 'OrderAndItemCharges'
        db.delete_table(u'shipping_orderanditemcharges')

        # Removing M2M table for field countries on 'OrderAndItemCharges'
        db.delete_table(db.shorten_name(u'shipping_orderanditemcharges_countries'))

        # Deleting model 'WeightBased'
        db.delete_table(u'shipping_weightbased')

        # Removing M2M table for field countries on 'WeightBased'
        db.delete_table(db.shorten_name(u'shipping_weightbased_countries'))

        # Deleting model 'WeightBand'
        db.delete_table(u'shipping_weightband')


    models = {
        u'address.country': {
            'Meta': {'ordering': "('-display_order', 'name')", 'object_name': 'Country'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'is_shipping_country': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'iso_3166_1_a2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso_3166_1_a3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_index': 'True'}),
            'iso_3166_1_numeric': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'shipping.orderanditemcharges': {
            'Meta': {'object_name': 'OrderAndItemCharges'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['address.Country']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'free_shipping_threshold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'price_per_item': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'}),
            'price_per_order': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        u'shipping.weightband': {
            'Meta': {'ordering': "['upper_limit']", 'object_name': 'WeightBand'},
            'charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bands'", 'to': u"orm['shipping.WeightBased']"}),
            'upper_limit': ('django.db.models.fields.FloatField', [], {})
        },
        u'shipping.weightbased': {
            'Meta': {'object_name': 'WeightBased'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['address.Country']", 'null': 'True', 'blank': 'True'}),
            'default_weight': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'upper_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2'})
        }
    }

    complete_apps = ['shipping']
