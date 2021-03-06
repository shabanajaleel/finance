# Generated by Django 4.0.1 on 2022-01-28 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeadmin', '0006_alter_partner_partner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profit',
            name='created_date',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='partnership',
            unique_together={('project', 'partner')},
        ),
    ]
