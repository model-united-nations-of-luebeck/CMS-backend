# Generated by Django 3.1.14 on 2022-06-12 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_school_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='city',
        ),
    ]
