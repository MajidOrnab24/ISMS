# Generated by Django 4.1.1 on 2022-11-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0045_rename_remeration_medlog_remuneration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medlog',
            name='remuneration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]