# Generated by Django 4.2.4 on 2023-12-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_puzzle_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='lock',
            field=models.CharField(default='None', max_length=100),
        ),
    ]