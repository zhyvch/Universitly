# Generated by Django 5.1.6 on 2025-02-28 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0002_initial'),
        ('students', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ['first_name', 'last_name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.AddField(
            model_name='studenthomework',
            name='section_homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='education.sectionhomework', verbose_name='Related test'),
        ),
        migrations.AddField(
            model_name='studenthomeworkfile',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='students.studenthomework', verbose_name='Related homework'),
        ),
        migrations.AddField(
            model_name='studenttestattempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='education.sectiontest', verbose_name='Attempted test'),
        ),
        migrations.AddField(
            model_name='studenttestattempt',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_attempts', to='students.student', verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='studenthomework',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='students.student', verbose_name='Student'),
        ),
    ]
