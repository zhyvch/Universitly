# Generated by Django 5.1.6 on 2025-02-18 21:13

import core.apps.common.models.fields
import core.apps.users.models.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('phone_number', core.apps.common.models.fields.PhoneNumberField(max_length=15, verbose_name='Phone number')),
                ('first_name', models.CharField(blank=True, max_length=254, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=254, verbose_name='Last name')),
                ('middle_name', models.CharField(blank=True, max_length=254, verbose_name='Middle name or patronymic')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/', verbose_name='Photo')),
                ('is_student', models.BooleanField(default=False, verbose_name='Is student')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Is teacher')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='Date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['email'],
            },
            managers=[
                ('objects', core.apps.users.models.managers.UserManager()),
            ],
        ),
    ]
