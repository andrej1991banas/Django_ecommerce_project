# Generated by Django 4.2.20 on 2025-04-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_rename_adress1_member_address1'),
        ('order', '0008_remove_order_user_order_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='member',
        ),
        migrations.AddField(
            model_name='order',
            name='member',
            field=models.ManyToManyField(blank=True, null=True, related_name='orders', to='member.member'),
        ),
    ]
