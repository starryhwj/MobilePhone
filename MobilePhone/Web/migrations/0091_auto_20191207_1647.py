# Generated by Django 2.1.14 on 2019-12-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0090_allmissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiktokaccount',
            name='ShareURL',
            field=models.TextField(default='', max_length=150, verbose_name='短链接'),
        ),
    ]
