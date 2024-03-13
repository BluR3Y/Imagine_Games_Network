from django.db import models

class Video(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    legacy_id = models.UUIDField(primary_key=False, editable=False)
    content_id = models.UUIDField(primary_key=False, editable=False)
    metadata_id = models.UUIDField(primary_key=False, editable=False)

class VideoMetadata(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    chat_enabled = models.BooleanField()
    description_html = models.TextField()
    downloadable = models.BooleanField()
    duration = models.IntegerField()
    m3u_url = models.CharField(max_length=512)

class VideoAsset(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    video_id = models.UUIDField(primary_key=False, editable=False)
    legacy_url = models.CharField(max_length=1024)
    key = models.CharField(max_length=1024)
    width = models.IntegerField()
    height = models.IntegerField()
    fps = models.IntegerField()

class VideoCaption(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    video_id = models.UUIDField(primary_key=False, editable=False)
    language = models.CharField(max_length=128)
    text = models.TextField()

# -- Video Asset
# CREATE TABLE video_assets (
#     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
#     video_id UUID NOT NULL,
#     legacy_url VARCHAR(1024),
#     key VARCHAR(1024),
#     width INT,
#     height INT,
#     fps INT,

#     FOREIGN KEY (video_id) REFERENCES videos (id)
# );

# -- Video Caption
# CREATE TABLE video_captions (
#     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
#     metadata_id UUID NOT NULL,

#     language VARCHAR(128),
#     text TEXT,

#     FOREIGN KEY (metadata_id) REFERENCES video_metadatas (id)
# );