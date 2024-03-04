# Generated by Django 3.2.12 on 2024-02-28 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends_id', models.ManyToManyField(related_name='Friends', to='facebook.User')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.user', verbose_name='Friends')),
            ],
        ),
    ]