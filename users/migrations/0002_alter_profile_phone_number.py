# Generated by Django 3.2.6 on 2021-09-03 08:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.PositiveBigIntegerField(default=1, unique=True, validators=[django.core.validators.RegexValidator('^(\\+98|0)?9\\d{9}$', message='wrong number')], verbose_name='phone number'),
            preserve_default=False,
        ),
    ]