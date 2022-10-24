# Generated by Django 4.1.2 on 2022-10-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_app", "0031_alter_facultyprofile_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="semester",
            field=models.IntegerField(
                choices=[
                    (8, "8"),
                    (1, "1"),
                    (7, "7"),
                    (2, "2"),
                    (6, "6"),
                    (5, "5"),
                    (3, "3"),
                    (4, "4"),
                ],
                default=1,
            ),
        ),
    ]
