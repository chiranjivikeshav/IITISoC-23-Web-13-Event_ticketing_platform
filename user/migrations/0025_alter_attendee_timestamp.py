# Generated by Django 4.2.2 on 2023-07-26 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0024_alter_attendee_attendecontact_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendee",
            name="timeStamp",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 7, 26, 19, 18, 22, 609077),
                null=True,
            ),
        ),
    ]
