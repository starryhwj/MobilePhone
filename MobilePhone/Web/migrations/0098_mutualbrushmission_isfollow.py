# Generated by Django 2.1.14 on 2019-12-25 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0097_watchlivemission_commenttimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mutualbrushmission',
            name='IsFollow',
            field=models.BooleanField(default=False, verbose_name='是否关注'),
        ),
    ]
