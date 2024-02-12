import scrapy
from uuid import uuid4

class User(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    avatar = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()
    privacy = scrapy.Field()
    contributor = scrapy.Field() # id referencing Contributor

    def __init__(self, user_data = {}, manual_assignments = {}, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', user_data.get('id'))
        self['avatar'] = manual_assignments.get('avatar', user_data.get('avatarImageUrl'))
        self['name'] = manual_assignments.get('name', user_data.get('name'))
        self['nickname'] = manual_assignments.get('nickname', user_data.get('nickname'))
        self['privacy'] = manual_assignments.get('privacy', (user_data['playlistSettings'].get('privacy') if user_data.get('playlistSettings') else "Private"))
        self['contributor'] = manual_assignments.get('contributor')
        
class Author (scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    legacy_author_id = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    position = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    socials = scrapy.Field()

    def __init__(self, contributor_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        
        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', contributor_data.get('id'))
        self['legacy_author_id'] = manual_assignments.get('authorId', contributor_data.get('authorId'))
        self['url'] = manual_assignments.get('url', contributor_data.get('url'))
        self['cover'] = manual_assignments.get('backgroundImageUrl', contributor_data.get('backgroundImageUrl'))
        self['position'] = manual_assignments.get('position', contributor_data.get('position'))
        self['bio'] = manual_assignments.get('bio', contributor_data.get('bio'))
        self['location'] = manual_assignments.get('location', contributor_data.get('location'))
        self['socials'] = manual_assignments.get('socials', contributor_data.get('socials'))

class OfficialReview(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    score = scrapy.Field()
    score_text = scrapy.Field()
    editors_choice = scrapy.Field()
    score_summary = scrapy.Field()
    article_url = scrapy.Field()
    video_url = scrapy.Field()
    review_date = scrapy.Field()

    def __init__(self, review_data = {}, manual_assignments = {}, *args, **kwargs):
        super(OfficialReview, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', review_data.get('id'))
        self['score'] = manual_assignments.get('score', review_data.get('score'))
        self['score_text'] = manual_assignments.get('scoreText', review_data.get('scoreText'))
        self['editors_choice'] = manual_assignments.get('editorsChoice', review_data.get('editorsChoice'))
        self['score_summary'] = manual_assignments.get('scoreSummary', review_data.get('scoreSummary'))
        self['article_url'] = manual_assignments.get('articleUrl', review_data.get('articleUrl'))
        self['video_url'] = manual_assignments.get('videoUrl', review_data.get('videoUrl'))
        self['review_date'] = manual_assignments.get('reviewedOn', review_data.get('reviewedOn'))

class UserReview(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    user_id = scrapy.Field()
    legacy_user_id = scrapy.Field()
    object_id = scrapy.Field()
    legacy_object_id = scrapy.Field()
    is_liked = scrapy.Field()
    score = scrapy.Field()
    text = scrapy.Field()
    is_spoiler = scrapy.Field()
    is_private = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    tags = scrapy.Field()
    platform = scrapy.Field()

    def __init__(self, review_data = None, manual_assignments = {}, *args, **kwargs):
        super(UserReview, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', review_data.get('id'))
        self['user_id'] = manual_assignments.get('user_id')
        self['legacy_user_id'] = manual_assignments.get('legacy_user_id', review_data.get('userId'))
        self['object_id'] = manual_assignments.get('object_id')
        self['legacy_object_id'] = manual_assignments.get('objectId', review_data.get('objectId'))
        self['is_liked'] = manual_assignments.get('liked', review_data.get('liked'))
        self['score'] = manual_assignments.get('score', review_data.get('score'))
        self['text'] = manual_assignments.get('text', review_data.get('text'))
        self['is_spoiler'] = manual_assignments.get('isSpoiler', review_data.get('isSpoiler'))
        self['is_private'] = manual_assignments.get('isPrivate', review_data.get('isPrivate'))
        self['publish_date'] = manual_assignments.get('createdAt', review_data.get('createdAt'))
        self['modify_date'] = manual_assignments.get('updatedAt', review_data.get('updatedAt'))   
        self['platform'] = manual_assignments.get('platform', review_data.get('platform'))
        self['tags'] = manual_assignments.get('tags', [])     

class UserReviewTag(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    is_positive = scrapy.Field()

    def __init__(self, tag_data = {}, manual_assignments = {}, *args, **kwargs):
        super(UserReviewTag, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', tag_data.get('id'))
        self['name'] = manual_assignments.get('name', tag_data.get('name'))
        self['is_positive'] = manual_assignments.get('isPositive', tag_data.get('isPositive'))