# Generated by Django 4.1.5 on 2023-02-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_room_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='game',
            field=models.CharField(default=None, max_length=6, null=True),
        ),
    ]