# Generated by Django 3.2.5 on 2021-11-13 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_claim_reviewer_timeline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewertimeline',
            old_name='data',
            new_name='date',
        ),
    ]
