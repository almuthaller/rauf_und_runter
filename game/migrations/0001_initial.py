# Generated by Django 4.1.5 on 2023-02-03 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.SlugField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('round_no', models.PositiveIntegerField(default=1)),
                ('current_player', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(default=None, max_length=40, null=True)),
                ('current_bet', models.PositiveIntegerField(default=None, null=True)),
                ('tricks_won', models.PositiveIntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit', models.IntegerField(default=None)),
                ('rank', models.IntegerField(default=None)),
                ('played', models.BooleanField(default=False)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.room')),
            ],
        ),
    ]