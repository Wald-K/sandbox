# Generated by Django 2.2.6 on 2019-11-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20191118_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.FloatField(default=0),
        ),
    ]
