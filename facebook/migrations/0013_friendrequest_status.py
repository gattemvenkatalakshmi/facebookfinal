# Generated by Django 3.2.12 on 2024-02-29 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0012_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.TextField(default='pending'),
        ),
    ]
