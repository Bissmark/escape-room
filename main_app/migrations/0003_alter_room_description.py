# Generated by Django 4.2.4 on 2023-12-13 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(max_length=250),
        ),
    ]
