# Generated by Django 2.0.2 on 2019-04-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0026_auto_20190426_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]
