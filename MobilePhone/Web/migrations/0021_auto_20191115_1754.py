# Generated by Django 2.1.14 on 2019-11-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0020_auto_20191115_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='followmission',
            name='Title',
            field=models.TextField(max_length=150, null=True, verbose_name='标题'),
        ),
        migrations.AddField(
            model_name='maintenancenumbermission',
            name='Title',
            field=models.TextField(max_length=150, null=True, verbose_name='标题'),
        ),
        migrations.AddField(
            model_name='mutualbrushmission',
            name='Title',
            field=models.TextField(max_length=150, null=True, verbose_name='标题'),
        ),
        migrations.AddField(
            model_name='scanmission',
            name='Title',
            field=models.TextField(max_length=150, null=True, verbose_name='标题'),
        ),
    ]
