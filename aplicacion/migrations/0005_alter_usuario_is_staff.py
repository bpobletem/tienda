# Generated by Django 5.0.6 on 2024-07-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0004_rename_admin_administrador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
