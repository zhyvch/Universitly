# Generated by Django 5.1.6 on 2025-02-28 12:27

from django.db import migrations

def populate_email(apps, schema_editor):
    Email = apps.get_model('tasks', 'Email')

    Email.objects.bulk_create([
        Email(
            type='CI',
            subject='Institution successfully created',
            plain_text='Dear %(name)s,\n\nYour institution "%(institution)s" has been successfully created.\n\nBest regards,\nUniversitly Team',
            html='<p>Dear %(name)s,</p><p>Your institution "<strong>%(institution)s</strong>" has been successfully created.</p><p>Best regards,<br>Universitly Team</p>'
        ),
        Email(
            type='UI',
            subject='Institution information updated',
            plain_text='Dear %(name)s,\n\nYour institution "%(institution)s" has been updated with the following changes:\n%(changes)s\n\nBest regards,\nUniversitly Team',
            html='<p>Dear %(name)s,</p><p>Your institution "<strong>%(institution)s</strong>" has been updated with the following changes:</p><p>%(changes)s</p><p>Best regards,<br>Universitly Team</p>'
        ),
        Email(
            type='DI',
            subject='Deletion of institution',
            plain_text='Dear %(name)s,\n\nYour institution "%(institution)s" has been deleted.\n\nBest regards,\nUniversitly Team',
            html='<p>Dear %(name)s,</p><p>Your institution "<strong>%(institution)s</strong>" has been deleted.</p><p>Best regards,<br>Universitly Team</p>'
        ),
        Email(
            type='M',
            subject='Periodic test mail',
            plain_text='Test',
            html='<p>Test</p><h1>Test</h1>'
        ),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_email),
    ]
