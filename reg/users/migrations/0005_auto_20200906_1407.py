# Generated by Django 3.1.1 on 2020-09-06 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200905_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_status',
            field=models.CharField(choices=[('open', 'Open'), ('close', 'Close')], max_length=5),
        ),
    ]