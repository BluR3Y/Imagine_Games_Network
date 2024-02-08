import scrapy

class User(scrapy.Item):
    legacy_id = scrapy.Field()
    avatar = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()
    privacy = scrapy.Field()
    reporter_metadata = scrapy.Field()

    def __init__(self, user_data = {}, manual_assignments = {}, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
        self['legacy_id'] = manual_assignments.get('id', user_data.get('id', None))
        self['avatar'] = manual_assignments.get('avatar', user_data.get('avatarImageUrl', None))
        self['name'] = manual_assignments.get('name', user_data.get('name', None))
        self['nickname'] = manual_assignments.get('nickname', user_data.get('nickname', None))
        self['privacy'] = manual_assignments.get('privacy', (user_data['playlistSettings'].get('privacy') if user_data.get('playlistSettings', None) else "Private"))
        self['reporter_metadata'] = manual_assignments.get('reporter_metadata', None)
        
class Reporter(scrapy.Item):
    legacy_id = scrapy.Field()
    legacy_author_id = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    position = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    socials = scrapy.Field()

    def __init__(self, reporter_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Reporter, self).__init__(*args, **kwargs)
        
        self['legacy_id'] = manual_assignments.get('id', reporter_data.get('id', None))
        self['legacy_author_id'] = manual_assignments.get('authorId', reporter_data.get('authorId', None))
        self['url'] = manual_assignments.get('url', reporter_data.get('url', None))
        self['cover'] = manual_assignments.get('backgroundImageUrl', reporter_data.get('backgroundImageUrl', None))
        self['position'] = manual_assignments.get('position', reporter_data.get('position', None))
        self['bio'] = manual_assignments.get('bio', reporter_data.get('bio', None))
        self['location'] = manual_assignments.get('location', reporter_data.get('location', None))
        self['socials'] = manual_assignments.get('socials', reporter_data.get('socials', None))

class ReporterReview(scrapy.Item):
    legacy_id = scrapy.Field()
    score = scrapy.Field()
    score_text = scrapy.Field()
    editors_choice = scrapy.Field()
    score_summary = scrapy.Field()
    article_url = scrapy.Field()
    video_url = scrapy.Field()
    review_date = scrapy.Field()

    def __init__(self, review_data = {}, manual_assignments = {}, *args, **kwargs):
        super(ReporterReview, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', review_data.get('id', None))
        self['score'] = manual_assignments.get('score', review_data.get('score', None))
        self['score_text'] = manual_assignments.get('scoreText', review_data.get('scoreText', None))
        self['editors_choice'] = manual_assignments.get('editorsChoice', review_data.get('editorsChoice', None))
        self['score_summary'] = manual_assignments.get('scoreSummary', review_data.get('scoreSummary', None))
        self['article_url'] = manual_assignments.get('articleUrl', review_data.get('articleUrl', None))
        self['video_url'] = manual_assignments.get('videoUrl', review_data.get('videoUrl', None))
        self['review_date'] = manual_assignments.get('reviewedOn', review_data.get('reviewedOn', None))

class UserReview(scrapy.Item):
    legacy_id = scrapy.Field()
    legacy_user_id = scrapy.Field()
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
    # object_metadata = scrapy.Field()
    # user_metadata = scrapy.Field()
    # platform_metadata = scrapy.Field()

    def __init__(self, review_data = None, manual_assignments = {}, *args, **kwargs):
        super(UserReview, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', review_data.get('id', None))
        self['legacy_user_id'] = manual_assignments.get('userId', review_data.get('userId', None))
        self['legacy_object_id'] = manual_assignments.get('objectId', review_data.get('objectId', None))
        self['is_liked'] = manual_assignments.get('liked', review_data.get('liked', None))
        self['score'] = manual_assignments.get('score', review_data.get('score', None))
        self['text'] = manual_assignments.get('text', review_data.get('text', None))
        self['is_spoiler'] = manual_assignments.get('isSpoiler', review_data.get('isSpoiler', None))
        self['is_private'] = manual_assignments.get('isPrivate', review_data.get('isPrivate', None))
        self['publish_date'] = manual_assignments.get('createdAt', review_data.get('createdAt', None))
        self['modify_date'] = manual_assignments.get('updatedAt', review_data.get('updatedAt', None))   
        self['tags'] = manual_assignments.get('tags', None)     

class UserReviewTag(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    is_positive = scrapy.Field()

    def __init__(self, tag_data = {}, manual_assignments = {}, *args, **kwargs):
        super(UserReviewTag, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', tag_data.get('id', None))
        self['name'] = manual_assignments.get('name', tag_data.get('name', None))
        self['is_positive'] = manual_assignments.get('isPositive', tag_data.get('isPositive', None))