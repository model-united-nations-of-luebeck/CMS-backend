# Generated by Django 2.2.6 on 2019-10-06 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_issue_lunch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Document's name", max_length=100, verbose_name='Name of the document')),
                ('path', models.CharField(help_text='Path to document on server', max_length=512, verbose_name='Path')),
                ('created', models.DateTimeField(help_text='When was this document created', verbose_name='Created at')),
                ('author', models.CharField(blank=True, help_text='Who created this document?', max_length=100, verbose_name='Author(s)')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='info',
            field=models.CharField(blank=True, help_text='Add additional information, e.g. dress code, speakers title', max_length=200, verbose_name='Additional information'),
        ),
        migrations.CreateModel(
            name='ResearchReport',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Document')),
                ('issue', models.ForeignKey(help_text='Select the issue this research report belongs to', on_delete=django.db.models.deletion.CASCADE, to='api.Issue')),
            ],
            options={
                'verbose_name': 'Research Report',
            },
            bases=('api.document',),
        ),
        migrations.CreateModel(
            name='PositionPaper',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Document')),
                ('delegate', models.ForeignKey(help_text='Who has written this position paper?', on_delete=django.db.models.deletion.CASCADE, to='api.Delegate')),
            ],
            bases=('api.document',),
        ),
    ]
