# Generated by Django 4.2.7 on 2023-11-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ice_cream_truck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flavor',
            name='name',
            field=models.CharField(choices=[('Chocolate', 'Chocolate'), ('Pistachio', 'Pistachio'), ('Strawberry', 'Strawberry'), ('Mint', 'Mint')], default='Chocolate', max_length=20),
        ),
    ]