# Generated by Django 3.1 on 2020-11-20 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0002_auto_20201117_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionbeneficio',
            name='fecha_entrega',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
