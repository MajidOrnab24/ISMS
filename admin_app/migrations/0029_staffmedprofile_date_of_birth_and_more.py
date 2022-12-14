# Generated by Django 4.1.1 on 2022-10-23 14:19

import admin_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0028_alter_facultyprofile_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmedprofile',
            name='date_of_birth',
            field=models.DateField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='staffmedprofile',
            name='image',
            field=models.ImageField(upload_to=admin_app.models.filepathStaff),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(6, '6'), (5, '5'), (1, '1'), (3, '3'), (2, '2'), (4, '4'), (8, '8'), (7, '7')], default=1),
        ),
    ]
