# Generated by Django 2.1.14 on 2019-12-03 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0078_order_aliconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Goods',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.Goods', verbose_name='商品'),
        ),
    ]
