# Generated by Django 4.0.1 on 2022-01-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeadmin', '0004_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profit',
            name='created_date',
            field=models.DateField(),
        ),
    ]
