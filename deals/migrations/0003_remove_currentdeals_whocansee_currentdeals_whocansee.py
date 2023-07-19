# Generated by Django 4.1.5 on 2023-01-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
        ('deals', '0002_rename_deals_currentdeals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentdeals',
            name='whoCanSee',
        ),
        migrations.AddField(
            model_name='currentdeals',
            name='whoCanSee',
            field=models.ManyToManyField(to='userAuth.userinfo'),
        ),
    ]
