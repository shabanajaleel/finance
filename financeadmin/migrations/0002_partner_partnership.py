# Generated by Django 4.0.1 on 2022-01-24 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='partnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partnership', models.IntegerField()),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeadmin.partner')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeadmin.project')),
            ],
        ),
    ]
