import scrapy
import json
from imagine_games_scraper.items import Article

class ArticleSpiderSpider(scrapy.Spider):
    name = "article_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/news?endIndex=20"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'article_data.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
                'store_empty': False,
                'indent': 4
            }
        }
    }

    # ** Unfinished - Scrape Page Main content

    def start_requests(self):
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        yield scrapy.Request(url='https://www.ign.com/articles/the-last-of-us-part-2-review', callback=self.parse_article_page)

    def parse(self, response):
        # Extracting article content elements from the response
        article_content = response.xpath(
            # Search for a <div> element whose's class attribute contains "content-item"
            "//div[contains(@class, 'content-item')]" + 
            # From those previous elements, select those that have a child of type <a> with an href attribute that includes "/articles/"
            "/a[contains(@href, '/articles/')]" + 
            # From the previous elements, provide the ancestor element of type <div> whose class attribute contains 'content-item'
            "/ancestor::div[contains(@class, 'content-item')]"
        )

        # Iterate over each content element
        for article in article_content:
            article_uri = article.css('a.item-body ::attr(href)').get()
            article_url = 'https://www.ign.com' + article_uri

            # Following the link to the content's page and calling parsing function
            yield scrapy.Request(url=article_url, callback=self.parse_article_page, cb_kwargs={ 'recursion_level': 0 })

    def parse_article_page(self, response, recursion_level = 0):
        # Creating an Article item instance to store the scraped data
        article_item = Article({ 'url': response.url })

        page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
        page_json_data = json.loads(page_script_data)

        # For debugging issues with data extraction
        # with open('problematic_article.json', 'w') as f:
        #     json.dump(page_json_data, f)

        # Select page metadata from json object
        page_data = page_json_data['props']['pageProps']['page']
        article_item['legacy_id'] = page_data['id']
        article_item['cover'] = page_data['image']
        article_item['title'] = page_data['pageTitle']
        article_item['subtitle'] = page_data['subtitle']
        article_item['description'] = page_data['description']
        article_item['excerpt'] = page_data['excerpt']
        article_item['publish_date'] = page_data['publishDate']
        article_item['modify_date'] = page_data['schema']['dateModified']
        article_item['slug'] = page_data['slug']
        article_item['category'] = page_data['category']
        article_item['vertical'] = page_data['vertical']
        article_item['processedHtml'] = page_data['processedHtml']
        article_item['contributors'] = self.parse_article_contributors(page_json_data)
        article_item['objects'] = []

        review_data = page_data['review']
        article_item['review'] = None if review_data is None else {
            'legacy_id': review_data['id'],
            'score': review_data['score'],
            'score_text': review_data['scoreText'],
            'editors_choice': review_data['editorsChoice'],
            'score_summary': review_data['scoreSummary'],
            'verdict': review_data['verdict'],
            'review_date': review_data['reviewedOn']
        }

        for object_id in [object['id'] for object in page_data['objects']]:
            object_data = page_json_data['props']['apolloState'][f'Object:{object_id}']

            article_item['objects'].append({
                'legacy_id': object_data['id'],
                'url': object_data['url'],
                'slug': object_data['slug'],
                'type': object_data['type'],
                'names': {
                    'primary': object_data['metadata']['names']['name'],
                    'alt': object_data['metadata']['names']['alt'],
                    'short': object_data['metadata']['names']['short']
                },
                'descriptions': {
                    'long': object_data['metadata']['descriptions']['long'],
                    'short': object_data['metadata']['descriptions']['short']
                },
                'franchises': [{
                    'name': franchise['name'],
                    'slug': franchise['slug']
                } for franchise in object_data['franchises']],
                'genres': [{
                    'name': genre['name'],
                    'slug': genre['slug']
                } for genre in object_data['genres']],
                'features': [{
                    'name': feature['name'],
                    'slug': feature['slug']
                } for feature in object_data['features']],
                'producers': [{
                    'name': producer['name'],
                    'short_name': producer['shortName'],
                    'slug': producer['slug']
                } for producer in object_data['producers']],
                'publishers': [{
                    'name': publisher['name'],
                    'short_name': publisher['shortName'],
                    'slug': publisher['slug']
                } for publisher in object_data['publishers']]
            } )


        # Yielding the Article Item for further processing or storage
        # yield article_item

    def parse_article_contributors(self, page_json_data):
        parsed_contributors = []

        for contributor_id in [contributor['id'] for contributor in page_json_data['props']['pageProps']['page']['contributors']]:
            contributor_data = page_json_data['props']['apolloState'][f'Contributor:{contributor_id}']

            contributor_object = {
                'legacy_author_id': contributor_data['authorId'],
                'legacy_id': contributor_id,
                'thumbnail_url': contributor_data['thumbnailUrl'],
                'name': contributor_data['name'],
                'nickname': contributor_data['nickname']
            }
            
            # Extracts related reviews by contributor if article is a review
            feed_partial_key = 'contentFeed'
            feed_complete_key = next((key for key in contributor_data if feed_partial_key in key), None)
            if (feed_complete_key):
                feed_params_str = feed_complete_key[len(feed_partial_key) + 1:]
                contributor_object['recommendation_feed'] = {
                    **(json.loads(feed_params_str)),
                    'feed_items': []
                }

                for feed_key in [feed_key['__ref'] for feed_key in contributor_data[feed_complete_key]['feedItems']]:
                    feed_article_data = page_json_data['props']['apolloState'][feed_key]
                    feed_content_data = page_json_data['props']['apolloState'][f'ModernContent:{feed_article_data['content']['id']}']
                    feed_object_data = page_json_data['props']['apolloState'][feed_content_data['primaryObject']['__ref']]

                    parsed_feed_item = {
                        'url': feed_content_data['url'],
                        'slug': feed_content_data['slug'],
                        'legacy_id': feed_content_data['id'],
                        'type': feed_content_data['type'],
                        'cover': feed_content_data['feedImage']['url'],
                        'title': feed_content_data['title'],
                        'subtitle': feed_content_data['subtitle'],
                        'publish_date': feed_content_data['publishDate'],
                        'category': page_json_data['props']['apolloState'][feed_content_data['contentCategory']['__ref']]['name'],
                        'review': {
                            'score': feed_article_data['review']['score']
                        },
                        'primary_object': {
                            'legacy_id': feed_object_data['id'],
                            'url': feed_object_data['url'],
                            'slug': feed_object_data['slug'],
                            'type': feed_object_data['type'],
                            'names': {
                                'primary': feed_object_data['metadata']['names']['name'],
                                'alt': feed_object_data['metadata']['names']['alt'],
                                'short': feed_object_data['metadata']['names']['short']
                            },
                            'franchises': feed_object_data['franchises'],
                            'regions': self.parse_feed_regions(page_json_data, feed_object_data)
                        }
                    }                       

                    contributor_object['recommendation_feed']['feed_items'].append(parsed_feed_item)
            parsed_contributors.append(contributor_object)
        return parsed_contributors
    
    def parse_feed_regions(self, page_json_data, feed_object_data):
        parsed_regions = []
        region_partial_key = 'objectRegions('
        region_complete_key = next((key for key in feed_object_data if region_partial_key in key), None)

        if (region_complete_key):
            region_params_str = region_complete_key[len(region_partial_key):len(region_complete_key) - 1]
            region_params_json = json.loads(region_params_str)


        # Last Here

        return parsed_regions