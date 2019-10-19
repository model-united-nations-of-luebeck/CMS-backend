# Generated by Django 2.2.6 on 2019-10-05 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_delegate_represents'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name will be used like this for badges and certificates.', max_length=50, verbose_name='School Name')),
                ('street', models.CharField(max_length=50, verbose_name='Street Name')),
                ('zipcode', models.CharField(max_length=10, verbose_name='ZIP Code')),
                ('country', models.CharField(max_length=50, verbose_name='Country of origin')),
                ('requested', models.PositiveSmallIntegerField(help_text='Note, that this is the <b>requested</b> number, <u>not</u> the confirmed one which might be lower.', verbose_name='Number of requested students')),
                ('housing', models.CharField(choices=[('hostel', 'hostel'), ('guest family', 'guest family'), ('other', 'other self-organized accommodation')], default='other', help_text='Please note, that housing in guest families is not available for all delegations and we will prefer international delegations in our housing who travels the longest distances.', max_length=50, verbose_name='Housing option')),
                ('registration_status', models.CharField(choices=[('WAITING_FOR_PRE_REGISTRATION', 'waiting for pre-registration'), ('PRE_REGISTRATION_DONE', 'pre-registration done'), ('WAITING_FOR_DATA_PROTECTION', 'waiting for data protection'), ('WAITING_FOR_FINAL_REGISTRATION', 'waiting for final registration'), ('FINAL_REGISTRATION_DONE', 'final registration done')], default='WAITING_FOR_PRE_REGISTRATION', help_text='This status indicates at what stage of registration the school is.', max_length=50, verbose_name='Registation status')),
                ('arrival', models.TextField(blank=True, help_text='Please provide date, time and location (e.g. school, conference venue, train station, airport, ...) of arrival here so that we can plan the registration process and housing respectively.', verbose_name='Arrival Information')),
                ('departure', models.TextField(blank=True, help_text='Please provide date, time and location (e.g. conference venue, train station, airport, ...) of departure here so that we can plan in advance.', verbose_name='Departure Information')),
            ],
        ),
        migrations.AlterField(
            model_name='delegate',
            name='represents',
            field=models.ForeignKey(help_text='select member organization which is represented by this delegate', on_delete=django.db.models.deletion.PROTECT, to='api.MemberOrganization'),
        ),
        migrations.AddField(
            model_name='delegate',
            name='school',
            field=models.ForeignKey(default='0', help_text='select the school which is attended by this delegate', on_delete=django.db.models.deletion.PROTECT, to='api.School'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mundirector',
            name='school',
            field=models.ForeignKey(default='0', help_text='select the school at which this MUN Director teaches', on_delete=django.db.models.deletion.PROTECT, to='api.School'),
            preserve_default=False,
        ),
    ]
