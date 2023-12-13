# Generated by Django 4.2.7 on 2023-12-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('allocations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='start',
            field=models.DateField(auto_now_add=True, verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='submitted',
            field=models.DateField(auto_now_add=True, verbose_name='Submission Date'),
        ),
    ]