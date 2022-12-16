# Generated by Django 4.1.1 on 2022-12-16 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0059_alter_enrollment_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='course_assigner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.facultyprofile')),
            ],
        ),
    ]
