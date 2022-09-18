# Generated by Django 4.1.1 on 2022-09-18 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('type', models.CharField(choices=[('STUDENT', 'student'), ('FACULTY', 'faculty'), ('STAFF_LIB', 'staff_lib'), ('STAFF_MED', 'staff_med')], default='STUDENT', max_length=20)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_faculty', models.BooleanField(default=False)),
                ('is_staff_med', models.BooleanField(default=False)),
                ('is_staff_lib', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.useraccount',),
        ),
        migrations.CreateModel(
            name='StaffLib',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.useraccount',),
        ),
        migrations.CreateModel(
            name='StaffMed',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.useraccount',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.useraccount',),
        ),
    ]
