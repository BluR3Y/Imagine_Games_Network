import scrapy
import json
import re

from . import html_methods
from imagine_games_scraper.items.article import Article, ArticleContent
from imagine_games_scraper.items.content import Content, ContentCategory, Attribute, TypedAttribute, Brand
from imagine_games_scraper.items.misc import Image, Catalog, CommerceDeal, Poll, PollAnswer, PollConfiguration
from imagine_games_scraper.items.user import User, Author, OfficialReview
from imagine_games_scraper.items.object import Object
from imagine_games_scraper.items.video import Video
from imagine_games_scraper.items.slideshow import Slideshow

@classmethod
def parse_article_page(self, response, article_item = Article(), recursion_level = 0):
    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_article_ref = apollo_state['ROOT_QUERY'].get(f"article({{\"slug\":\"{page_data.get('slug')}\"}})")
    modern_article_data = page_json_data['props']['apolloState'][modern_article_ref['__ref']]

    # ************************* Parse Modern Content *****************************
    # modern_content_ref = modern_article_data.get('content')
    # if modern_content_ref:
    #     modern_content_item = Content()
    #     yield self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)

    #     article_item['content'] = modern_content_item.get('id')

    # ************************* Parse Article Content *****************************
    article_content_data = modern_article_data.get('article')
    article_content_item = ArticleContent(article_content_data)
    article_item['article'] = article_content_item.get('id')

    yield article_content_item

    # ************************ Parse Article Review *****************************
    review_ref = page_data.get('review')
    if review_ref:
        review_item = OfficialReview(apollo_state['Review:' + review_ref.get('id')])
        article_item['review'] = review_item.get('id')

        yield review_item

    # *********************** Parse Article Embeds ******************************

    html_data = html_methods.HTML_DOCUMENT(modern_article_data['article'].get('processedHtml'))
    element_filter = lambda x : x.attributes.get('data-transform') is not None
    embedded_elements = filter(element_filter, html_data.get_elements_by_tag('section'))

    for element in embedded_elements:
        data_transform = element.attributes.get('data-transform')

        if data_transform == 'slideshow':
            slideshow_item = Slideshow()
            article_item['embeds']['slideshows'].append(slideshow_item.get('id'))
            
            # yield scrapy.Request(url="https://www.ign.com/slideshows/" + element.attributes.get('data-slug'), callback=self.parse_slideshow_page, cb_kwargs={ 'slideshow_item': slideshow_item, 'recursion_level': recursion_level })
        elif data_transform == 'poll':
            poll_item = Poll()
            article_item['embeds']['polls'].append(poll_item.get('id'))

            # yield from self.parse_poll(page_json_data, element, poll_item)
        elif data_transform == 'ignvideo':
            video_item = Video()
            article_item['embeds']['videos'].append(video_item.get('id'))

            # yield scrapy.Request(url="https://www.ign.com/videos/" + element.attributes.get('data-slug'), callback=self.parse_video_page, cb_kwargs={ 'video_item': video_item, 'recursion_level': recursion_level })
        elif data_transform == 'image-with-caption':
            captioned_image_item = Image()
            article_item['embeds']['captioned_images'].append(captioned_image_item.get('id'))

            yield from self.parse_captioned_image(page_json_data, element, captioned_image_item)
        elif data_transform == 'commerce-deal':
            commerce_item = Catalog()
            article_item['embeds']['commerce_deals'].append(commerce_item.get('id'))

            yield from self.parse_commerce_deal(page_json_data, element, commerce_item)
        # else: print(element)

    # *********************** Scraping recommendation Content *******************************
    if recursion_level < 1:
        recommendation_regex = re.compile(r"topPages\({.*}\)")
        recommendation_key = next((key for key in apollo_state['ROOT_QUERY'] if recommendation_regex.search(key)), None)
        recommendation_refs = [ref['__ref'] for ref in apollo_state['ROOT_QUERY'][recommendation_key]]

        for modern_article in [apollo_state[ref] for ref in recommendation_refs]:
            article_content = apollo_state[modern_article['content']['__ref']]
            yield scrapy.Request(url="https://www.ign.com" + article_content.get('url'), callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    yield article_item

@classmethod
def parse_poll(self, page_json_data, element, poll_item = Poll()):
    apollo_state = page_json_data['props']['apolloState']

    poll_regex = re.compile(r"poll\({\"id\":\"%s\"}\)" % element.attributes.get('data-id'))
    poll_root_key = next((key for key in apollo_state['ROOT_QUERY'] if poll_regex.search(key)), None)
    poll_data = apollo_state[apollo_state['ROOT_QUERY'][poll_root_key].get('__ref')]

    poll_item['voters'] = poll_data.get('voters')

    modern_content_ref = poll_data.get('content')
    if modern_content_ref:
        modern_content_item = Content(apollo_state[modern_content_ref.get('__ref')])
        poll_item['content'] = modern_content_item.get('id')

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)

    poll_config_ref = poll_data.get('config')
    if poll_config_ref:
        poll_config_item = PollConfiguration(poll_data.get('config'))
        poll_item['configuration'] = poll_config_item.get('id')

        yield poll_config_item

    for answer in [apollo_state[answer_ref.get('__ref')] for answer_ref in poll_data.get('answers')]:
        yield PollAnswer(answer, { 'poll_id': poll_item.get('id') })

    poll_image = poll_data.get('image')
    if poll_image:
        image_item = Image(poll_image)
        poll_item['image'] = image_item.get('id')
        
        yield image_item

    yield poll_item

@classmethod
def parse_captioned_image(self, page_json_data, element, captioned_image_item):

    yield captioned_image_item

@classmethod
def parse_commerce_deal(self, page_json_data, element, commerce_deal_item, recursion_level = 0):
    apollo_state = page_json_data['props']['apolloState']
    deal_regex = re.compile(r"catalogBySlug\({\"slug\":\"%s\"}\)" % element.attributes.get('data-slug'))

    deal_root_key = next((key for key in apollo_state['ROOT_QUERY'] if deal_regex.search(key)), None)
    deal_root_data = apollo_state['ROOT_QUERY'].get(deal_root_key)

    modern_content_ref = deal_root_data.get('content')
    if modern_content_ref:
        modern_content_item = Content(apollo_state[modern_content_ref.get('__ref')])
        commerce_deal_item['content'] = modern_content_item.get('id')

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item, recursion_level)

    for deal in [apollo_state[deal_ref.get('__ref')] for deal_ref in deal_root_data.get('items')]:
        deal_image = Image(deal.get('image'))
        deal_item = CommerceDeal(deal, { 'cover': deal_image.get('id') })
        commerce_deal_item['items'].append(deal_item.get('id'))

        yield deal_image
        yield deal_item

    yield commerce_deal_item