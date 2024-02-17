import psycopg2

from imagine_games_scraper.methods import postgres_store_methods
from imagine_games_scraper.items import article as Article
from imagine_games_scraper.items import video as Video
from imagine_games_scraper.items import user as User
from imagine_games_scraper.items import object as Object
from imagine_games_scraper.items import misc as Misc
from imagine_games_scraper.items import content as Content
from imagine_games_scraper.items import slideshow as Slideshow

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImagineGamesScraperPipeline:
    def process_item(self, item, spider):
        print('marker')
        print(type(item))
        return item

class PostgresStore:
    # Method used to retrieve settings from Scrapy project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Establish a connection to the Postgres database
        self.conn = psycopg2.connect(
            database = settings.get('POSTGRES_DATABASE'),
            user = settings.get('POSTGRES_ACCESS_USER'),
            password = settings.get('POSTGRES_ACCESS_PASSWORD'),
            host = settings.get('POSTGRES_HOST'),
            port = settings.get('POSTGRES_PORT')
        )

    def open_spider(self, spider):
        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        # Close cursor & connection to database when the spider is closed
        self.cur.close()
        self.conn.close()

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
        elif isinstance(item, User.Author):
            self.store_author(item)
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
        elif isinstance(item, Object.ObjectConnection):
            self.store_object_connection(item)
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
        elif isinstance(item, Content.AttributeConnection):
            self.store_attribute_connection(item)
        elif isinstance(item, Content.Brand):
            self.store_brand(item)
        elif isinstance(item, Misc.Image):
            self.store_image(item)
        elif isinstance(item, Slideshow.Slideshow):
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
        # else:
        #     print(type(item))

        return item
# Last Here

PostgresStore.store_article = postgres_store_methods.store_article
PostgresStore.store_article_content = postgres_store_methods.store_article_content
PostgresStore.store_video = postgres_store_methods.store_video
PostgresStore.store_video_metadata = postgres_store_methods.store_video_metadata
PostgresStore.store_video_asset = postgres_store_methods.store_video_asset
PostgresStore.store_user = postgres_store_methods.store_user
PostgresStore.store_author = postgres_store_methods.store_author
PostgresStore.store_contributor = postgres_store_methods.store_contributor
PostgresStore.store_official_review = postgres_store_methods.store_official_review
PostgresStore.store_user_review = postgres_store_methods.store_user_review
PostgresStore.store_user_review_tag = postgres_store_methods.store_user_review_tag
PostgresStore.store_object = postgres_store_methods.store_object
PostgresStore.store_object_connection = postgres_store_methods.store_object_connection
PostgresStore.store_object_region = postgres_store_methods.store_object_region
PostgresStore.store_region_release = postgres_store_methods.store_region_release
PostgresStore.store_region_rating = postgres_store_methods.store_region_rating
PostgresStore.store_how_long_to_beat = postgres_store_methods.store_how_long_to_beat
PostgresStore.store_object_wiki = postgres_store_methods.store_object_wiki
PostgresStore.store_wiki_navigation = postgres_store_methods.store_wiki_navigation
PostgresStore.store_map_object = postgres_store_methods.store_map_object
PostgresStore.store_map_item = postgres_store_methods.store_map_item
PostgresStore.store_content = postgres_store_methods.store_content
PostgresStore.store_content_category = postgres_store_methods.store_content_category
PostgresStore.store_typed_attribute = postgres_store_methods.store_typed_attribute
PostgresStore.store_attribute = postgres_store_methods.store_attribute
PostgresStore.store_attribute_connection = postgres_store_methods.store_attribute_connection
PostgresStore.store_brand = postgres_store_methods.store_brand
PostgresStore.store_image = postgres_store_methods.store_image
PostgresStore.store_catalog = postgres_store_methods.store_catalog
PostgresStore.store_poll = postgres_store_methods.store_poll
PostgresStore.store_poll_answer = postgres_store_methods.store_poll_answer
PostgresStore.store_poll_configuration = postgres_store_methods.store_poll_configuration
PostgresStore.store_commerce_deal = postgres_store_methods.store_commerce_deal
PostgresStore.store_gallery = postgres_store_methods.store_gallery
PostgresStore.store_image_connection = postgres_store_methods.store_image_connection
PostgresStore.store_slideshow = postgres_store_methods.store_slideshow