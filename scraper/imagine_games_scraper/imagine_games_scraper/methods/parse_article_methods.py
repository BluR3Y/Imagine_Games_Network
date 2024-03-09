import scrapy
import json
import re

from imagine_games_scraper.methods import html_methods
from imagine_games_scraper.items.article import Article, ArticleContent
from imagine_games_scraper.items.content import Content, ContentCategory, Brand, OfficialReview
from imagine_games_scraper.items.misc import Catalog, CommerceDeal, Poll, PollAnswer, PollConfiguration, DealConnection, Attribute, TypedAttribute
from imagine_games_scraper.items.media import Image, Slideshow
from imagine_games_scraper.items.user import User, Author
from imagine_games_scraper.items.object import Object
from imagine_games_scraper.items.video import Video
from imagine_games_scraper.items.wiki import WikiObject

def parse_article_page(self, response, article_item = None, recursion_level = 0):
    if article_item is None:
        article_item = Article()

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']

    modern_article_ref = apollo_state['ROOT_QUERY'].get(f"article({{\"slug\":\"{page_data.get('slug')}\"}})")
    modern_article_data = page_json_data['props']['apolloState'][modern_article_ref['__ref']]

    # ************************* Parse Modern Content *****************************
    modern_content_ref = modern_article_data.get('content')
    if modern_content_ref:
        modern_content_item = Content(referrers=[f"{article_item.__tablename__}:{article_item.get('id')}"])

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)
        article_item['content_id'] = { '__ref': f"{modern_content_item.__tablename__}:{modern_content_item.get('id')}" }

    # ************************* Parse Article Content *****************************
    article_content_data = modern_article_data.get('article')
    if article_content_data:
        article_content_item = ArticleContent(referrers=[f"{article_item.__tablename__}:{article_item.get('id')}"])

        yield from self.parse_article_content(page_json_data, article_content_data, article_content_item, recursion_level + 1)
        article_item['article_content_id'] = { '__ref': f"{article_content_item.__tablename__}:{article_content_item.get('id')}" }

    # ************************ Parse Article Review *****************************
    review_ref = page_data.get('review')
    if review_ref:
        review_data = apollo_state['Review:' + review_ref.get('id')]
        review_item = OfficialReview(referrers=[f"{article_item.__tablename__}:{article_item.get('id')}"])

        review_item['legacy_id'] = review_data.get('id')
        review_item['score'] = review_data.get('score')
        review_item['score_text'] = review_data.get('scoreText')
        review_item['editors_choice'] = review_data.get('editorsChoice')
        review_item['score_summary'] = review_data.get('scoreSummary')
        review_item['article_url'] = review_data.get('articleUrl')
        review_item['video_url'] = review_data.get('videoUrl')
        review_item['review_date'] = review_data.get('reviewedOn')

        yield review_item
        article_item['review_id'] = { '__ref': f"{review_item.__tablename__}:{review_item.get('id')}" }   

    # *********************** Scraping recommendation Content *******************************
    # if recursion_level < 1:
    #     recommendation_regex = re.compile(r"topPages\({.*}\)")
    #     recommendation_key = next((key for key in apollo_state['ROOT_QUERY'] if recommendation_regex.search(key)), None)
    #     if recommendation_key:
    #         for modern_article in (apollo_state[ref] for ref in (ref.get('__ref') for ref in apollo_state['ROOT_QUERY'][recommendation_key])):
    #             article_content = apollo_state[modern_article['content']['__ref']]
    #             yield scrapy.Request(url="https://www.ign.com" + article_content.get('url'), callback=self.parse_article_page, cb_kwargs={ 'recursion_level': recursion_level + 1 })

    yield article_item

def parse_poll(self, page_json_data, poll_item = None):
    if poll_item is None:
        poll_item = Poll()

    apollo_state = page_json_data['props']['apolloState']
    # poll_regex = re.compile(r"poll\({\"id\":\"%s\"}\)" % element.attributes.get('data-id'))
    poll_regex = re.compile(r"poll\({\"id\":\"%s\"}\)" % poll_item.get('legacy_id'))
    poll_root_key = next((key for key in apollo_state['ROOT_QUERY'] if poll_regex.search(key)), None)
    poll_data = apollo_state[apollo_state['ROOT_QUERY'][poll_root_key].get('__ref')]

    poll_item['voters'] = poll_data.get('voters')

    modern_content_ref = poll_data.get('content')
    if modern_content_ref:
        modern_content_item = Content(referrers=[f"{poll_item.__tablename__}:{poll_item.get('id')}"])

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), modern_content_item)
        poll_item['content_id'] = { '__ref': f"{modern_content_item.__tablename__}:{modern_content_item.get('id')}" }

    poll_config_ref = poll_data.get('config')
    if poll_config_ref:
        poll_config_item = PollConfiguration(referrers=[f"{poll_item.__tablename__}:{poll_item.get('id')}"])
        poll_config_item['require_authentication'] = poll_config_ref.get('requireAuthenticated')
        poll_config_item['require_authentication_for_results'] = poll_config_ref.get('requireAuthenticatedForResults')
        poll_config_item['multi_choice'] = poll_config_ref.get('multiChoice')
        poll_config_item['auto_display_results'] = poll_config_ref.get('autoDisplayResults')

        yield poll_config_item
        poll_item['configuration_id'] = { '__ref': f"{poll_config_item.__tablename__}:{poll_config_item.get('id')}" }

    for answer in [apollo_state[answer_ref.get('__ref')] for answer_ref in poll_data.get('answers')]:
        answer_item = PollAnswer()
        answer_item['legacy_id'] = answer.get('id')
        answer_item['answer'] = answer.get('answer')
        answer_item['votes'] = answer.get('votes')

        answer_item['poll_id'] = { '__ref': f"{poll_item.__tablename__}:{poll_item.get('id')}" }

        yield answer_item
        poll_item['referrers'].append(f"{answer_item.__tablename__}:{answer_item.get('id')}")

    poll_image_ref = poll_data.get('image')
    if poll_image_ref:
        image_item = Image(referrers=[f"{poll_item.__tablename__}:{poll_item.get('id')}"])
        image_item['legacy_url'] = poll_image_ref.get('url')

        yield image_item
        poll_item['image_id'] = { '__ref': f"{image_item.__tablename__}:{image_item.get('id')}" }
    yield poll_item

