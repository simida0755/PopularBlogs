# Generated by Django 2.0.2 on 2019-04-15 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20190415_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogposts',
            name='category',
            field=models.CharField(choices=[('py', 'python'), ('ja', 'java'), ('C', 'C++'), ('zw', '杂文')], max_length=2, null=True, verbose_name='文章分类'),
        ),
        migrations.AlterField(
            model_name='blogposts',
            name='desc',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='文章描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='blogger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Blogger', verbose_name='所属博主'),
        ),
    ]
