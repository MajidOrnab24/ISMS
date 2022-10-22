# Generated by Django 4.1.1 on 2022-10-22 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0020_alter_studentprofile_semester_facultyprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultyprofile',
            name='gender',
            field=models.CharField(choices=[('Female', 'FEMALE'), ('Male', 'MALE')], max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('Female', 'FEMALE'), ('Male', 'MALE')], max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(5, '5'), (6, '6'), (1, '1'), (7, '7'), (3, '3'), (2, '2'), (4, '4'), (8, '8')], default=1),
        ),
        migrations.CreateModel(
            name='DeptHeadFaculty',
            fields=[
                ('dept', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='admin_app.department')),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_app.facultyprofile')),
            ],
        ),
    ]
