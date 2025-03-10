# Generated by Django 5.1.6 on 2025-02-28 12:17

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'ordering': ['first_name', 'last_name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
    ]
