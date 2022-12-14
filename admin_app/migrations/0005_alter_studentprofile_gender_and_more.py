# Generated by Django 4.1.1 on 2022-10-12 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_studentprofile_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'MALE'), ('Female', 'FEMALE')], max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(8, '8'), (5, '5'), (4, '4'), (3, '3'), (1, '1'), (2, '2'), (6, '6'), (7, '7')], default=1),
        ),
    ]
