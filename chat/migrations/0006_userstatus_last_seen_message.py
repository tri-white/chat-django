# Generated by Django 5.0 on 2023-12-06 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_userstatus_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='last_seen_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_seen_message', to='chat.message'),
        ),
    ]
