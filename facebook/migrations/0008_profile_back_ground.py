# Generated by Django 3.2.12 on 2024-02-28 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0007_auto_20240228_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='back_ground',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
