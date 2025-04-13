# Generated by Django 4.2.20 on 2025-04-07 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_product_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0006_alter_order_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='member',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='x', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(default='x', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(default='x', max_length=1500),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
            ],
        ),
    ]
