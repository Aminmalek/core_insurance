# Generated by Django 3.2.5 on 2021-10-07 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_insuranceconnector_register_form'),
        ('insured', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='insured',
            name='bank_account_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='insured',
            name='insurance',
            field=models.ManyToManyField(blank=True, to='payment.InsuranceConnector'),
        ),
    ]
