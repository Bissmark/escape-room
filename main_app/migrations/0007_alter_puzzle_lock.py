# Generated by Django 4.2.4 on 2023-12-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_puzzle_lock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='lock',
            field=models.CharField(choices=[('None', 'None'), ('Key', 'Key'), ('number', 'Number'), ('letter', 'Letter'), ('dial', 'Dial')], default='None', max_length=100),
        ),
    ]
