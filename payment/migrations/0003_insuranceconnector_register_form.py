# Generated by Django 3.2.5 on 2021-10-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_insuranceconnector_register_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceconnector',
            name='register_form',
            field=models.JSONField(null=True),
        ),
    ]