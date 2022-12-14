# Generated by Django 4.1.1 on 2022-10-30 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0034_facultyprofile_designation'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='CR',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deptheadfaculty',
            name='email',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_app.facultyprofile'),
        ),
    ]
