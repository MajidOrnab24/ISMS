# Generated by Django 4.1.1 on 2022-10-30 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0039_books'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='rack_no',
            new_name='shelf_no',
        ),
    ]
