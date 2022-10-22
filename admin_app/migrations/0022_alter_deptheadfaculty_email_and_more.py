# Generated by Django 4.1.1 on 2022-10-22 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0021_alter_facultyprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deptheadfaculty',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_app.facultyprofile', unique=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(2, '2'), (8, '8'), (1, '1'), (4, '4'), (3, '3'), (7, '7'), (6, '6'), (5, '5')], default=1),
        ),
    ]
