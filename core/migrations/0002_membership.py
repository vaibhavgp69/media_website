# Generated by Django 4.2.4 on 2023-08-13 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=10)),
                ('lname', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=20)),
                ('passwd', models.CharField(max_length=20)),
                ('age', models.IntegerField(max_length=3)),
            ],
        ),
    ]
