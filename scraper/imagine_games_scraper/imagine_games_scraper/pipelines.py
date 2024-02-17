import psycopg2

from imagine_games_scraper.items import article as Article
from imagine_games_scraper.items import video as Video
from imagine_games_scraper.items import user as User
from imagine_games_scraper.items import object as Object
from imagine_games_scraper.items import misc as Misc
from imagine_games_scraper.items import content as Content
from imagine_games_scraper.items import wiki as Wiki

from imagine_games_scraper.postgres import store_articles as ArticleStore
from imagine_games_scraper.postgres import store_content as ContentStore
from imagine_games_scraper.postgres import store_misc as MiscStore
from imagine_games_scraper.postgres import store_objects as ObjectStore
from imagine_games_scraper.postgres import store_users as UserStore
from imagine_games_scraper.postgres import store_videos as VideoStore
from imagine_games_scraper.postgres import store_wiki as WikiStore

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

        elif isinstance(item, Wiki.ObjectWiki):
            self.store_object_wiki(item)
        elif isinstance(item, Wiki.WikiNavigation):
            self.store_wiki_navigation(item)
        elif isinstance(item, Wiki.MapObject):
            self.store_map_object(item)
        elif isinstance(item, Wiki.Map):
            self.store_map_item(item)

        elif isinstance(item, Content.Content):
            self.store_content(item)
        elif isinstance(item, Content.Contributor):
            self.store_contributor(item)
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
        elif isinstance(item, Misc.Gallery):
            self.store_gallery(item)
        elif isinstance(item, Misc.Slideshow):
            self.store_slideshow(item)
        elif isinstance(item, Misc.ImageConnection):
            self.store_image_connection(item)
        elif isinstance(item, Misc.Catalog):
            self.store_catalog(item)
        elif isinstance(item, Misc.DealConnection):
            self.store_deal_connection(item)
        elif isinstance(item, Misc.CommerceDeal):
            self.store_commerce_deal(item)
        elif isinstance(item, Misc.Poll):
            self.store_poll(item)
        elif isinstance(item, Misc.PollAnswer):
            self.store_poll_answer(item)
        elif isinstance(item, Misc.PollConfiguration):
            self.store_poll_configuration(item)
        print('pipeline marker')
        return item

PostgresStore.store_article = ArticleStore.store_article
PostgresStore.store_article_content = ArticleStore.store_article_content

PostgresStore.store_video = VideoStore.store_vide
PostgresStore.store_video_metadata = VideoStore.store_video_metadata
PostgresStore.store_video_asset = VideoStore.store_video_asset

PostgresStore.store_user = UserStore.store_user
PostgresStore.store_author = UserStore.store_author
PostgresStore.store_official_review = UserStore.store_official_review
PostgresStore.store_user_review = UserStore.store_user_review
PostgresStore.store_user_review_tag = UserStore.store_user_review_tag

PostgresStore.store_object = ObjectStore.store_object
PostgresStore.store_object_connection = ObjectStore.store_object_connection
PostgresStore.store_object_region = ObjectStore.store_object_region
PostgresStore.store_region_release = ObjectStore.store_region_release
PostgresStore.store_region_rating = ObjectStore.store_region_rating
PostgresStore.store_how_long_to_beat = ObjectStore.store_how_long_to_beat

PostgresStore.store_object_wiki = WikiStore.store_object_wiki
PostgresStore.store_wiki_navigation = WikiStore.store_wiki_navigation
PostgresStore.store_map_object = WikiStore.store_map_object
PostgresStore.store_map_item = WikiStore.store_map_item

PostgresStore.store_content = ContentStore.store_content
PostgresStore.store_contributor = ContentStore.store_contributor
PostgresStore.store_content_category = ContentStore.store_content_category
PostgresStore.store_typed_attribute = ContentStore.store_typed_attribute
PostgresStore.store_attribute = ContentStore.store_attribute
PostgresStore.store_attribute_connection = ContentStore.store_attribute_connection
PostgresStore.store_brand = ContentStore.store_brand

PostgresStore.store_image = MiscStore.store_image
PostgresStore.store_gallery = MiscStore.store_gallery
PostgresStore.store_slideshow = MiscStore.store_slideshow
PostgresStore.store_image_connection = MiscStore.store_image_connection
PostgresStore.store_catalog = MiscStore.store_catalog
PostgresStore.store_deal_connection = MiscStore.store_deal_connection
PostgresStore.store_commerce_deal = MiscStore.store_commerce_deal
PostgresStore.store_poll = MiscStore.store_poll
PostgresStore.store_poll_answer = MiscStore.store_poll_answer
PostgresStore.store_poll_configuration = MiscStore.store_poll_configuration