import scrapy
from imagine_games_scraper.items import Article, Video


class ContentspiderSpider(scrapy.Spider):
    name = "contentSpider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com?endIndex=0"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'content_data.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    # Main parse function for the spider
    def parse(self, response):
        # Extracting content elements from the response
        page_content = response.css('div.content-item')

        # Iterate over each content element
        for content_item in page_content:
            # Construct absolute URL of the item
            item_url = 'https://www.ign.com' + content_item.css('a.item-body ::attr(href)').get()
            # Determine the appropriate callback function based on the type of content
            callback_function = self.parse_article_page if 'video' not in item_url else self.parse_video_page
            # Following the link to the content's page and calling parsing function
            yield scrapy.Request(url=item_url, callback=callback_function)
        
    # Parsing function for article pages
    def parse_article_page(self, response):
        # Creating an Article instance to store the scraped data
        article_item = Article({ 'url': response.url })

        # Populating the item fields with scraped data
        article_item['thumbnail'] = response.xpath("//meta[@property='og:image']/@content").get()
        article_item['headline'] = response.xpath("//h1[@data-cy='article-headline']/text()").get()
        article_item['sub_headline'] = response.xpath("//h2[@data-cy='article-sub-headline']/text()").get()
        article_item['reporter'] = response.xpath("//meta[@property='article:author']/@content").get()
        article_item['published_date'] = response.xpath("//meta[@property='article:published_time']/@content").get()
        article_item['modified_date'] = response.xpath("//meta[@property='article:modified_time']/@content").get()
        article_item['tags'] = response.xpath("//a[@data-cy='object-breadcrumb']/text()").getall()
        article_item['category'] = self.identify_category(response)

    # Parsing function for video pages
    def parse_video_page(self, response):
        pass

    # Potential Elements: meta:vertical, meta:tags, breadcrumbs, url

    # def identify_category(self, response):
    #     category_identifiers = (
    #         ['games', 'game'],
    #         ['movies', 'movie', 'film', 'theater'],
    #         ['tv', 'television', 'show', 'tv-show'],
    #         ['comics', 'comic', 'book'],
    #         ['tech', 'technology']
    #     )

    #     breadcrumb_elements = response.xpath("//a[@data-cy='object-breadcrumb']/@href").getall()
    #     breadcrumb_categories = []
    #     for crumb in breadcrumb_elements:
    #         breadcrumb_categories.append(crumb.split('/')[1])
    #     breadcrumb_category = self.breadcrumb_identification(breadcrumb_categories)

    #     vertical_identification = lambda value: value if value is not None and value != 'Entertainment' else None
    #     vertical_category = vertical_identification(response.xpath("//meta[@name='vertical']/@content").get())

    #     tag_categories = filter(lambda value : value != 'News' and value != 'Entertainment', response.xpath("//meta[@property='article:tag']/@content").getall())

    #     combined_categories = [breadcrumb_category, vertical_category, *tag_categories]

    def identify_category(self, response):
        breadcrumb_category_identification = lambda url : url.split('/')[1]
        breadcrumb_urls = response.xpath("//a[@data-cy='object-breadcrumb']/@href").getall()
        breadcrumb_categories = [breadcrumb_category_identification(url) for url in breadcrumb_urls]
        
        vertical_category_identification = lambda value: value if value is not None and value != 'Entertainment' else None
        vertical_category = vertical_category_identification(response.xpath("//meta[@name='vertical']/@content").get())

        tag_category_identification = lambda value : value != 'News' and value != 'Entertainment'
        tag_categories = response.xpath("//meta[@property='article:tag']/@content").getall()
        filtered_tag_categories = filter(tag_category_identification, tag_categories)

        combined_categories = [vertical_category, *breadcrumb_categories, *filtered_tag_categories]
        print(combined_categories)
        # Last Here

    def breadcrumb_identification(self, categories):
        if not categories:
            return None

        category_count = dict()

        # Count occurrences of each category
        for category in categories:
            # get method will return the value for key if it exists, else it will return 0
            category_count[category] = category_count.get(category, 0) + 1

        # Find the category with the maximum occurence
            # max function will compare every value in the dictionary using "lambda" function that returns the value associated with each key
        most_occuring_category = max(category_count, key=category_count.get)

        return most_occuring_category