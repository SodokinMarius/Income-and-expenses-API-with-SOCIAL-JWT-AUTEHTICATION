# Generated by Django 4.0.4 on 2022-09-03 17:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='category',
        ),
        migrations.AddField(
            model_name='income',
            name='source',
            field=models.CharField(choices=[('SALARY', 'SALARY'), ('BUSINESSES', 'BUSINESSES'), ('FIVEN', 'GIVEN'), ('FARMS', 'FARMS'), ('OTHERS', 'OTHERS')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
