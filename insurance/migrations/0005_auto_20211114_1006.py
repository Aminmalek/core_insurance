# Generated by Django 3.2.5 on 2021-11-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0004_auto_20211112_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coverage',
            name='capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='coverage',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
