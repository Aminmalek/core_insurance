# Generated by Django 3.2.5 on 2021-11-13 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20211112_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='reviewer_timeline',
            field=models.ManyToManyField(blank=True, related_name='claim_reviewer_time_line_claim', to='ticket.ReviewerTimeline'),
        ),
    ]
