# Generated by Django 2.1.14 on 2019-11-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0055_auto_20191122_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followmission',
            name='StartTime',
            field=models.DateTimeField(verbose_name='任务开始日期'),
        ),
        migrations.AlterField(
            model_name='maintenancenumbermission',
            name='StartTime',
            field=models.DateTimeField(verbose_name='任务开始日期'),
        ),
        migrations.AlterField(
            model_name='mutualbrushmission',
            name='StartTime',
            field=models.DateTimeField(verbose_name='任务开始日期'),
        ),
        migrations.AlterField(
            model_name='scanmission',
            name='StartTime',
            field=models.DateTimeField(verbose_name='任务开始日期'),
        ),
        migrations.AlterField(
            model_name='videomission',
            name='StartTime',
            field=models.DateTimeField(verbose_name='任务开始日期'),
        ),
    ]
