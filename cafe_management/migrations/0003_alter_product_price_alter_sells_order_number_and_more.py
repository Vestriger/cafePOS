# Generated by Django 5.0 on 2023-12-17 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_management', '0002_shifts_opened'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=1, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sells',
            name='order_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sells',
            name='product',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sells',
            name='worker',
            field=models.CharField(max_length=50),
        ),
    ]