import scrapy
from imagine_games_scraper.items import Article

class ArticleSpiderSpider(scrapy.Spider):
    name = "article_spider"
    allowed_domains = ["ign.com"]
    start_urls = ["https://ign.com/news?endIndex=0"]
    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'article_data': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    # ** Unfinished - Scrape Page Main content

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

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
            yield scrapy.Request(url=article_url, callback=self.parse_article_page)

    # Parsing function for article pages
    def parse_article_page(self, response):
        # Creating an Article instance to store the scraped data
        article_item = Article({ 'url': response.url })

        # Populating the item fields with scraped data
        article_item['thumbnail'] = response.xpath("//meta[@property='og:image']/@content").get()
        article_item['headline'] = response.xpath("//h1[@data-cy='article-headline']/text()").get()
        article_item['sub_headline'] = response.xpath("//h2[@data-cy='article-sub-headline']/text()").get()
        article_item['reporter_name'] = response.xpath("//meta[@property='article:author']/@content").get()
        article_item['reporter_avatar'] = response.css("div.author-thumb.profile-thumb img::attr(src)").get()
        article_item['published_date'] = response.xpath("//meta[@property='article:published_time']/@content").get()
        article_item['modified_date'] = response.xpath("//meta[@property='article:modified_time']/@content").get()
        article_item['tags'] = response.xpath("//a[@data-cy='object-breadcrumb']/text()").getall()
        article_item['category'] = self.identify_category(response)
        # Last Here
        print(article_item)

    def identify_category(self, response):
        
        breadcrumb_category_identification = lambda url : url.split('/')[1]
        # Extract all breadcrumb element links from the document
        breadcrumb_urls = response.xpath("//a[@data-cy='object-breadcrumb']/@href").getall()
        # Loop through every string in breadcrumb_urls and run the lambda function that will extract the category from the url and be stored in the list
        breadcrumb_categories = [breadcrumb_category_identification(url) for url in breadcrumb_urls]

        # Retrieve the value of the content attribute from a <meta> element whose's 'name' attribute is 'vertical'
        vertical_category = response.xpath("//meta[@name='vertical']/@content").get()
        # Run the closest_valid_category method which will return the closest valid category of a given string
        validated_vertical_category = self.closest_valid_category(vertical_category)

        # Retrieve the value of the content attribute from all the <meta> elements whose's 'property' attribute is 'article:tag'
        tag_categories = response.xpath("//meta[@property='article:tag']/@content").getall()
        # Loop through all the items in tag_categories and run the method closest_valid_category() passing the current looping item as an argument
            # The returned values will be stored in a list
        validated_tag_categories = [self.closest_valid_category(category) for category in tag_categories]
    
        # Store all the values that will be considered for category in a list 
            # Unpacking all the values from lists using the unpacking operator (*)
        combined_categories = [validated_vertical_category, *breadcrumb_categories, *validated_tag_categories]
        # Remove all items in combined_categories that are not string values or are instances of None
        filtered_categories = [category for category in combined_categories if category is not None and isinstance(category, str)]
        # category_counter is used to keep track of how many times each category is found in filtered_categories
        category_counter = dict()

        # Count occurrences of each category
        for category in filtered_categories:
            # get method will return the value for key if it exists, else it will return 0
            category_counter[category] = category_counter.get(category, 0) + 1

        # Find the category with the maximum occurence
            # max function will compare every value in the dictionary using "lambda" function that returns the value associated with each key
        most_occuring_category = max(category_counter, key=category_counter.get)

        return most_occuring_category

    def closest_valid_category(self, category):
        if category is None:
            return None

        game_platforms = ('pc', 'xbox', 'playstation', 'nintendo')
        movie_platforms = ('dvd', 'blu-ray')
        category_identifiers = [
            ['games', 'game', *game_platforms],
            ['movies', 'movie', 'film', 'theater', *movie_platforms],
            ['tv', 'television', 'show', 'tv-show', 'on-demand'],
            ['comics', 'comic', 'book'],
            ['tech', 'technology'],
            ['commerce']
        ]

        for row in category_identifiers:
            for row_item in row:
                if category.lower() in row_item:
                    return row[0]
        return None