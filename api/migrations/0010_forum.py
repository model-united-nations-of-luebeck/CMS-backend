# Generated by Django 2.2.6 on 2019-10-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20191005_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="e.g. 'First Committee', 'Economic and Social Council", max_length=50, verbose_name='Forum Name')),
                ('abbreviation', models.CharField(blank=True, help_text="e.g. 'GA1', 'ECOSOC'", max_length=10, verbose_name='Abbreviated Forum Name')),
                ('subtitle', models.CharField(blank=True, help_text="e.g. 'Disarmament and International Security", max_length=75, verbose_name='Explanatory Subtitle')),
                ('email', models.EmailField(blank=True, help_text='Email will be displayed on website', max_length=254, verbose_name='E-Mail')),
            ],
        ),
    ]