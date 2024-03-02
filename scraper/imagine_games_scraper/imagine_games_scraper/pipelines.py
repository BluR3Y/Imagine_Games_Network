from imagine_games_scraper.alchemy.models.article import Article, ArticleContent
from imagine_games_scraper.alchemy.models.content import Content, Brand, ContentCategory, ObjectConnection, Contributor, ContentAttributeConnection, Slideshow, OfficialReview, UserReview, TagObject, ReviewTag
from imagine_games_scraper.alchemy.models.media import Gallery, Image, ImageConnection
from imagine_games_scraper.alchemy.models.misc import Attribute, TypedAttribute, PollConfiguration, Poll, PollAnswer, Catalog, CommerceDeal, DealConnection
from imagine_games_scraper.alchemy.models.object import Object, ObjectAttributeConnection, HowLongToBeat, AgeRating, Region, Release, AgeRatingDescriptor, AgeRatingInteractiveElement, ReleasePlatformAttribute
from imagine_games_scraper.alchemy.models.user import User, Author, UserConfiguration
from imagine_games_scraper.alchemy.models.video import Video, VideoMetadata, VideoAsset, VideoCaption
from imagine_games_scraper.alchemy.models.wiki import WikiObject, WikiNavigation, MapObject, Map

high_priority = [ArticleContent, Brand, ContentCategory, Image, Gallery, Attribute, User, OfficialReview, TagObject, TypedAttribute, PollConfiguration, CommerceDeal, HowLongToBeat, AgeRating, Release, VideoMetadata, VideoMetadata]
medium_priority = [Content, UserReview, ReviewTag, ImageConnection, Poll, PollAnswer, Catalog, Region, AgeRatingDescriptor, AgeRatingInteractiveElement, ReleasePlatformAttribute, Author, UserConfiguration]
low_priority = [Article, Video, WikiObject, Contributor, ObjectConnection, ContentAttributeConnection, Slideshow, DealConnection, Object, ObjectAttributeConnection, VideoCaption, VideoAsset]

class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print(dict(item))
        return item
    
# Pipeline used to enqueue scraped data to redis-based queue
class RedisQueue:
    def process_item(self, item, spider):
        obj_priority_and_delay = self.get_obj_priority(item)
        spider.enqueue_task(item.get('obj'), obj_priority_and_delay[0], item.get('delay', obj_priority_and_delay[1]))
        
        return item
    
    def get_obj_priority(self, item):
        for obj_type in high_priority:
            if type(item) == obj_type:
                return (0, 0)
        for obj_type in medium_priority:
            if type(item) == obj_type:
                return (1, 4)
        return (2, 8)