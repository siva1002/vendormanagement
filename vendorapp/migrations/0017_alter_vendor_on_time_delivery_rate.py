# Generated by Django 4.2.7 on 2023-11-29 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0016_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
    ]
