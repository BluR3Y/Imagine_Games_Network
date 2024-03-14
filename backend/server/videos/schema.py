import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Video, VideoMetadata, VideoAsset, VideoCaption

class VideoMetadataType(DjangoObjectType):
    class Meta:
        model = VideoMetadata
        fields = ("id", "chat_enabled", "description_html", "downloadable", "duration", "m3u_url")

class VideoType(DjangoObjectType):
    class Meta:
        model = Video
        fields = ("id", "legacy_id", "content_id")

    metadata = graphene.Field(VideoMetadataType)
    def resolve_metadata(self, info):
        return self.metadata

class VideoAssetType(DjangoObjectType):
    class Meta:
        model = VideoAsset
        fields = ("id", "video_id", "legacy_url", "key", "width", "height", "fps")

class VideoCaptionType(DjangoObjectType):
    class Meta:
        model = VideoCaption
        fields = ("id", "video_id", "language", "text")

# class Query(graphene.ObjectType):
#     metadata = graphene.Field(VideoMetadataType, metadata_id=graphene)

#     videos = graphene.List(VideoType)
#     def resolve_videos(self, info, **kwargs):
#         return Video.objects.all()
        
class Query(graphene.ObjectType):
    videos = graphene.List(VideoType)
    video_assets = graphene.List(VideoAssetType)

    def resolve_videos(self, info, **kwargs):
        return Video.objects.prefetch_related('metadata').all()
    def resolve_video_assets(self, info, **kwargs):
        video_id = kwargs.get('video_id')
        if video_id:
            return VideoAsset.objects.filter(video_id=video_id)
        return VideoAsset.objects.all()

schema = graphene.Schema(query=Query)