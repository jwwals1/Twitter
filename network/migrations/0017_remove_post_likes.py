# Generated by Django 4.2.5 on 2023-09-12 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_rename_newpost_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]