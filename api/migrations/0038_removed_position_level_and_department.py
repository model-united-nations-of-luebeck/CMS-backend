# Generated by Django 3.2.25 on 2024-06-09 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_made_fields_optional'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='executive',
            name='department_name',
        ),
        migrations.RemoveField(
            model_name='executive',
            name='position_level',
        ),
        migrations.RemoveField(
            model_name='studentofficer',
            name='position_level',
        ),
    ]