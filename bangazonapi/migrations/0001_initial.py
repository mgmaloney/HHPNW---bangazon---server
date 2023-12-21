# Generated by Django 5.0 on 2023-12-21 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=10)),
                ('uid', models.CharField(max_length=50)),
                ('is_seller', models.BooleanField(default=False)),
            ],
        ),
    ]