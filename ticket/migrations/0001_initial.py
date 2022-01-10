# Generated by Django 3.2.5 on 2021-11-10 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_insuranceconnector_register_form'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=250, null=True)),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Reopened', 'Reopened'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=10, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250, null=True)),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Reopened', 'Reopened'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=10)),
                ('response', models.TextField(max_length=250)),
                ('claim_form', models.JSONField()),
                ('is_archived', models.BooleanField(default=False)),
                ('franchise', models.IntegerField(null=True)),
                ('tarrif', models.IntegerField(null=True)),
                ('payable_amount', models.IntegerField(null=True)),
                ('deducations', models.IntegerField(null=True)),
                ('claimed_amount', models.IntegerField(null=True)),
                ('claim_date', models.DateTimeField(null=True)),
                ('specefic_name', models.CharField(max_length=50)),
                ('coverage', models.CharField(max_length=40)),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payment.insuranceconnector')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
