# Generated by Django 2.0.2 on 2019-04-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_auto_20190424_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='courses/%Y/%m', verbose_name='封面图'),
        ),
    ]
