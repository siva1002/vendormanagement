# Generated by Django 4.2.7 on 2023-11-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0022_rename_orderdate_purchaseorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
