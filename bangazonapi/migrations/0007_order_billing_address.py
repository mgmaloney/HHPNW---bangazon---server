# Generated by Django 5.0 on 2023-12-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0006_alter_order_date_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.CharField(default='', max_length=250),
        ),
    ]
