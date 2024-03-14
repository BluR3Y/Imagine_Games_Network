from django.db import models

class VideoMetadata(models.Model):
    class Meta:
        db_table = 'video_metadatas'

    id = models.UUIDField(primary_key=True, editable=False)
    chat_enabled = models.BooleanField()
    description_html = models.TextField()
    downloadable = models.BooleanField()
    duration = models.IntegerField()
    m3u_url = models.CharField(max_length=512)

class Video(models.Model):
    class Meta:
        db_table = 'videos'

    id = models.UUIDField(primary_key=True, editable=False)
    legacy_id = models.UUIDField(primary_key=False, editable=False)
    content_id = models.UUIDField(primary_key=False, editable=False)
    # metadata_id = models.UUIDField(primary_key=False, editable=False)
    metadata = models.ForeignKey(VideoMetadata, related_name='videos', on_delete=models.CASCADE)

class VideoAsset(models.Model):
    class Meta:
        db_table = 'video_assets'

    id = models.UUIDField(primary_key=True, editable=False)
    video_id = models.UUIDField(primary_key=False, editable=False)
    legacy_url = models.CharField(max_length=1024)
    key = models.CharField(max_length=1024)
    width = models.IntegerField()
    height = models.IntegerField()
    fps = models.IntegerField()

class VideoCaption(models.Model):
    class Meta:
        db_table = 'video_captions'

    id = models.UUIDField(primary_key=True, editable=False)
    video_id = models.UUIDField(primary_key=False, editable=False)
    language = models.CharField(max_length=128)
    text = models.TextField()