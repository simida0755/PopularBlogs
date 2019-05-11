# Generated by Django 2.0.2 on 2019-04-15 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20190413_1114'),
        ('course', '0002_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='blogger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.BlogOrg', verbose_name='所属博主'),
        ),
    ]
