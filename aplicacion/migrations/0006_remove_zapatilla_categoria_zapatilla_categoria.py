# Generated by Django 5.0.6 on 2024-06-22 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0005_alter_zapatilla_modelo_delete_modelo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zapatilla',
            name='categoria',
        ),
        migrations.AddField(
            model_name='zapatilla',
            name='categoria',
            field=models.ManyToManyField(to='aplicacion.categoria'),
        ),
    ]
