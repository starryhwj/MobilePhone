# Generated by Django 2.1.14 on 2019-12-31 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0105_auto_20191230_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliconfig',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='commentlibrary',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='commoditydataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='maintenancenumbermissionkeyword',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='maintenancenumbermissionkeywordclassification',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='mobilephone',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='tiktokaccountdataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='tiktokaccountgroup',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='worksdataanalysis',
            name='Owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
    ]
