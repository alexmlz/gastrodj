# Generated by Django 3.1.7 on 2021-05-12 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0022_basket_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='addzusatz',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
