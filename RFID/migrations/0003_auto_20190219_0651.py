# Generated by Django 2.1.5 on 2019-02-19 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFID', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
