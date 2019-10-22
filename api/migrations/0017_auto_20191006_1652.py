# Generated by Django 2.2.6 on 2019-10-06 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20191006_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Participant')),
                ('car', models.BooleanField(blank=True, default=False, help_text='Do you have a car available during MUNOL and have a driving license so that you could help driving people and stuff around?', verbose_name='Car available')),
                ('availability', models.CharField(blank=True, help_text='Please specify on which days and nighs you will attend the conference and give your advice', max_length=512, verbose_name='Availability during week')),
                ('experience', models.CharField(blank=True, help_text="Please specify which role you had in former MUNOL sessions and other conferences, e.g. 'School Management 2013'", max_length=512, verbose_name='MUN Experience')),
                ('help', models.CharField(help_text='In which areas would you like to support the team?', max_length=512, verbose_name='Areas of help')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.participant',),
        ),
        migrations.AlterModelOptions(
            name='positionpaper',
            options={'verbose_name': 'Position Paper'},
        ),
    ]