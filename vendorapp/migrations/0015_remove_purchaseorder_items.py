# Generated by Django 4.2.7 on 2023-11-29 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0014_purchaseorder_items_purchaseorder_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='items',
        ),
    ]
