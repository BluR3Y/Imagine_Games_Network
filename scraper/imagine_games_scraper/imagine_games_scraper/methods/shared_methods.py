import scrapy
import json
import re

from imagine_games_scraper.items.user import User, Author, UserConfiguration
from imagine_games_scraper.items.object import Object, Region, HowLongToBeat, Release, AgeRating, ObjectAttributeConnection, AgeRatingDescriptor, AgeRatingInteractiveElement, ReleasePlatformAttribute
from imagine_games_scraper.items.misc import Attribute, TypedAttribute
from imagine_games_scraper.items.content import ContentAttributeConnection, ObjectConnection, Contributor, Content, ContentCategory, Brand, UserReview, ReviewTag
from imagine_games_scraper.items.wiki import WikiObject
from imagine_games_scraper.items.media import Image, Gallery, ImageConnection

def parse_contributor_page(self, response, author_item = None, recursion_level = 0):
    if author_item is None:
        author_item = Author()

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    author_data = page_data['author']
    # Missing: Contributor related Articles

    author_item['legacy_id'] = author_data.get('authorId')
    author_url = author_data.get('profileUrl')
    author_item['url'] = author_url.replace("https://www.ign.com", "")
    author_item['position'] = author_data.get('position')
    author_item['bio'] = author_data.get('bio')
    author_item['location'] = author_data.get('location')
    author_socials = author_data.get('socials')
    if author_socials:
        author_item['socials'] = { '__static': "ARRAY%s::social_media_entry[]" % ([(social.get('platform'), social.get('username')) for social in author_socials]) }
    # author user's profile image is only accessible from contributor page
    cover_ref = author_data.get('backgroundImageUrl')
    if cover_ref:
        cover_image_item = Image(referrers=[f"{author_item.__tablename__}:{author_item.get('id')}"])
        cover_image_item['url'] = cover_ref

        yield cover_image_item
        author_item['cover_id'] = { '__ref': f"{cover_image_item.__tablename__}:{cover_image_item.get('id')}" }

    yield author_item

