# Generated by Django 4.2.4 on 2023-08-16 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_name', models.CharField(max_length=255)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.jobfield')),
            ],
        ),
    ]
