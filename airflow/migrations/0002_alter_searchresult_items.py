# Generated by Django 3.2.9 on 2021-12-31 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='items',
            field=models.JSONField(default=[], null=True, verbose_name='Результат'),
        ),
    ]
