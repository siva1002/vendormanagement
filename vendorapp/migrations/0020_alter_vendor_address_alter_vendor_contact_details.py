# Generated by Django 4.2.7 on 2023-11-29 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0019_alter_vendor_address_alter_vendor_contact_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.TextField(default='address', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='contact_details',
            field=models.TextField(default='contact_details', null=True),
        ),
    ]
