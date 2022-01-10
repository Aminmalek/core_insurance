# Generated by Django 3.2.5 on 2021-12-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_alter_reviewertimeline_date'),
        ('payment', '0003_insuranceconnector_register_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceconnector',
            name='claim',
            field=models.ManyToManyField(blank=True, related_name='users_Claim', to='ticket.Claim'),
        ),
    ]
