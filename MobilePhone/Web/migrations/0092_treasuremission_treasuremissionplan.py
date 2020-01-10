# Generated by Django 2.1.14 on 2019-12-09 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0091_auto_20191207_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreasureMission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.IntegerField(choices=[(0, '待获取'), (1, '已获取'), (2, '已成功结束'), (3, '执行失败')], default=0, verbose_name='状态')),
                ('CreateTime', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('UpdateTime', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('StartTime', models.DateTimeField(verbose_name='任务开始日期')),
                ('EndTime', models.DateTimeField(null=True, verbose_name='任务结束日期')),
                ('Priority', models.IntegerField(default=0, verbose_name='优先级')),
                ('FailReason', models.TextField(null=True, verbose_name='失败原因')),
                ('MobilePhone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.MobilePhone', verbose_name='手机ID')),
                ('Owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='拥有者')),
            ],
        ),
        migrations.CreateModel(
            name='TreasureMissionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.TextField(max_length=150, null=True, verbose_name='标题')),
                ('Description', models.TextField(max_length=150, null=True, verbose_name='任务描述')),
                ('StartTime', models.DateTimeField(verbose_name='任务开始日期')),
                ('EndTime', models.DateTimeField(null=True, verbose_name='任务结束日期')),
                ('MissionPlanTemplate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.MissionPlanTemplate', verbose_name='模板ID')),
            ],
        ),
    ]
