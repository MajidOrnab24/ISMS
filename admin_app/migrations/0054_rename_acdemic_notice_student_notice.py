# Generated by Django 4.1.1 on 2022-11-22 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0053_acdemic_notice'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='acdemic_notice',
            new_name='student_notice',
        ),
    ]
