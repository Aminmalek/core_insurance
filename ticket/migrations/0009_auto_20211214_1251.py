# Generated by Django 3.2.5 on 2021-12-14 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_auto_20211213_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='deducations',
            new_name='deductions',
        ),
        migrations.RenameField(
            model_name='claim',
            old_name='tarrif',
            new_name='tariff',
        ),
    ]
