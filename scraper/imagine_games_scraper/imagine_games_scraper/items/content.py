import scrapy
from imagine_games_scraper.items.base_item import Item

class Content(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()
    type = scrapy.Field()
    vertical = scrapy.Field()
    header_image_id = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    feed_title = scrapy.Field()
    feed_image_id = scrapy.Field()
    primary_object_id = scrapy.Field()
    excerpt = scrapy.Field()
    description = scrapy.Field()
    state = scrapy.Field()
    publish_date = scrapy.Field()
    modify_date = scrapy.Field()
    events = scrapy.Field()
    brand_id = scrapy.Field()
    category_id = scrapy.Field()

    __tablename__ = "contents"

    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)

        


class Brand(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    slug = scrapy.Field()
    name = scrapy.Field()
    logo_light = scrapy.Field()
    logo_dark = scrapy.Field()

    __tablename__ = "brands"

    def __init__(self, *args, **kwargs):
        super(Brand, self).__init__(*args, **kwargs)

        



class ContentCategory(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()

    __tablename__ = "content_categories"

    def __init__(self, *args, **kwargs):
        super(ContentCategory, self).__init__(*args, **kwargs)

        

class ObjectConnection(Item):
    id = scrapy.Field()
    content_id = scrapy.Field()
    object_id = scrapy.Field()

    __tablename__ = "object_connections"

    def __init__(self, *args, **kwargs):
        super(ObjectConnection, self).__init__(*args, **kwargs)

        

class Contributor(Item):
    id = scrapy.Field()
    content_id = scrapy.Field()
    user_id = scrapy.Field()

    __tablename__ = "contributors"

    def __init__(self, *args, **kwargs):
        super(Contributor, self).__init__(*args, **kwargs)

        

class ContentAttributeConnection(Item):
    id = scrapy.Field()
    content_id = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = "content_attribute_connections"

    def __init__(self, *args, **kwargs):
        super(ContentAttributeConnection, self).__init__(*args, **kwargs)

        


class OfficialReview(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    score = scrapy.Field()
    score_text = scrapy.Field()
    editors_choice = scrapy.Field()
    score_summary = scrapy.Field()
    article_url = scrapy.Field()
    video_url = scrapy.Field()
    review_date = scrapy.Field()

    __tablename__ = 'official_reviews'

    def __init__(self, *args, **kwargs):
        super(OfficialReview, self).__init__(*args, **kwargs)

        



class UserReview(Item):
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
    platform_id = scrapy.Field()

    __tablename__ = 'user_reviews'

    def __init__(self, *args, **kwargs):
        super(UserReview, self).__init__(*args, **kwargs)

        

# class TagObject(Item):
#     id = scrapy.Field()
#     legacy_id = scrapy.Field()
#     name = scrapy.Field()

#     __tablename__ = 'tag_objects'

#     def __init__(self, *args, **kwargs):
#         super(TagObject, self).__init__(*args, **kwargs)

        

class ReviewTag(Item):
    id = scrapy.Field()
    review_id = scrapy.Field()
    is_positive = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'review_tags'

    def __init__(self, *args, **kwargs):
        super(ReviewTag, self).__init__(*args, **kwargs)

        