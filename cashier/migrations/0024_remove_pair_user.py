# Generated by Django 3.1.7 on 2021-05-12 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0023_auto_20210512_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pair',
            name='user',
        ),
    ]