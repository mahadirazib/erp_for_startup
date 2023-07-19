# Generated by Django 4.1.5 on 2023-01-29 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='clientAndServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.BooleanField()),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('occupation', models.CharField(blank=True, max_length=50)),
                ('companyName', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='spendMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('purpose', models.CharField(max_length=50)),
                ('medium', models.CharField(max_length=30)),
                ('spendOn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.clientandserviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='recivedMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('purpose', models.CharField(max_length=50)),
                ('medium', models.CharField(max_length=30)),
                ('recivedFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.clientandserviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='deals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giveOrReceive', models.CharField(choices=[('give', 'Give'), ('recive', 'Recive')], max_length=10)),
                ('dealAmount', models.IntegerField()),
                ('deadLine', models.DateField()),
                ('dealWith', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.clientandserviceprovider')),
            ],
        ),
    ]
