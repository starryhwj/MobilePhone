# Generated by Django 2.1.14 on 2019-11-13 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0012_auto_20191113_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='Goods',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.Goods', verbose_name='商品'),
        ),
    ]
