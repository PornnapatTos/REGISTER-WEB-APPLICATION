# Generated by Django 3.1.1 on 2020-09-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=5)),
                ('course_name', models.CharField(max_length=64)),
                ('course_sem', models.CharField(max_length=1)),
                ('course_year', models.CharField(max_length=4)),
                ('course_total', models.CharField(max_length=64)),
                ('course_status', models.CharField(max_length=1)),
            ],
        ),
    ]
