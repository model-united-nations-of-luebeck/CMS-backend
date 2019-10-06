# Generated by Django 2.2.6 on 2019-10-06 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_forum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plenary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="e.g. 'General Assembly' or 'Economic and Social Council'", max_length=50, verbose_name='Plenary Name')),
            ],
        ),
        migrations.AddField(
            model_name='forum',
            name='plenary',
            field=models.ForeignKey(blank=True, help_text='Select a Plenary if this forum is part of it, otherwise choose none.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Plenary'),
        ),
        migrations.AddField(
            model_name='studentofficer',
            name='plenary',
            field=models.ForeignKey(blank=True, help_text='Select if this Student Officer is also chairing a Plenary.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Plenary'),
        ),
    ]
