# Generated by Django 5.0.6 on 2024-07-03 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0006_alter_usuario_is_staff_alter_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidozapatilla',
            name='talla',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=3),
        ),
    ]
