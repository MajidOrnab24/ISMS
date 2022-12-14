# Generated by Django 4.1.1 on 2022-10-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0030_stafflibprofile_alter_facultyprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultyprofile',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], default='MALE', max_length=30),
        ),
        migrations.AlterField(
            model_name='stafflibprofile',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], default='MALE', max_length=30),
        ),
        migrations.AlterField(
            model_name='staffmedprofile',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], default='MALE', max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], default='MALE', max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(5, '5'), (8, '8'), (2, '2'), (6, '6'), (1, '1'), (4, '4'), (3, '3'), (7, '7')], default=1),
        ),
    ]
