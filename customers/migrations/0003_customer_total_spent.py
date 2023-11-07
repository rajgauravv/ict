# Generated by Django 4.2.7 on 2023-11-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='total_spent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
