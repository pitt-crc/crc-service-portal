# Generated by Django 5.1.2 on 2024-10-12 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research_products', '0002_grant_grant_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='group',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='group',
        ),
    ]