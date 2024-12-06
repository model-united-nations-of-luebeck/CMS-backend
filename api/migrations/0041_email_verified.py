# Generated by Django 4.2.16 on 2024-11-11 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_participant_data_consent_ip_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mundirector',
            name='landline_phone',
        ),
        migrations.AddField(
            model_name='participant',
            name='email_verified',
            field=models.BooleanField(default=False, help_text='Has the email address been verified?', verbose_name='E-Mail verified'),
        ),
        migrations.AlterField(
            model_name='studentofficer',
            name='position_name',
            field=models.CharField(help_text="Full position name, e.g. 'Vice-Chairman of the First Committee', 'Chairwoman of the Human Rights Council' or 'President of the General Assembly'", max_length=100, verbose_name='Position name'),
        ),
    ]