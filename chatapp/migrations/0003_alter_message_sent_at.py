# Generated by Django 3.2.4 on 2021-08-21 14:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_alter_message_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 21, 14, 50, 24, 595318, tzinfo=utc)),
        ),
    ]
