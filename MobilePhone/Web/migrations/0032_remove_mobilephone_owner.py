# Generated by Django 2.1.14 on 2019-11-16 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0031_auto_20191116_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilephone',
            name='Owner',
        ),
    ]
