# Generated by Django 3.1.7 on 2021-04-15 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0009_auto_20210415_0726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cat',
            name='description_long',
        ),
        migrations.AddField(
            model_name='nugget',
            name='description_long',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
