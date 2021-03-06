# Generated by Django 2.1.14 on 2020-01-06 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0108_tiktokaccount_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='commoditydataanalysis',
            name='CommodityOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='商品拥有者', to=settings.AUTH_USER_MODEL, verbose_name='商品拥有者'),
        ),
        migrations.AddField(
            model_name='tiktokaccountdataanalysis',
            name='AccountOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='账号拥有者', to=settings.AUTH_USER_MODEL, verbose_name='账号拥有者'),
        ),
        migrations.AddField(
            model_name='worksdataanalysis',
            name='WorkOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='作品拥有者', to=settings.AUTH_USER_MODEL, verbose_name='作品拥有者'),
        ),
        migrations.AlterField(
            model_name='commoditydataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='商品分析数据拥有者', to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AlterField(
            model_name='tiktokaccountdataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='账号分析数据拥有者', to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AlterField(
            model_name='worksdataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='作品分析数据拥有者', to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
    ]
