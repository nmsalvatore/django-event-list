# Generated by Django 4.0.4 on 2022-05-01 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_event_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['title']},
        ),
    ]