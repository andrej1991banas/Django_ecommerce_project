# Generated by Django 4.2.20 on 2025-04-07 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_rename_location_member_adress1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='adress1',
            new_name='address1',
        ),
    ]
