# Generated by Django 2.2.12 on 2020-04-11 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20200411_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='tags',
            new_name='tag',
        ),
    ]