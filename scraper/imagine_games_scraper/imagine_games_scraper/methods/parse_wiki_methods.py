import scrapy
import json
import re

from imagine_games_scraper.items.object import ObjectWiki

@classmethod
def parse_wiki_page(self, response, wiki_item = ObjectWiki, recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    with open('scraping_wiki_data.json', 'w') as json_file:
        json.dump(page_json_data, json_file)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']