# Generated by Django 2.2.7 on 2019-11-13 10:00

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_order_mobail_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
