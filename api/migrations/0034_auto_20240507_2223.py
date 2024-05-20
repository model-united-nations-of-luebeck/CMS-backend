# Generated by Django 3.2.25 on 2024-05-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20240507_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='plenary',
            name='abbreviation',
            field=models.CharField(blank=True, help_text="e.g. 'GA', 'ECOSOC'", max_length=10, null=True, verbose_name='Abbreviated Plenary Name'),
        ),
        migrations.AddField(
            model_name='plenary',
            name='name',
            field=models.CharField(default='', help_text="e.g. 'General Assembly' or 'Economic and Social Council'", max_length=50, verbose_name='Plenary Name'),
            preserve_default=False,
        ),
    ]