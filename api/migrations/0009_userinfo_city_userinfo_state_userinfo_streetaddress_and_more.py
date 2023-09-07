# Generated by Django 4.2.4 on 2023-08-29 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_userinfo_jobfield_alter_userinfo_jobtitle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='streetaddress',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='zipcode',
            field=models.IntegerField(null=True),
        ),
    ]