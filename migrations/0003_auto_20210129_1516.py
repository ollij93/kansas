# Generated by Django 2.2.9 on 2021-01-29 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kansas', '0002_auto_20210126_2205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
