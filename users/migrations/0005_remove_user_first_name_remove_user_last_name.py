# Generated by Django 5.0.4 on 2024-04-25 10:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
    ]
