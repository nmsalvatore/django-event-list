# Generated by Django 4.0.4 on 2022-05-15 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cost',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
