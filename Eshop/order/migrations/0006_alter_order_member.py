# Generated by Django 4.2.20 on 2025-04-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_rename_adress1_member_address1'),
        ('order', '0005_rename_address1_shippingaddress_shipping_address1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='member',
            field=models.ManyToManyField(blank=True, related_name='orders', to='member.member'),
        ),
    ]
