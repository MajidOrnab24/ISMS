# Generated by Django 4.1.2 on 2022-10-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_app", "0018_alter_studentprofile_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="semester",
            field=models.IntegerField(
                choices=[
                    (7, "7"),
                    (4, "4"),
                    (5, "5"),
                    (1, "1"),
                    (3, "3"),
                    (2, "2"),
                    (6, "6"),
                    (8, "8"),
                ],
                default=1,
            ),
        ),
    ]
