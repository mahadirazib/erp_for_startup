# Generated by Django 4.1.5 on 2023-01-29 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_clientandserviceprovider_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientandserviceprovider',
            old_name='client',
            new_name='isClient',
        ),
    ]
