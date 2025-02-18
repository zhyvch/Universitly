# Generated by Django 5.1.6 on 2025-02-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentHomework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Student homework',
                'verbose_name_plural': 'Student homeworks',
            },
        ),
        migrations.CreateModel(
            name='StudentHomeworkFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='homework_files/', verbose_name='File')),
            ],
            options={
                'verbose_name': 'Student homework file',
                'verbose_name_plural': 'Student homework files',
            },
        ),
        migrations.CreateModel(
            name='StudentTestAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('answered_correctly', models.PositiveSmallIntegerField(default=0, verbose_name='Answered correctly')),
            ],
            options={
                'verbose_name': 'Student test attempt',
                'verbose_name_plural': 'Student test attempts',
            },
        ),
    ]
