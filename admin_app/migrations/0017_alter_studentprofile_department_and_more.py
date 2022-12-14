# Generated by Django 4.1.1 on 2022-10-13 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0016_alter_studentprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_app.department'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('Female', 'FEMALE'), ('Male', 'MALE')], max_length=30),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(5, '5'), (4, '4'), (7, '7'), (8, '8'), (6, '6'), (1, '1'), (2, '2'), (3, '3')], default=1),
        ),
    ]
