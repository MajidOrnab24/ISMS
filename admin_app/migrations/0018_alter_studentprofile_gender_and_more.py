# Generated by Django 4.1.1 on 2022-10-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0017_alter_studentprofile_department_and_more'),
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
            field=models.IntegerField(choices=[(2, '2'), (3, '3'), (6, '6'), (4, '4'), (7, '7'), (8, '8'), (1, '1'), (5, '5')], default=1),
        ),
    ]
