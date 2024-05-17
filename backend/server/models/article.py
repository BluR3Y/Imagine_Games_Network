from django.db import models

class Article(models.Model):
    id = models.UUIDField()
    legacy_id = models.UUIDField()
    content_id = models.UUIDField()
    article_content_id = models.UUIDField()
    review_id = models.UUIDField()

class ArticleContent(models.Model):
    id = models.UUIDField()
    legacy_id = models.UUIDField()
    hero_video_content_id = models.UUIDField()
    hero_video_content_slug = models.CharField(max_length=64)
    processed_html = models.TextField()