# Generated by Django 2.2.6 on 2019-10-19 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_participant_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='lunches',
            field=models.ManyToManyField(to='api.Lunch'),
        ),
        migrations.AddField(
            model_name='plenary',
            name='lunches',
            field=models.ManyToManyField(to='api.Lunch'),
        ),
    ]
