# Generated by Django 5.0 on 2023-12-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifts',
            name='opened',
            field=models.BooleanField(default=False),
        ),
    ]
