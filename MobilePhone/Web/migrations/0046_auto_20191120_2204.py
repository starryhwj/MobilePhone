# Generated by Django 2.1.14 on 2019-11-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0045_mobilephone_heartbeat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tiktokaccount',
            name='Classification',
        ),
        migrations.AddField(
            model_name='tiktokaccount',
            name='Classification',
            field=models.ManyToManyField(to='Web.MaintenanceNumberMissionKeywordClassification', verbose_name='标签'),
        ),
    ]
