# Generated by Django 4.2 on 2023-04-26 10:09

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
            name='Coordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selected', models.BooleanField(default=False)),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selected', models.BooleanField(default=False)),
                ('game_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=240)),
                ('draw', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('watchers', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.PositiveBigIntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('match', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='futsal.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=240)),
                ('description', models.TextField()),
                ('post_image', models.ImageField(upload_to='post/')),
                ('completion_status', models.BooleanField(default=False)),
                ('coordinators', models.ManyToManyField(related_name='cor_application', through='futsal.Coordinator', to=settings.AUTH_USER_MODEL)),
                ('game_managers', models.ManyToManyField(related_name='gm_application', through='futsal.GameManager', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team_image', models.ImageField(upload_to='team_image/')),
                ('title', models.CharField(max_length=240)),
                ('score', models.PositiveBigIntegerField(default=0)),
                ('match_completed', models.BooleanField(default=False)),
                ('players', models.ManyToManyField(related_name='player_teams', through='futsal.Players', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_teams', to='futsal.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='final_winner', to='futsal.team'),
        ),
        migrations.AddField(
            model_name='players',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_players', to='futsal.post'),
        ),
        migrations.AddField(
            model_name='players',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_player', to='futsal.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_matches', to='futsal.post'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_match', to='futsal.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_match', to='futsal.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner_matches', to='futsal.team'),
        ),
        migrations.AddField(
            model_name='gamemanager',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futsal.post'),
        ),
        migrations.AddField(
            model_name='coordinator',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futsal.post'),
        ),
    ]
