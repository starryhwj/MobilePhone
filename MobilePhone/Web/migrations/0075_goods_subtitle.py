# Generated by Django 2.1.14 on 2019-11-29 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0074_piddaysummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='SubTitle',
            field=models.TextField(default='', max_length=150, verbose_name='短标题'),
        ),
    ]
