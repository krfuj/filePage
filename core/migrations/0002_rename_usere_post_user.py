# Generated by Django 4.1.2 on 2022-10-15 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="usere",
            new_name="user",
        ),
    ]
