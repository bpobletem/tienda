# Generated by Django 5.0.6 on 2024-06-21 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'Enviado'), ('C', 'Completado'), ('A', 'Anulado')], default='P', max_length=1)),
                ('total', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.usuario')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.direccion')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoZapatilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.pedido')),
                ('zapatilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.zapatilla')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='zapatillas',
            field=models.ManyToManyField(through='aplicacion.PedidoZapatilla', to='aplicacion.zapatilla'),
        ),
    ]
