# Generated by Django 4.1.5 on 2023-01-29 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_alter_clientandserviceprovider_isclient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientandserviceprovider',
            name='isClient',
            field=models.BooleanField(blank=True),
        ),
    ]