# Generated by Django 4.2.4 on 2023-08-15 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_likepost_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
