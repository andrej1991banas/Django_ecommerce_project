# Generated by Django 4.2.20 on 2025-05-02 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0021_order_date_shipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to=settings.AUTH_USER_MODEL),
        ),
    ]
