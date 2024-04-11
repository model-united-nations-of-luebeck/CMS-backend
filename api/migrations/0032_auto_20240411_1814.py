# Generated by Django 3.1.14 on 2024-04-11 18:14

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_event_relevance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='relevance',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('advisor', 'Conference Advisor'), ('student officer', 'Student Officer'), ('delegate', 'Delegate'), ('mun_director', 'MUN Director'), ('executive', 'Executive'), ('staff', 'Staff')], max_length=61, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='role',
            field=models.CharField(blank=True, choices=[('advisor', 'Conference Advisor'), ('student officer', 'Student Officer'), ('delegate', 'Delegate'), ('mun_director', 'MUN Director'), ('executive', 'Executive'), ('staff', 'Staff')], editable=False, max_length=15, verbose_name='the role they are participating in the conference as'),
        ),
    ]
