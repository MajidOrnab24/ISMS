# Generated by Django 4.1.1 on 2022-10-12 18:06

import admin_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0005_alter_studentprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='department',
            field=models.CharField(choices=[('CSE', 'CSE'), ('EEE', 'EEE'), ('SWE', 'SWE'), ('MCE', 'ME'), ('IPE', 'IPE'), ('CEE', 'CEE'), ('BTM', 'BTM')], max_length=30, verbose_name=admin_app.models.department),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('Female', 'FEMALE'), ('Male', 'MALE')], max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(6, '6'), (5, '5'), (4, '4'), (1, '1'), (8, '8'), (7, '7'), (2, '2'), (3, '3')], default=1),
        ),
    ]
