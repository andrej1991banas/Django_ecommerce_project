# Generated by Django 4.2.20 on 2025-04-07 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_rename_adress1_member_address1'),
        ('order', '0007_remove_order_member_remove_order_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='member.member'),
        ),
    ]