def parse_captioned_image(self, page_json_data, element, captioned_image_item = None):
    pass

def parse_commerce_deal(self, page_json_data, data_slug, catalog_item = None, recursion_level = 0):
    if catalog_item is None:
        catalog_item = Catalog()

    # Persisting issue: Some catalogs cannot be found in root_query; Temporary solution: In postgresStore handler
    apollo_state = page_json_data['props']['apolloState']
    deal_regex = re.compile(r"catalogBySlug\({\"slug\":\"%s\"}\)" % data_slug)

    deal_root_key = next((key for key in apollo_state['ROOT_QUERY'] if deal_regex.search(key)), None)
    deal_root_data = apollo_state['ROOT_QUERY'].get(deal_root_key, {})

    modern_content_ref = deal_root_data.get('content')
    if modern_content_ref:
        content_item = Content(referrers=[f"{catalog_item.__tablename__}:{catalog_item.get('id')}"])
        content_item['type'] = 'Catalog'
        content_item['slug'] = data_slug

        yield from self.parse_modern_content(page_json_data, modern_content_ref.get('__ref'), content_item)
        catalog_item['content_id'] = { '__ref': f"{content_item.__tablename__}:{content_item.get('id')}" }

    for deal in [apollo_state[deal_ref.get('__ref')] for deal_ref in deal_root_data.get('items', [])]:
        deal_connection_item = DealConnection()
        deal_connection_item['catalog_id'] = { '__ref': f"{catalog_item.__tablename__}:{catalog_item.get('id')}" }

        deal_item = CommerceDeal(referrers=[f"{deal_connection_item.__tablename__}:{deal_connection_item.get('id')}"])
        deal_item['legacy_id'] = deal.get('id')
        deal_item['url'] = deal.get('url')
        deal_item['title'] = deal.get('title')
        deal_item['description'] = deal.get('description')
        deal_item['brand'] = deal.get('brand')
        deal_item['model'] = deal.get('model')
        deal_item['vendor'] = deal.get('vendor')
        deal_item['price'] = deal.get('price')
        deal_item['msrp'] = deal.get('msrp')
        deal_item['discount'] = deal.get('discount')
        deal_item['coupon_code'] = deal.get('couponCode')
        deal_item['sponsor_disclosure'] = deal.get('sponsorDisclosure')
        deal_item['is_large'] = deal.get('large')
        deal_item['region_code'] = deal.get('regionCode')
        deal_item['up_votes'] = deal.get('upVotes')

        deal_image_ref = deal.get('image')
        if deal_image_ref:
            image_item = Image(referrers=[f"{deal_item.__tablename__}:{deal_item.get('id')}"])
            image_item['legacy_url'] = deal_image_ref.get('url')

            yield image_item
            deal_item['cover_id'] = { '__ref': f"{image_item.__tablename__}:{image_item.get('id')}" }

        yield deal_item
        deal_connection_item['deal_id'] = { '__ref': f"{deal_item.__tablename__}:{deal_item.get('id')}" }

        yield deal_connection_item
        catalog_item['referrers'].append(f"{deal_connection_item.__tablename__}:{deal_connection_item.get('id')}")

    yield catalog_item

