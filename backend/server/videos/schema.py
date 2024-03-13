import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Video, VideoMetadata, VideoAsset, VideoCaption

class VideoType(DjangoObjectType):
    class Meta:
        model = Video
        fields = ("id", "legacy_id", "content_id", "metadata_id")

class VideoMetadataType(DjangoObjectType):
    class Meta:
        model = VideoMetadata
        fields = ("id", "chat_enabled", "description_html", "downloadable", "duration", "m3u_url")

class VideoAssetType(DjangoObjectType):
    class Meta:
        model = VideoAsset
        fields = ("id", "video_id", "legacy_url", "key", "width", "height", "fps")

class VideoCaptionType(DjangoObjectType):
    class Meta:
        model = VideoCaption
        fields = ("id", "video_id", "language", "text")

class Query(graphene.ObjectType):
    # all_videos = graphene.List(VideoType)

    # def resolve_all_videos(root, info):
    #     return Video.objects.filter(title="lol")

    all_videos = DjangoListField(VideoType)
    def resolve_all_videos(root, info):
        return Video.objects.all()

schema = graphene.Schema(query=Query)