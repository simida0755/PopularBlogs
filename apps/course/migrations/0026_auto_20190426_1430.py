# Generated by Django 2.0.2 on 2019-04-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0025_auto_20190426_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图'),
        ),
    ]
