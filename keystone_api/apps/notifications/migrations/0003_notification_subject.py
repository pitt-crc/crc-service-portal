# Generated by Django 5.0.7 on 2024-08-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='subject',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
