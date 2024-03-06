from imagine_games_scraper.queue import activeQueue
import json

from imagine_games_scraper.items.article import Article, ArticleContent
from imagine_games_scraper.items.content import Content, Brand, ContentCategory, ObjectConnection, Contributor, ContentAttributeConnection, OfficialReview, UserReview, TagObject, ReviewTag
from imagine_games_scraper.items.media import Gallery, Image, ImageConnection
from imagine_games_scraper.items.misc import Attribute, TypedAttribute, PollConfiguration, Poll, PollAnswer, Catalog, CommerceDeal, DealConnection
from imagine_games_scraper.items.object import Object, ObjectAttributeConnection, HowLongToBeat, AgeRating, Region, Release, AgeRatingDescriptor, AgeRatingInteractiveElement, ReleasePlatformAttribute
from imagine_games_scraper.items.user import User, Author, UserConfiguration
from imagine_games_scraper.items.video import Video, VideoMetadata, VideoAsset, VideoCaption
from imagine_games_scraper.items.wiki import WikiObject, WikiNavigation, MapObject, Map

# Missing items: Slideshow

high_priority = [ArticleContent, Brand, ContentCategory, Image, Gallery, Attribute, User, OfficialReview, TagObject, TypedAttribute, PollConfiguration, CommerceDeal, HowLongToBeat, AgeRating, Release, VideoMetadata, VideoMetadata]
medium_priority = [Content, UserReview, ReviewTag, ImageConnection, Poll, PollAnswer, Catalog, Region, AgeRatingDescriptor, AgeRatingInteractiveElement, ReleasePlatformAttribute, Author, UserConfiguration]
low_priority = [Article, Video, WikiObject, Contributor, ObjectConnection, ContentAttributeConnection, DealConnection, Object, ObjectAttributeConnection, VideoCaption, VideoAsset]

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(item.to_dict())
        return item.to_dict()
    
# Pipeline used to enqueue scraped data to redis-based queue
class RedisQueue:

    def process_item(self, item, spider):
        obj_priority_and_delay = self.get_obj_priority(item)
        
        item_key = "%s:%s" % (item.__tablename__, item.get('id'))

        dict_item = item.to_dict()

        json_item = json.dumps(dict_item)

        activeQueue.redis_connection.set(item_key, json_item)

        activeQueue.enqueue_task(item_key, obj_priority_and_delay[0], item.get('delay', obj_priority_and_delay[1]))

        return dict_item

    def get_obj_priority(self, item):
        for obj_type in high_priority:
            if type(item) == obj_type:
                return (0, 0)
        for obj_type in medium_priority:
            if type(item) == obj_type:
                return (1, 4)
        return (2, 8)