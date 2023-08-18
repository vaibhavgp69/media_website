# Generated by Django 4.2.4 on 2023-08-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_membership_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='age',
            field=models.IntegerField(choices=[(10, 'Kid'), (18, 'Teenager'), (25, 'Depressed'), (50, 'Dead')]),
        ),
    ]