def parse_article_content(self, page_json_data, article_content_data, article_content_item = None, recursion_level = 0):
    if article_content_item is None:
        article_content_item = ArticleContent()

    article_content_item['legacy_id'] = article_content_data.get('id')
    article_content_item['hero_video_content_id'] = article_content_data.get('heroVideoContentId')
    article_content_item['hero_video_content_slug'] = article_content_data.get('heroVideoContentSlug')

    html_object = html_methods.HTMLDocument(article_content_data.get('processedHtml'))
    parsed_html, parsed_content = parse_embedded_html_element(html_object.root_node)
    article_content_item['processed_html'] = parsed_html

    for content_item in parsed_content:
        item_data_transform = content_item['data_transform']

        if item_data_transform == 'slideshow':
            yield scrapy.Request(url="https://www.ign.com/slideshows/" + content_item.get("data_slug"), callback=self.parse_slideshow_page, cb_kwargs={ 'slideshow_item': content_item.get("item") })
        elif item_data_transform == 'ignvideo':
            yield scrapy.Request(url="https://www.ign.com/videos/" + content_item.get("data_slug"), callback=self.parse_video_page, cb_kwargs={ 'video_item': content_item.get("item"), 'recursion_level': recursion_level + 1 })
        elif item_data_transform == 'commerce-deal':
            yield from self.parse_commerce_deal(page_json_data, content_item.get('data_slug'), content_item.get('item'))
        elif item_data_transform == 'poll':
            yield from self.parse_poll(page_json_data, content_item.get('item'))
        # elif item_data_transform == 'image-with-caption':
        #     yield content_item.get("item")
        elif item_data_transform == 'ignobject':
            yield scrapy.Request(url=("https://www.ign.com/" + content_item.get('object_type') + '/' + content_item.get('data_slug')), callback=self.parse_object_page, cb_kwargs={ 'object_item': content_item.get('item'), 'recursion_level': recursion_level + 1 })
        # elif item_data_transform == 'ignwiki':
        #     yield scrapy.Request(url="https://www.ign.com/wikis/" + content_item.get("data_slug"), callback=self.parse_wiki_page, cb_kwargs={ 'wiki_item': content_item.get("item") })
        elif item_data_transform == 'ignarticle':
            yield scrapy.Request(url="https://www.ign.com/articles/" + content_item.get("data_slug"), callback=self.parse_article_page, cb_kwargs={ 'article_item': content_item.get("item"), 'recursion_level': recursion_level + 1 })

    yield article_content_item

def parse_embedded_html_element(element):
    parsed_content = []
    if 'data-transform' in element.attributes:
        data_transform = element.attributes.get('data-transform')

        if data_transform == 'slideshow':
            parsed_content.append({
                "item": Slideshow(),
                "data_transform": data_transform,
                "data_slug": element.attributes.get('data-slug')
            })
        elif data_transform == 'ignvideo':
            parsed_content.append({
                "item": Video(),
                "data_transform": data_transform,
                "data_slug": element.attributes.get('data-slug')
            })
        elif data_transform == 'commerce-deal':
            parsed_content.append({
                "item": Poll(),
                'data_transform': data_transform,
                'data_slug': element.attributes.get('data-slug')
            })
        elif data_transform == 'poll':
            poll_item = Poll()
            poll_item['legacy_id'] = element.attributes.pop('data-id')
            element.attributes['data-id'] = poll_item.get('id')

            parsed_content.append({
                "item": poll_item,
                "data_transform": data_transform
            })
        elif data_transform == 'image-with-caption':
            captioned_image_item = Image()
            captioned_image_item['legacy_url'] = element.attributes.pop('data-image-url')
            element.attributes.pop('data-image-title')
            element.attributes.pop('data-image-link')
            captioned_image_item['caption'] = element.attributes.pop('data-caption')

            element.attributes['data-id'] = captioned_image_item.get('id')

            parsed_content.append({
                "item": captioned_image_item,
                "data_transform": data_transform
            })
    elif element.tag == 'a' and 'href' in element.attributes and re.compile(r"https://www.ign.com/.*").search(element.attributes.get('href')):
        object_types = ['games','tech','movies','shows','comics']
        element_href = element.attributes.get('href')
        domain_len = len("https://www.ign.com/")
        data_transform, resource_path = element_href[domain_len:].split('/', 1)
        
        if data_transform in object_types:
            element.tag = "section"
            element.attributes['data-transform'] = 'ignobject'
            element.attributes['data-slug'] = resource_path
            parsed_content.append({
                "item": Object(),
                "data_transform": 'ignobject',
                "object_type": data_transform,
                "data_slug": resource_path
            })
        elif data_transform == 'wikis':
            element.tag = "section"
            element.attributes['data-transform'] = 'ignwiki'
            element.attributes['data-slug'] = resource_path
            parsed_content.append({
                "item": WikiObject(),
                "data_transform": 'ignwiki',
                "data_slug": resource_path
            })
        elif data_transform == 'articles':
            element.tag = "section"
            element.attributes['data-transform'] = 'ignarticle'
            element.attributes['data-slug'] = resource_path
            parsed_content.append({
                "item": Article(),
                "data_transform": 'ignarticle',
                "data_slug": resource_path
            })

    parsed_html = f"<{element.tag}"

    for key, value in element.attributes.items():
        parsed_html += f" {key}=\"{value}\""

    if not element.children and element.tag in html_methods.self_closing_elements:
        parsed_html += " />"
    else:
        parsed_html += '>'
        for child in element.children:
            if isinstance(child, html_methods.HTMLNode):
                child_parsed_html, child_parsed_content = parse_embedded_html_element(child)
                parsed_html += child_parsed_html
                parsed_content = [*parsed_content, *child_parsed_content]
            else:
                parsed_html += child
        parsed_html += f"</{element.tag}>"
    return parsed_html, parsed_content