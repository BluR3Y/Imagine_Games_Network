import scrapy
from imagine_games_scraper.items.base_item import Item

class User(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    avatar_id = scrapy.Field()
    name = scrapy.Field()
    nickname = scrapy.Field()

    __tablename__ = 'users'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        


class Author(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    user_id = scrapy.Field()
    url = scrapy.Field()
    cover_id = scrapy.Field()
    position = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    socials = scrapy.Field()

    __tablename__ = 'authors'

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)

        

class UserConfiguration(Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    privacy = scrapy.Field()

    __tablename__ = 'user_configurations'

    def __init__(self, *args, **kwargs):
        super(UserConfiguration, self).__init__(*args, **kwargs)

        
