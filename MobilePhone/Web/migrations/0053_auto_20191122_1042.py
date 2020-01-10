# Generated by Django 2.1.14 on 2019-11-22 10:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0052_remove_tiktokaccount_isonline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenancenumbermission',
            name='During',
        ),
        migrations.RemoveField(
            model_name='mutualbrushmission',
            name='EffectTime',
        ),
        migrations.AddField(
            model_name='followmission',
            name='Priority',
            field=models.IntegerField(default=0, verbose_name='优先级'),
        ),
        migrations.AddField(
            model_name='followmission',
            name='StartTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='任务开始日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maintenancenumbermission',
            name='EndTime',
            field=models.DateTimeField(auto_now=True, verbose_name='任务结束日期'),
        ),
        migrations.AddField(
            model_name='maintenancenumbermission',
            name='Priority',
            field=models.IntegerField(default=0, verbose_name='优先级'),
        ),
        migrations.AddField(
            model_name='maintenancenumbermission',
            name='StartTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='任务开始日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mutualbrushmission',
            name='Priority',
            field=models.IntegerField(default=0, verbose_name='优先级'),
        ),
        migrations.AddField(
            model_name='mutualbrushmission',
            name='StartTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='任务开始日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scanmission',
            name='Priority',
            field=models.IntegerField(default=0, verbose_name='优先级'),
        ),
        migrations.AddField(
            model_name='scanmission',
            name='StartTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='任务开始日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videomission',
            name='Priority',
            field=models.IntegerField(default=0, verbose_name='优先级'),
        ),
        migrations.AddField(
            model_name='videomission',
            name='StartTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='任务开始日期'),
            preserve_default=False,
        ),
    ]
