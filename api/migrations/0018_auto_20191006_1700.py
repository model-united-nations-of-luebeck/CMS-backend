# Generated by Django 2.2.6 on 2019-10-06 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20191006_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='mundirector',
            name='housing',
            field=models.CharField(choices=[('hostel', 'hostel'), ('guest family', 'guest family'), ('other', 'other self-organized accommodation')], default='other', help_text='Please note, that housing in guest families is not available for all MUN-Directors.', max_length=50, verbose_name='Housing option'),
        ),
        migrations.AddField(
            model_name='school',
            name='fee',
            field=models.BooleanField(default=False, help_text='Was the pre-registration fee paid?', verbose_name='Pre-registration fee'),
        ),
        migrations.AlterField(
            model_name='school',
            name='registration_status',
            field=models.CharField(choices=[('WAITING_FOR_PRE_REGISTRATION', 'waiting for pre-registration'), ('PRE_REGISTRATION_DONE', 'pre-registration done'), ('WAITING_FOR_DATA_PROTECTION', 'waiting for data protection'), ('WAITING_FOR_FINAL_REGISTRATION', 'waiting for final registration'), ('FINAL_REGISTRATION_DONE', 'final registration done'), ('CANCELED', 'canceled')], default='WAITING_FOR_PRE_REGISTRATION', help_text='This status indicates at what stage of registration the school is.', max_length=50, verbose_name='Registation status'),
        ),
    ]