def parse_object_page(self, response, object_item = None, recursion_level = 0):
    if object_item is None:
        object_item = Object()

    page_script_data = response.xpath("//script[@id='__NEXT_DATA__' and @type='application/json']/text()").get()
    page_json_data = json.loads(page_script_data)

    page_data = page_json_data['props']['pageProps']['page']
    apollo_state = page_json_data['props']['apolloState']
    object_data = apollo_state["Object:" + page_data.get('id')]

    object_item['legacy_id'] = object_data.get('id')
    object_item['url'] = object_data.get('url')
    object_item['slug'] = object_data.get('slug')
    object_item['wiki_slug'] = object_data.get('wikiSlug')
    object_item['type'] = object_data.get('type')

    object_image_ref = object_data.get('primaryImage')
    if object_image_ref:
        object_cover_item = Image(referrers=[f"{object_item.__tablename__}:{object_item.get('id')}"])
        object_cover_item['url'] = object_image_ref.get('url')

        yield object_cover_item
        object_item['cover_id'] = { '__ref': f"{object_cover_item.__tablename__}:{object_cover_item.get('id')}" }

    hl2b_data = object_data.get('hl2bData')
    if hl2b_data:
        hl2b_item = HowLongToBeat(referrers=[f"{object_item.__tablename__}:{object_item.get('id')}"])
        hl2b_item['legacy_id'] = hl2b_data.get('id')
        hl2b_item['legacy_ign_object_id'] = hl2b_data.get('ign_object_id')
        hl2b_item['steam_id'] = hl2b_data.get('steam_id')
        hl2b_item['itch_id'] = hl2b_data.get('itch_id')
        hl2b_item['platforms'] = hl2b_data.get('platforms')
        hl2b_item['list'] = hl2b_data.get('list')
        hl2b_item['review'] = hl2b_data.get('review')
        hl2b_item['time'] = hl2b_data.get('time')
        
        yield hl2b_item
        object_item['how_long_to_beat_id'] = { '__ref': f"{hl2b_item.__tablename__}:{hl2b_item.get('id')}" }

    object_names = object_data['metadata'].get('names')
    if object_names:
        long = object_names.get('name')
        alt = object_names.get('alt')
        short = object_names.get('short')
        object_item['names'] = {
            '__static': "(%s,ARRAY%s::VARCHAR[],%s)::name_entry" % (("quote_literal('" + long.replace("'", "''") + "')" if long else 'null'),(alt if alt else []),("quote_literal('" + short.replace("'", "''") + "')" if short else 'null'))
        }

    object_descriptions = object_data['metadata'].get('descriptions')
    if object_descriptions:
        long = object_descriptions.get('long')
        short = object_descriptions.get('short')
        object_item['descriptions'] = {
            '__static': "(%s,%s)::description_entry" % (("quote_literal('" + long.replace("'", "''") + "')" if long else 'null'), ("quote_literal('" + short.replace("'", "''") + "')" if short else 'null'))
        }

    all_attributes = []
    all_attributes.extend([{
        'type': 'franchise',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('franchises')])
    all_attributes.extend([{
        'type': 'genre',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('genres')])
    all_attributes.extend([{
        'type': 'feature',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('features')])
    all_attributes.extend([{
        'type': 'producer',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('producers')])
    all_attributes.extend([{
        'type': 'publisher',
        'name': attr.get('name'),
        'short_name': attr.get('shortName'),
        'slug': attr.get('slug', attr.get('name').replace(' ', '-').lower())
    } for attr in object_data.get('publishers')])

    for attr in all_attributes:
        object_attribute_connection = ObjectAttributeConnection()
        object_attribute_connection['object_id'] = { '__ref': f"{object_item.__tablename__}:{object_item.get('id')}" }
        object_item['referrers'].append(f"{object_attribute_connection.__tablename__}:{object_attribute_connection.get('id')}")

        self.cursor.execute("""
            SELECT typed_attributes.id
            FROM typed_attributes
            INNER JOIN attributes
                ON typed_attributes.attribute_id = attributes.id
            WHERE typed_attributes.type = %s AND attributes.name = %s
            LIMIT 1                    
        """, (attr.get('type'), attr.get('name'),))
        existing_attribute = self.cursor.fetchone()
        if existing_attribute:
            object_attribute_connection['attribute_id'] = existing_attribute[0]
        else:
            typed_attribute_item = TypedAttribute(referrers=[f"{object_attribute_connection.__tablename__}:{object_attribute_connection.get('id')}"])
            typed_attribute_item['type'] = attr.get('type')

            attribute_item = Attribute(referrers=[f"{typed_attribute_item.__tablename__}:{typed_attribute_item.get('id')}"])
            attribute_item['name'] = attr.get('name')
            attribute_item['short_name'] = attr.get('short_name')
            attribute_item['slug'] = attr.get('slug')

            attribute_obj_search = (lambda obj, target : obj.get('name') == target)
            attribute_obj = next((apollo_state[key] for key in apollo_state.keys() if key.startswith('Attribute:') and attribute_obj_search(apollo_state[key], attr.get('name'))), None)
            if attribute_obj:
                attribute_item['legacy_id'] = attribute_obj.get('id')
                attribute_item['short_name'] = attribute_item['short_name'] or attribute_obj.get('shortName')
                attribute_item['slug'] = attribute_item['slug'] or attribute_obj.get('slug')

            yield attribute_item
            typed_attribute_item['attribute_id'] = { '__ref': f"{attribute_item.__tablename__}:{attribute_item.get('id')}" }

            yield typed_attribute_item
            object_attribute_connection['attribute_id'] = { '__ref': f"{typed_attribute_item.__tablename__}:{typed_attribute_item.get('id')}" }

        yield object_attribute_connection
        
    for region in [apollo_state[region_ref['__ref']] for region_ref in filter((lambda x : x.get('__ref') is not None), object_data.get('objectRegions'))]:
        region_item = Region()
        region_item['legacy_id'] = region.get('id')
        region_item['name'] = region.get('name')
        region_item['region'] = region.get('region')

        region_item['object_id'] = { '__ref': f"{object_item.__tablename__}:{object_item.get('id')}" }
        object_item['referrers'].append(f"{region_item.__tablename__}:{region_item.get('id')}")

        age_rating_ref = region.get('ageRating')
        if age_rating_ref:
            age_rating_data = apollo_state[age_rating_ref.get('__ref')]

            existing_age_rating = self.postgres_find_by_legacy_id(table=AgeRating.__tablename__, id=age_rating_data.get('id'), fields=['id'], only_first=True)
            if existing_age_rating:
                region_item['age_rating_id'] = existing_age_rating[0]
            else:
                age_rating_item = AgeRating(referrers=[f"{region_item.__tablename__}:{region_item.get('id')}"])
                age_rating_item['legacy_id'] = age_rating_data.get('id')
                age_rating_item['name'] = age_rating_data.get('name')
                age_rating_item['slug'] = age_rating_data.get('slug')
                age_rating_item['type'] = age_rating_data.get('ageRatingType')

                yield age_rating_item
                region_item['age_rating_id'] = { '__ref': f"{age_rating_item.__tablename__}:{age_rating_item.get('id')}" }
        
        for descriptor in region.get('ageRatingDescriptors'):
            descriptor_item = AgeRatingDescriptor()
            
            descriptor_item['region_id'] = { '__ref': f"{region_item.__tablename__}:{region_item.get('id')}" }
            region_item['referrers'].append(f"{descriptor_item.__tablename__}:{descriptor_item.get('id')}")

            self.cursor.execute("SELECT id FROM attributes WHERE name = %s LIMIT 1;", (descriptor.get('name'),))
            existing_attribute = self.cursor.fetchone()
            if existing_attribute:
                descriptor_item['attribute_id'] = existing_attribute[0]
            else:
                descriptor_attribute_item = Attribute(referrers=[f"{descriptor_item.__tablename__}:{descriptor_item.get('id')}"])
                descriptor_attribute_item['name'] = descriptor.get('name')
                yield descriptor_attribute_item
                
                descriptor_item['attribute_id'] = { '__ref': f"{descriptor_attribute_item.__tablename__}:{descriptor_attribute_item.get('id')}" }
            yield descriptor_item

        for element in region.get('interactiveElements'):
            element_item = AgeRatingInteractiveElement()

            element_item['region_id'] = { '__ref': f"{region_item.__tablename__}:{region_item.get('id')}" }
            region_item['referrers'].append(f"{element_item.__tablename__}:{element_item.get('id')}")

            self.cursor.execute("SELECT id FROM attributes WHERE name = %s LIMIT 1;", (element.get('name'),))
            existing_attribute = self.cursor.fetchone()
            if existing_attribute:
                element_item['attribute_id'] = existing_attribute[0]
            else:
                element_attribute_item = Attribute(referrers=[f"{element_item.__tablename__}:{element_item.get('id')}"])
                element_attribute_item['name'] = element.get('name')
                yield element_attribute_item

                element_item['attribute_id'] = { '__ref': f"{element_attribute_item.__tablename__}:{element_attribute_item.get('id')}" }
            yield element_item

        for release in [apollo_state[release_ref['__ref']] for release_ref in region.get('releases')]:
            release_item = Release()
            release_item['legacy_id'] = release.get('id')
            release_item['date'] = release.get('date')
            release_item['estimated_date'] = release.get('estimatedDate')
            release_item['time_frame_year'] = release.get('timeframeYear')

            for platform in [apollo_state[platform_ref['__ref']] for platform_ref in release.get('platformAttributes')]:
                platform_item = ReleasePlatformAttribute()

                platform_item['release_id'] = { '__ref': f"{release_item.__tablename__}:{release_item.get('id')}" }
                release_item['referrers'].append(f"{platform_item.__tablename__}:{platform_item.get('id')}")

                existing_platform = self.postgres_find_by_legacy_id(table=Attribute.__tablename__, id=platform.get('id'), fields=['id'], only_first=True)
                if existing_platform:
                    platform_item['attribute_id'] = existing_platform[0]
                else:
                    platform_attribute_item = Attribute(referrers=[f"{platform_item.__tablename__}:{platform_item.get('id')}"])
                    platform_attribute_item['legacy_id'] = platform.get('id')
                    platform_attribute_item['name'] = platform.get('name')
                    platform_attribute_item['slug'] = platform.get('slug')
                    yield platform_attribute_item

                    platform_item['attribute_id'] = { '__ref': f"{platform_attribute_item.__tablename__}:{platform_attribute_item.get('id')}" }
                yield platform_item
            yield release_item
        yield region_item
            
    user_review_key = next((key for key in apollo_state['ROOT_QUERY'] if 'userReviewSearch' in key), None)
    if user_review_key:
        for user_review in [apollo_state[review_ref['__ref']] for review_ref in apollo_state['ROOT_QUERY'][user_review_key]['userReviews']]:
            user_review_item = UserReview()
            user_review_item['legacy_id'] = user_review.get('id')
            user_review_item['is_liked'] = user_review.get('liked')
            user_review_item['score'] = user_review.get('score')
            user_review_item['text'] = user_review.get('text')
            user_review_item['is_spoiler'] = user_review.get('isSpoiler')
            user_review_item['is_private'] = user_review.get('isPrivate')
            user_review_item['publish_date'] = user_review.get('createdAt')
            user_review_item['modify_date'] = user_review.get('updatedAt')

            user_review_item['object_id'] = { '__ref': f"{object_item.__tablename__}:{object_item.get('id')}" }
            object_item['referrers'].append(f"{user_review_item.__tablename__}:{user_review_item.get('id')}")

            user_review_platform_ref = user_review.get('platformId')
            if user_review_platform_ref:
                existing_platform = self.postgres_find_by_legacy_id(table=Attribute.__tablename__, id=user_review_platform_ref, fields=['id'], only_first=True)
                if existing_platform:
                    user_review_item['platform_id'] = existing_platform[0]
                else:
                    attribute_data = apollo_state["Attribute:" + str(user_review_platform_ref)]
                    if attribute_data:
                        attribute_item = Attribute(referrers=[f"{user_review_item.__tablename__}:{user_review_item.get('id')}"])
                        attribute_item['legacy_id'] = attribute_data.get('id')
                        attribute_item['name'] = attribute_data.get('name')
                        attribute_item['slug'] = attribute_data.get('slug')
                        attribute_item['short_name'] = attribute_data.get('shortName')

                        yield attribute_item
                        user_review_item['platform_id'] = { '__ref': f"{attribute_item.__tablename__}:{attribute_item.get('id')}" }

            for tag in [apollo_state[tag_ref['__ref']] for tag_ref in user_review.get(next((key for key in user_review if 'userReviewObjectFeedback' in key), None))]:
                review_tag_item = ReviewTag()
                review_tag_item['is_positive'] = tag.get('isPositive')
                
                review_tag_item['review_id'] = { '__ref': f"{user_review_item.__tablename__}:{user_review_item.get('id')}" }
                user_review_item['referrers'].append(f"{review_tag_item.__tablename__}:{review_tag_item.get('id')}")

                existing_tag_object = self.postgres_find_by_legacy_id(table=Attribute.__tablename__, id=tag.get('id'), fields=['id'], only_first=True)
                if existing_tag_object:
                    review_tag_item['attribute_id'] = existing_tag_object[0]
                else:
                    tag_object_item = Attribute(referrers=[f"{review_tag_item.__tablename__}:{review_tag_item.get('id')}"])
                    tag_object_item['legacy_id'] = tag.get('id')
                    tag_object_item['name'] = tag.get('name')

                    yield tag_object_item
                    review_tag_item['attribute_id'] = { '__ref': f"{tag_object_item.__tablename__}:{tag_object_item.get('id')}" }
                yield review_tag_item

            user_data = apollo_state[user_review['user']['__ref']]
            existing_user = self.postgres_find_by_legacy_id(table=User.__tablename__, id=user_data.get('id'), fields=['id'], only_first=True)
            if existing_user:
                user_review_item['user_id'] = existing_user[0]
            else:
                user_item = User(referrers=[f"{user_review_item.__tablename__}:{user_review_item.get('id')}"])
                user_item['legacy_id'] = user_data.get('id')
                user_item['name'] = user_data.get('name')
                user_item['nickname'] = user_data.get('nickname')

                user_avatar_ref = user_data.get('avatarImageUrl')
                if user_avatar_ref:
                    user_avatar_item = Image(referrers=[f"{user_item.__tablename__}:{user_item.get('id')}"])
                    user_avatar_item['url'] = user_avatar_ref

                    yield user_avatar_item
                    user_item['avatar_id'] = { '__ref': f"{user_avatar_item.__tablename__}:{user_avatar_item.get('id')}" }

                user_configuration_ref = user_data.get('playlistSettings')
                if user_configuration_ref:
                    user_configuration_item = UserConfiguration()
                    user_configuration_item['privacy'] = user_configuration_ref.get('privacy', '').lower()
                    user_configuration_item['user_id'] = { '__ref': f"{user_item.__tablename__}:{user_item.get('id')}" }

                    yield user_configuration_item
                    user_item['referrers'].append(f"{user_configuration_item.__tablename__}:{user_configuration_item.get('id')}")

                yield user_item
                user_review_item['user_id'] = { '__ref': f"{user_item.__tablename__}:{user_item.get('id')}" }
            yield user_review_item

    gallery_regex = re.compile(r"imageGallery:{.*}")
    object_gallery_key = next((key for key in object_data if gallery_regex.search(key)), None)
    if object_gallery_key:
        gallery_item = Gallery(referrers=[f"{object_item.__tablename__}:{object_item.get('id')}"])

        for image in [apollo_state[img_ref['__ref']] for img_ref in object_data[object_gallery_key]['images']]:
            image_connection_item = ImageConnection()
            image_connection_item['gallery_id'] = { '__ref': f"{gallery_item.__tablename__}:{gallery_item.get('id')}" }
            gallery_item['referrers'].append(f"{image_connection_item.__tablename__}:{image_connection_item.get('id')}")

            existing_image = self.postgres_find_by_legacy_id(table=Image.__tablename__, id=image.get('id'), fields=['id'], only_first=True)
            if existing_image:
                image_connection_item['image_id'] = existing_image[0]
            else:
                image_item = Image(referrers=[f"{image_connection_item.__tablename__}:{image_connection_item.get('id')}"])
                image_item['legacy_id'] = image.get('id')
                image_item['caption'] = image.get('caption')
                image_item['url'] = image.get('url')

                yield image_item
                image_connection_item['image_id'] = { '__ref': f"{image_item.__tablename__}:{image_item.get('id')}" }
            yield image_connection_item
        yield gallery_item
        object_item['gallery_id'] = { '__ref': f"{gallery_item.__tablename__}:{gallery_item.get('id')}" }

    # legacy_wiki_key = next((key for key in apollo_state['ROOT_QUERY'] if 'wiki' in key), None)
    # if legacy_wiki_key:
    #     wiki_item = WikiObject()

    #     yield scrapy.Request(url="https://www.ign.com/wikis/" + object_data.get('wikiSlug'), callback=self.parse_wiki_page, cb_kwargs={ 'wiki_item': wiki_item, 'recursion_level': recursion_level })
    #     object_item['wiki'] = wiki_item.get('id')

    yield object_item

    # if legacy_wiki_key:
    #     wiki_data = apollo_state[apollo_state['ROOT_QUERY'][legacy_wiki_key]['__ref']]
    #     wiki_item = ObjectWiki(wiki_data)

    #     # Map image dimensions: 256 x 256
    #     # Smallest map magnification value: 254
    #     # Map zoom to coordinate increment: x2
    #     map_objects = {}
    #     for map in wiki_data.get('maps'):
    #         object_key = 'MapObject:' + map.get('objectSlug')
    #         if object_key not in map_objects:
    #             map_objects[object_key] = MapObject(apollo_state[object_key], { 'maps': [] })

    #         map_item = Map({ **map, **apollo_state[f'Map:{map.get('objectSlug')}:{map.get('mapSlug')}'] })
    #         map_objects[object_key]['maps'].append(map_item.get('id'))
    #         yield map_item

    #     for object_key in map_objects:
    #         map_object_item = map_objects[object_key]
    #         wiki_item['map_objects'].append(map_object_item.get('id'))
    #         yield map_object_item

    #     for nav in wiki_data.get('navigation'):
    #         nav_item = WikiNavigation(nav)
    #         wiki_item['navigation'].append(nav_item.get('id'))
    #         yield nav_item

    #     object_item['wiki'] = wiki_item.get('id')
    #     yield wiki_item

def parse_modern_content(self, page_json_data, modern_content_key, content_item = None, recursion_level = 0):
    if content_item is None:
        content_item = Content()

    apollo_state = page_json_data['props']['apolloState']
    modern_content_data = apollo_state[modern_content_key]

    content_item['legacy_id'] = modern_content_data.get('id')
    content_item['url'] = modern_content_data.get('url')
    content_item['slug'] = modern_content_data.get('slug')
    content_item['type'] = modern_content_data.get('type')
    content_item['vertical'] = modern_content_data.get('vertical')
    content_item['title'] = modern_content_data.get('title')
    content_item['subtitle'] = modern_content_data.get('subtitle')
    content_item['feed_title'] = modern_content_data.get('feedTitle')
    content_item['excerpt'] = modern_content_data.get('excerpt')
    content_item['description'] = modern_content_data.get('description') # possibly unnecessary
    content_item['state'] = modern_content_data.get('state')
    content_item['publish_date'] = modern_content_data.get('publishDate')
    content_item['modify_date'] = modern_content_data.get('updatedAt')
    content_item['events'] = modern_content_data.get('events')

    header_image = modern_content_data.get('headerImageUrl')
    if header_image:
        header_image_item = Image(referrers=[f"{content_item.__tablename__}:{content_item.get('id')}"])
        header_image_item['url'] = header_image
        yield header_image_item
        content_item['header_image_id'] = { '__ref': f"{header_image_item.__tablename__}:{header_image_item.get('id')}" }

    feed_image = modern_content_data.get('feedImage')
    if feed_image:
        feed_image_item = Image(referrers=[f"{content_item.__tablename__}:{content_item.get('id')}"])
        feed_image_item['url'] = feed_image.get('url')
        yield feed_image_item
        content_item['feed_image_id'] = { '__ref': f"{feed_image_item.__tablename__}:{feed_image_item.get('id')}" }
        
    for user_data in [apollo_state[contributor_ref.get('__ref')] for contributor_ref in modern_content_data.get('contributorsOrBylines', [])]:
        contributor_item = Contributor()
        
        contributor_item['content_id'] = { '__ref': f"{content_item.__tablename__}:{content_item.get('id')}" }
        content_item['referrers'].append(f"{contributor_item.__tablename__}:{contributor_item.get('id')}")

        existing_user = self.postgres_find_by_legacy_id(table=User.__tablename__, id=user_data.get('id'), fields=['id'], only_first=True)
        if existing_user:
            contributor_item['user_id'] = existing_user[0]
        else:
            author_item = Author()

            user_item = User(referrers=[f"{author_item.__tablename__}:{author_item.get('id')}", f"{contributor_item.__tablename__}:{contributor_item.get('id')}"])
            user_item['legacy_id'] = user_data.get('id')
            user_item['name'] = user_data.get('name')
            user_item['nickname'] = user_data.get('nickname')

            user_avatar = user_data.get('avatarImageUrl')
            if user_avatar:
                user_avatar_item = Image(referrers=[f"{user_item.__tablename__}:{user_item.get('id')}"])
                user_avatar_item['url'] = user_avatar

                yield user_avatar_item
                user_item['avatar_id'] = { '__ref': f"{user_avatar_item.__tablename__}:{user_avatar_item.get('id')}" }
            yield user_item

            author_item['user_id'] = { '__ref': f"{user_item.__tablename__}:{user_item.get('id')}" }

            yield scrapy.Request(url="https://www.ign.com/person/" + user_data.get('nickname'), callback=self.parse_contributor_page, cb_kwargs={ 'author_item': author_item, 'recursion_level': recursion_level })

            contributor_item['user_id'] = { '__ref': f"{user_item.__tablename__}:{user_item.get('id')}" }

        yield contributor_item
        
    brand_ref = modern_content_data.get('brand')

    if brand_ref:
        brand_data = None
        if brand_ref.get('__ref'):
            brand_data = apollo_state[brand_ref.get('__ref')]
        elif brand_ref.get('__typename'):
            brand_search = (lambda obj, target : obj.get('name') == target)
            brand_data = next((apollo_state[key] for key in apollo_state.keys() if key.startswith('Brand:') and brand_search(apollo_state[key], brand_ref.get('name'))), brand_ref)

        if brand_data.get('id'):
            self.cursor.execute("SELECT id FROM brands WHERE legacy_id = %s LIMIT 1;", (brand_data.get('id'),))
        else:
            self.cursor.execute("SELECT id FROM brands WHERE name = %s LIMIT 1;", (brand_data.get('name'),))

        existing_brand = self.cursor.fetchone()
        if existing_brand:
            content_item['brand_id'] = existing_brand[0]
        else:
            brand_item = Brand(referrers=[f"{content_item.__tablename__}:{content_item.get('id')}"])
            brand_item['legacy_id'] = brand_data.get('id')
            brand_item['slug'] = brand_data.get('slug')
            brand_item['name'] = brand_data.get('name')
            brand_item['logo_light'] = brand_data.get('logoLight')
            brand_item['logo_dark'] = brand_data.get('logoDark')

            yield brand_item
            content_item['brand_id'] = { '__ref': f"{brand_item.__tablename__}:{brand_item.get('id')}" }
            
    primary_object_ref = modern_content_data.get('primaryObject')
    object_regex = re.compile(r"objects\({.*}\)")
    object_key = next((key for key in modern_content_data if object_regex.search(key)), None)

    if object_key:
        for object_ref in modern_content_data.get(object_key):
            object_connection_item = ObjectConnection()
            object_connection_item['content_id'] = { '__ref': f"{content_item.__tablename__}:{content_item.get('id')}" }
            content_item['referrers'].append(f"{object_connection_item.__tablename__}:{object_connection_item.get('id')}")

            object_data = apollo_state[object_ref.get('__ref')]
            existing_object = self.postgres_find_by_legacy_id(table=Object.__tablename__, id=object_data.get('id'), fields=['id'], only_first=True)

            if existing_object:
                object_connection_item['object_id'] = existing_object[0]
                if primary_object_ref and primary_object_ref.get('__ref') == object_ref.get('__ref'):
                    content_item['primary_object_id'] = existing_object[0]
            else:
                object_item = Object(referrers=[f"{object_connection_item.__tablename__}:{object_connection_item.get('id')}"])
                # Bug: Some entries fail to get stored if they have a primary_object_id
                if primary_object_ref and primary_object_ref.get('__ref') == object_ref.get('__ref'):
                    content_item['primary_object_id'] = { '__ref': f"{object_item.__tablename__}:{object_item.get('id')}" }
                    object_item['referrers'].append(f"{content_item.__tablename__}:{content_item.get('id')}")

                yield scrapy.Request(url="https://www.ign.com" + object_data.get('url'), callback=self.parse_object_page, cb_kwargs={ 'object_item': object_item, 'recursion_level': recursion_level })
                object_connection_item['object_id'] = { '__ref': f"{object_item.__tablename__}:{object_item.get('id')}" }
            yield object_connection_item
                    

    content_category_ref = modern_content_data.get('contentCategory')
    if content_category_ref:
        content_category_data = None
        if content_category_ref.get('__ref'):
            content_category_data = apollo_state[content_category_ref.get('__ref')]
        elif content_category_ref.get('__typename'):
            content_category_data = content_category_ref

        if content_category_data.get('id'):
            self.cursor.execute("SELECT id FROM content_categories WHERE legacy_id = %s LIMIT 1;", (content_category_data.get('id'),))
        else:
            self.cursor.execute("SELECT id FROM content_categories WHERE name = %s LIMIT 1;", (content_category_data.get('name'),))

        existing_category = self.cursor.fetchone()
        if existing_category:
            content_item['category_id'] = existing_category[0]
        else:
            content_category_item = ContentCategory(referrers=[f"{content_item.__tablename__}:{content_item.get('id')}"])
            content_category_item['legacy_id'] = content_category_data.get('id')
            content_category_item['name'] = content_category_data.get('name')

            yield content_category_item
            content_item['category_id'] = { '__ref': f"{content_category_item.__tablename__}:{content_category_item.get('id')}" }
            
    for nested_attribute in modern_content_data.get('attributes', []):
        attribute_data = nested_attribute.get('attribute')

        attribute_connection = ContentAttributeConnection()
        attribute_connection['content_id'] = { '__ref': f"{content_item.__tablename__}:{content_item.get('id')}" }
        content_item['referrers'].append(f"{attribute_connection.__tablename__}:{attribute_connection.get('id')}")

        self.cursor.execute("""
            SELECT typed_attributes.id
            FROM typed_attributes
            INNER JOIN attributes
                ON typed_attributes.attribute_id = attributes.id
            WHERE typed_attributes.type = %s AND attributes.name = %s
            LIMIT 1;
        """, (nested_attribute.get('type'), attribute_data.get('name'),))
        existing_attribute = self.cursor.fetchone()
        if existing_attribute:
            attribute_connection['attribute_id'] = existing_attribute[0]
        else:
            typed_attribute_item = TypedAttribute(referrers=[f"{attribute_connection.__tablename__}:{attribute_connection.get('id')}"])
            typed_attribute_item['type'] = nested_attribute.get('type')

            attribute_item = Attribute(referrers=[f"{typed_attribute_item.__tablename__}:{typed_attribute_item.get('id')}"])
            attribute_item['name'] = attribute_data.get('name')

            attribute_obj_search = (lambda obj, target : obj.get('name') == target)
            attribute_obj = next((apollo_state[key] for key in apollo_state.keys() if key.startswith('Attribute:') and attribute_obj_search(apollo_state[key], attribute_data.get('name'))), None)
            if attribute_obj:
                attribute_item['short_name'] = attribute_obj.get('shortName')
                attribute_item['slug'] = attribute_obj.get('slug')
                attribute_item['legacy_id'] = attribute_obj.get('id')
            yield attribute_item

            typed_attribute_item['attribute_id'] = { '__ref': f"{attribute_item.__tablename__}:{attribute_item.get('id')}" }
            yield typed_attribute_item

            attribute_connection['attribute_id'] = { '__ref': f"{typed_attribute_item.__tablename__}:{typed_attribute_item.get('id')}" }
        yield attribute_connection

    yield content_item

def parse_wiki_page():
    pass