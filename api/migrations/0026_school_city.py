# Generated by Django 3.1.14 on 2022-06-10 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20220610_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='city',
            field=models.CharField(default='Lübeck', max_length=50, verbose_name='ZIP Code'),
            preserve_default=False,
        ),
    ]