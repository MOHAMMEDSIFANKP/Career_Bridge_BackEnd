# Generated by Django 4.2.4 on 2023-08-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_google',
            field=models.BooleanField(default=False),
        ),
    ]
