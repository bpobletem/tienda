# Generated by Django 5.0.6 on 2024-06-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0013_carrito_itemcarrito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zapatilla',
            name='descripcion',
            field=models.CharField(max_length=250),
        ),
    ]
