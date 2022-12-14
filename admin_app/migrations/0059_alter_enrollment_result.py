# Generated by Django 4.1.1 on 2022-11-24 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0058_notice_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='result',
            field=models.FloatField(blank=True, choices=[(4.0, 'A+'), (3.75, 'A'), (3.5, 'A-'), (3.25, 'B+'), (3.0, 'B'), (2.75, 'B-'), (2.5, 'C+'), (2.25, 'C'), (2.0, 'D'), (0.0, 'F')], default=0.0, null=True),
        ),
    ]
