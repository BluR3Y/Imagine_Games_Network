import pymongo
import urllib.parse

from imagine_games_scraper.methods import mongo_store_methods
from imagine_games_scraper.items import article as Article
from imagine_games_scraper.items import video as Video
from imagine_games_scraper.items import user as User
from imagine_games_scraper.items import object as Object
from imagine_games_scraper.items import misc as Misc
from imagine_games_scraper.items import content as Content

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, Article.Article):
            print('****** Article ******')
        elif isinstance(item, Video.Video):
            print('******* Video *******')
        elif isinstance(item, User.Contributor):
            print('******* Contributor *******')
        elif isinstance(item, Object.Object):
            print('********** Object ***************')
        else: print(f'******** {type(item)} ************')
        return item

class MongoStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Establish a connection to the MongoDB database
        self.mongo_uri = f"mongodb://{settings.get('MONGO_USER')}:{urllib.parse.quote_plus(settings.get('MONGO_PASSWORD'))}@{settings.get('MONGO_HOST')}:{settings.get('MONGO_PORT')}/{settings.get('MONGO_DATABASE')}"
        self.mongo_db = settings.get('MONGO_DATABASE')

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # Close connection to database when the spider is closed
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Article.Article):
            self.store_article(item)
        elif isinstance(item, Article.ArticleContent):
            self.store_article_content(item)
        elif isinstance(item, Video.Video):
            self.store_video(item)
        elif isinstance(item, Video.VideoMetadata):
            self.store_video_metadata(item)
        elif isinstance(item, Video.VideoAsset):
            self.store_video_asset(item)
        elif isinstance(item, User.User):
            self.store_user(item)
        elif isinstance(item, User.Contributor):
            self.store_contributor(item)
        elif isinstance(item, User.OfficialReview):
            self.store_official_review(item)
        elif isinstance(item, User.UserReview):
            self.store_user_review(item)
        elif isinstance(item, User.UserReviewTag):
            self.store_user_review_tag(item)
        elif isinstance(item, Object.Object):
            self.store_object(item)
        elif isinstance(item, Object.Region):
            self.store_object_region(item)
        elif isinstance(item, Object.Release):
            self.store_region_release(item)
        elif isinstance(item, Object.Rating):
            self.store_region_rating(item)
        elif isinstance(item, Object.HowLongToBeat):
            self.store_how_long_to_beat(item)
        elif isinstance(item, Object.ObjectWiki):
            self.store_object_wiki(item)
        elif isinstance(item, Object.WikiNavigation):
            self.store_wiki_navigation(item)
        elif isinstance(item, Object.MapObject):
            self.store_map_object(item)
        elif isinstance(item, Object.Map):
            self.store_map_item(item)
        elif isinstance(item, Content.Content):
            self.store_content(item)
        elif isinstance(item, Content.ContentCategory):
            self.store_content_category(item)
        elif isinstance(item, Content.TypedAttribute):
            self.store_typed_attribute(item)
        elif isinstance(item, Content.Attribute):
            self.store_attribute(item)
        elif isinstance(item, Content.Brand):
            self.store_brand(item)
        elif isinstance(item, Misc.Image):
            self.store_image(item)
        elif isinstance(item, Misc.Slideshow):
            self.store_slideshow(item)
        elif isinstance(item, Misc.Catalog):
            self.store_catalog(item)
        elif isinstance(item, Misc.Poll):
            self.store_poll(item)
        elif isinstance(item, Misc.PollAnswer):
            self.store_poll_answer(item)
        elif isinstance(item, Misc.PollConfiguration):
            self.store_poll_configuration(item)
        elif isinstance(item, Misc.CommerceDeal):
            self.store_commerce_deal(item)
        else:
            print(type(item))

        return item

MongoStore.store_article = mongo_store_methods.store_article
MongoStore.store_article_content = mongo_store_methods.store_article_content
MongoStore.store_video = mongo_store_methods.store_video
MongoStore.store_video_metadata = mongo_store_methods.store_video_metadata
MongoStore.store_video_asset = mongo_store_methods.store_video_asset
MongoStore.store_user = mongo_store_methods.store_user
MongoStore.store_contributor = mongo_store_methods.store_contributor
MongoStore.store_official_review = mongo_store_methods.store_official_review
MongoStore.store_user_review = mongo_store_methods.store_user_review
MongoStore.store_user_review_tag = mongo_store_methods.store_user_review_tag
MongoStore.store_object = mongo_store_methods.store_object
MongoStore.store_object_region = mongo_store_methods.store_object_region
MongoStore.store_region_release = mongo_store_methods.store_region_release
MongoStore.store_region_rating = mongo_store_methods.store_region_rating
MongoStore.store_how_long_to_beat = mongo_store_methods.store_how_long_to_beat
MongoStore.store_object_wiki = mongo_store_methods.store_object_wiki
MongoStore.store_wiki_navigation = mongo_store_methods.store_wiki_navigation
MongoStore.store_map_object = mongo_store_methods.store_map_object
MongoStore.store_map_item = mongo_store_methods.store_map_item
MongoStore.store_content = mongo_store_methods.store_content
MongoStore.store_content_category = mongo_store_methods.store_content_category
MongoStore.store_typed_attribute = mongo_store_methods.store_typed_attribute
MongoStore.store_attribute = mongo_store_methods.store_attribute
MongoStore.store_brand = mongo_store_methods.store_brand
MongoStore.store_image = mongo_store_methods.store_image
MongoStore.store_slideshow = mongo_store_methods.store_slideshow
MongoStore.store_catalog = mongo_store_methods.store_catalog
MongoStore.store_poll = mongo_store_methods.store_poll
MongoStore.store_poll_answer = mongo_store_methods.store_poll_answer
MongoStore.store_poll_configuration = mongo_store_methods.store_poll_configuration
MongoStore.store_commerce_deal = mongo_store_methods.store_commerce_deal