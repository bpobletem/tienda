# Generated by Django 5.0.6 on 2024-07-02 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_rename_administrador_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Admin',
            new_name='Administrador',
        ),
    ]
