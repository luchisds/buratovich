# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-24 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20170120_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='CtaCteKilos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('name', models.CharField(max_length=150, verbose_name='Raz\xf3n Social')),
                ('indicator', models.CharField(max_length=1, verbose_name='Indicador')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('species_description', models.CharField(max_length=50, verbose_name='Especie y Cosecha')),
                ('field', models.IntegerField(verbose_name='Codigo de Campo')),
                ('field_description', models.CharField(max_length=100, verbose_name='Nombre de Campo')),
                ('date', models.DateField(null=True, verbose_name='Fecha')),
                ('voucher', models.CharField(max_length=16, verbose_name='Comprobante')),
                ('gross_kg', models.IntegerField(verbose_name='Kilos Brutos')),
                ('humidity_percentage', models.FloatField(verbose_name='Humedad (%)')),
                ('humidity_reduction', models.FloatField(verbose_name='Merma de Humedad')),
                ('humidity_kg', models.IntegerField(verbose_name='Kilos de Humedad')),
                ('shaking_reduction', models.FloatField(verbose_name='Merma de Zarandeo')),
                ('shaking_kg', models.IntegerField(verbose_name='Kilos de Zarandeo')),
                ('volatile_reduction', models.FloatField(verbose_name='Merma Volatil')),
                ('volatile_kg', models.IntegerField(verbose_name='Kilos Volatil')),
                ('price_per_yard', models.FloatField(verbose_name='Precio por Quintal')),
                ('driver_code', models.IntegerField(verbose_name='Chofer')),
                ('driver_name', models.CharField(max_length=150, verbose_name='Nombre del Chofer')),
                ('factor', models.FloatField(verbose_name='Factor')),
                ('grade', models.IntegerField(verbose_name='Grado')),
                ('gluten', models.IntegerField(verbose_name='Gluten')),
                ('number_1116A', models.IntegerField(verbose_name='Numero 1116A')),
                ('km', models.IntegerField(verbose_name='Kilometros')),
                ('charge_carry', models.CharField(max_length=2, verbose_name='Cobra Acarreo')),
                ('external_voucher_code', models.CharField(max_length=2, verbose_name='Codigo de Comprobante Externo')),
                ('external_voucher_branch', models.IntegerField(verbose_name='Sucursal Comprobante Externo')),
                ('external_voucher_number', models.IntegerField(verbose_name='Numero Comprobante Externo')),
                ('aeration_reduction', models.FloatField(verbose_name='Merma de Aireacion')),
                ('aeration_kg', models.IntegerField(verbose_name='Kilos de Aireacion')),
                ('quality_reduction', models.FloatField(verbose_name='Merma de Calidad')),
                ('quality_kg', models.IntegerField(verbose_name='Kilos de Calidad')),
                ('zone', models.CharField(max_length=2, verbose_name='Zona')),
                ('zone_description', models.CharField(max_length=80, verbose_name='Descripcion de Zona')),
                ('plant_code', models.IntegerField(verbose_name='Planta')),
                ('service_billing_code', models.CharField(max_length=2, verbose_name='Codigo Factura de Servicios')),
                ('service_billing_branch', models.IntegerField(verbose_name='Sucursal Factura de Servicios')),
                ('service_billing_number', models.IntegerField(verbose_name='Numero Factura de Servicios')),
                ('service_billing_date', models.DateField(null=True, verbose_name='Fecha Factura de Servicios')),
                ('service_billing', models.CharField(max_length=50, verbose_name='Factura de Servicios')),
                ('carrier_code', models.IntegerField(verbose_name='Empresa de Transporte')),
                ('carrier_name', models.CharField(max_length=150, verbose_name='Nombre de Empresa de Transporte')),
                ('exclude_charge_expenses', models.CharField(max_length=2, verbose_name='Excluye Cobro de Gastos')),
                ('to_date', models.DateField(null=True, verbose_name='Fecha Entrega Hasta')),
                ('observations', models.CharField(max_length=300, verbose_name='Observaciones')),
                ('follow_destination', models.CharField(max_length=2, verbose_name='Sigue a Destino')),
                ('destination_code', models.CharField(max_length=5, verbose_name='Codigo de Destino')),
                ('net_weight', models.IntegerField(verbose_name='Peso Neto')),
                ('tare', models.IntegerField(verbose_name='Tara')),
                ('gross_weight_recognized', models.IntegerField(verbose_name='Peso Bruto Reconocido')),
                ('plant_description', models.CharField(max_length=80, verbose_name='Descripcion de Planta')),
                ('gross_kg_var', models.IntegerField(verbose_name='Kilos Brutos (otro)')),
                ('gross_kg_2', models.IntegerField(verbose_name='Kilos Brutos 2')),
                ('blank_1', models.CharField(max_length=1, verbose_name='Blanco 1')),
                ('blank_2', models.CharField(max_length=1, verbose_name='Blanco 1')),
                ('blank_3', models.CharField(max_length=1, verbose_name='Blanco 1')),
                ('blank_4', models.CharField(max_length=1, verbose_name='Blanco 4')),
                ('allotment', models.CharField(max_length=10, verbose_name='Lote')),
                ('allotment_description', models.CharField(max_length=100, verbose_name='Descripcion Lote')),
                ('blank_5', models.IntegerField(max_length=1, verbose_name='Blanco 5')),
                ('blank_6', models.CharField(max_length=2, verbose_name='Blanco 6')),
                ('kg_cnv', models.IntegerField(verbose_name='Kilos Conf. de Venta')),
                ('kg_cnv_2', models.IntegerField(verbose_name='Kilos Conf. de Venta 2')),
                ('kg_cnv_3', models.IntegerField(verbose_name='Kilos Conf. de Venta 3')),
                ('blank_7', models.CharField(max_length=2, verbose_name='Blanco 7')),
                ('blank_8', models.CharField(max_length=2, verbose_name='Blanco 8')),
                ('blank_9', models.CharField(max_length=2, verbose_name='Blanco 9')),
                ('blank_10', models.CharField(max_length=2, verbose_name='Blanco 10')),
                ('gross_kg_3', models.IntegerField(verbose_name='Kilos Brutos 3')),
                ('unknown_1', models.IntegerField(verbose_name='Desconocido 1')),
                ('unknown_2', models.IntegerField(verbose_name='Desconocido 2')),
                ('gross_kg_4', models.IntegerField(verbose_name='Kilos Brutos 4')),
                ('rate', models.FloatField(verbose_name='Tarifa')),
                ('net_weight_2', models.IntegerField(verbose_name='Peso Neto 2')),
                ('humidity_kg_2', models.IntegerField(verbose_name='Kilos de Humedad 2')),
                ('blank_11', models.CharField(max_length=1, verbose_name='Blanco 11')),
                ('blank_12', models.CharField(max_length=1, verbose_name='Blanco 12')),
                ('blank_13', models.CharField(max_length=1, verbose_name='Blanco 13')),
                ('blank_14', models.CharField(max_length=2, verbose_name='Blanco 14')),
                ('ctg', models.IntegerField(verbose_name='CTG')),
            ],
        ),
    ]
