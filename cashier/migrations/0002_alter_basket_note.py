# Generated by Django 3.2.6 on 2021-10-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='note',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]