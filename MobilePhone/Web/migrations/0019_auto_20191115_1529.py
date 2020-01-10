# Generated by Django 2.1.14 on 2019-11-15 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0018_videomission_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenancenumbermission',
            name='VideoURL',
        ),
        migrations.AddField(
            model_name='maintenancenumbermission',
            name='TikTokID',
            field=models.TextField(max_length=150, null=True, verbose_name='抖音号'),
        ),
    ]
