# Generated by Django 4.1 on 2024-08-24 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_flag', models.BooleanField()),
                ('code', models.CharField(max_length=10, unique=True)),
                ('default_record', models.BooleanField()),
                ('description', models.CharField(max_length=256)),
                ('integral', models.BooleanField()),
                ('name', models.CharField(max_length=30, unique=True)),
                ('read_only', models.BooleanField()),
            ],
            options={
                'db_table': 'uom',
            },
        ),
        migrations.CreateModel(
            name='UOMType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'db_table': 'uomtype',
            },
        ),
        migrations.CreateModel(
            name='UOMConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('factor', models.FloatField(blank=True, null=True)),
                ('multiply', models.FloatField(blank=True, null=True)),
                ('from_uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_uom_conversions', to='uom.uom')),
                ('to_uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_uom_conversions', to='uom.uom')),
            ],
            options={
                'db_table': 'uomconversion',
            },
        ),
        migrations.AddField(
            model_name='uom',
            name='uom_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uom.uomtype'),
        ),
    ]
