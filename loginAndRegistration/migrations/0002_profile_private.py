# Generated by Django 2.2.25 on 2022-01-08 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginAndRegistration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]