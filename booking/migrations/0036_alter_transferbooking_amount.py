# Generated by Django 4.2 on 2024-11-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0035_auto_20241109_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferbooking',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
