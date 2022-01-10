# Generated by Django 3.2.5 on 2021-10-07 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(max_length=150)),
                ('price', models.IntegerField(null=True)),
                ('register_form', models.JSONField(null=True)),
                ('claim_form', models.JSONField(null=True)),
            ],
        ),
    ]
