# Generated by Django 5.0 on 2023-12-06 20:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_userstatus_last_seen_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstatus',
            name='last_seen_message',
        ),
        migrations.CreateModel(
            name='MessageCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_checked', models.DateTimeField(default=django.utils.timezone.now)),
                ('other_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checked_messages_from', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_checks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'other_user')},
            },
        ),
    ]
