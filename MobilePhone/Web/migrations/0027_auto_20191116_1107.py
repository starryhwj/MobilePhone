# Generated by Django 2.1.14 on 2019-11-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0026_aliconfig_lastpid'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='CouponURL',
            field=models.TextField(max_length=500, null=True, verbose_name='优惠券URL'),
        ),
        migrations.AddField(
            model_name='goods',
            name='PIDURL',
            field=models.TextField(max_length=500, null=True, verbose_name='推广URL'),
        ),
    ]
