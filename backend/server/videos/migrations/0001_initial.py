# Generated by Django 5.0.3 on 2024-03-11 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('legacy_id', models.UUIDField(editable=False)),
                ('content_id', models.UUIDField(editable=False)),
                ('metadata_id', models.UUIDField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='VideoAsset',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('video_id', models.UUIDField(editable=False)),
                ('legacy_url', models.CharField(max_length=1024)),
                ('key', models.CharField(max_length=1024)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('fps', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoCaption',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('video_id', models.UUIDField(editable=False)),
                ('language', models.CharField(max_length=128)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoMetadata',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('chat_enabled', models.BooleanField()),
                ('description_html', models.TextField()),
                ('downloadable', models.BooleanField()),
                ('duration', models.IntegerField()),
                ('m3u_url', models.CharField(max_length=512)),
            ],
        ),
    ]
