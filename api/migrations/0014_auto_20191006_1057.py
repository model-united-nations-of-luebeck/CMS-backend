# Generated by Django 2.2.6 on 2019-10-06 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20191006_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='plenary',
            name='location',
            field=models.ForeignKey(blank=True, help_text='Select a conference venue where this plenary takes place', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Location'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='How is the event called', max_length=100, verbose_name='Event name')),
                ('day', models.DateField(help_text='On which day does it take place?', verbose_name='Day')),
                ('start_time', models.TimeField(help_text='Specify the beginning time', verbose_name='Start Time')),
                ('end_time', models.TimeField(blank=True, help_text="Specify the end time, none if it's open ended", verbose_name='End Time')),
                ('info', models.CharField(help_text='Add additional information, e.g. dress code, speakers title', max_length=200, verbose_name='Additional information')),
                ('location', models.ForeignKey(blank=True, help_text='Select where the event happens', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Location')),
            ],
        ),
    ]
