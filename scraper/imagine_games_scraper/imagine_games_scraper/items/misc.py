import scrapy
from uuid import uuid4

class Image(scrapy.Item):
    id = scrapy.Field()
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    caption = scrapy.Field()
    embargo_date = scrapy.Field()

    def __init__(self, image_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', image_data.get('id'))
        self['url'] = manual_assignments.get('url', image_data.get('url'))
        self['caption'] = manual_assignments.get('caption', image_data.get('caption'))
        self['embargo_date'] = manual_assignments.get('embargoDate', image_data.get('embargoDate'))

# class Brand(scrapy.Item):
#     id = scrapy.Field()
#     legacy_id = scrapy.Field()
#     name = scrapy.Field()
#     slug = scrapy.Field()

#     def __init__(self, brand_data = {}, manual_assignments = {}, *args, **kwargs):
#         super(Brand, self).__init__(*args, **kwargs)

#         self['id'] = str(uuid4())
#         self['legacy_id'] = manual_assignments.get('id', brand_data.get('id'))
#         self['name'] = manual_assignments.get('name', brand_data.get('name'))
#         self['slug'] = manual_assignments.get('slug', brand_data.get('slug'))

class Slideshow(scrapy.Item):
    id = scrapy.Field()
    slug = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()

    def __init__(self, slideshow_data={}, manual_assignments={}, *args, **kwargs):
        super(Slideshow, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['slug'] = manual_assignments.get('slug', slideshow_data.get('slug'))
        self['content'] = manual_assignments.get('content', slideshow_data.get('content'))
        self['images'] = manual_assignments.get('images', slideshow_data.get('images'))

class Catalog(scrapy.Item):
    id = scrapy.Field()
    slug = scrapy.Field()
    content = scrapy.Field()
    items = scrapy.Field()

    def __init__(self, catalog_data={}, manual_assignments={}, *args, **kwargs):
        super(Catalog, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['slug'] = manual_assignments.get('slug', catalog_data.get('slug'))
        self['content'] = manual_assignments.get('content', catalog_data.get('content'))
        self['items'] = manual_assignments.get('items', catalog_data.get('items'))

class Poll(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content = scrapy.Field()
    answers = scrapy.Field()
    configuration = scrapy.Field()
    image = scrapy.Field()
    voters = scrapy.Field()

    def __init__(self, poll_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Poll, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('legacy_id', poll_data.get('id'))
        self['content'] = manual_assignments.get('content', poll_data.get('content'))
        self['answers'] = manual_assignments.get('answers', poll_data.get('answers'))
        self['configuration'] = manual_assignments.get('configuration', poll_data.get('config'))
        self['image'] = manual_assignments.get('image', poll_data.get('image'))
        self['voters'] = manual_assignments.get('voters', poll_data.get('voters'))

class PollAnswer(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    answer = scrapy.Field()
    votes = scrapy.Field()

    def __init__(self, answer_data = {}, manual_assignments = {}, *args, **kwargs):
        super(PollAnswer, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('legacy_id', answer_data.get('id'))
        self['answer'] = manual_assignments.get('', answer_data.get('answer'))
        self['votes'] = manual_assignments.get('', answer_data.get('votes'))

class PollConfiguration(scrapy.Item):
    id = scrapy.Field()
    require_authentication = scrapy.Field()
    require_authentication_for_results = scrapy.Field()
    multi_choice = scrapy.Field()
    auto_display_results = scrapy.Field()

    def __init__(self, configuration_data = {}, manual_assignments = {}, *args, **kwargs):
        super(PollConfiguration, self).__init__(*args, **kwargs)
    
        self['id'] = str(uuid4())
        self['require_authentication'] = manual_assignments.get('require_authentication', configuration_data.get('requireAuthenticated'))
        self['require_authentication_for_results'] = manual_assignments.get('require_authentication_for_results', configuration_data.get('requireAuthenticatedForResults'))
        self['multi_choice'] = manual_assignments.get('multi_choice', configuration_data.get('multiChoice'))
        self['auto_display_results'] = manual_assignments.get('auto_display_results', configuration_data.get('autoDisplayResults'))

class CommerceDeal(scrapy.Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    vendor = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    discount = scrapy.Field()
    coupon_code = scrapy.Field()
    sponsor_disclosure = scrapy.Field()
    is_large = scrapy.Field()
    region_code = scrapy.Field()
    up_votes = scrapy.Field()
    cover = scrapy.Field()

    def __init__(self, deal_data = {}, manual_assignments = {}, *args, **kwargs):
        super(CommerceDeal, self).__init__(*args, **kwargs)

        self['id'] = str(uuid4())
        self['legacy_id'] = manual_assignments.get('id', deal_data.get('id'))
        self['url'] = manual_assignments.get('url', deal_data.get('url'))
        self['title'] = manual_assignments.get('title', deal_data.get('title'))
        self['description'] = manual_assignments.get('description', deal_data.get('description'))
        self['brand'] = manual_assignments.get('brand', deal_data.get('brand'))
        self['model'] = manual_assignments.get('model', deal_data.get('model'))
        self['vendor'] = manual_assignments.get('vendor', deal_data.get('vendor'))
        self['price'] = manual_assignments.get('price', deal_data.get('price'))
        self['msrp'] = manual_assignments.get('msrp', deal_data.get('msrp'))
        self['discount'] = manual_assignments.get('discount', deal_data.get('discount'))
        self['coupon_code'] = manual_assignments.get('coupon_code', deal_data.get('couponCode'))
        self['sponsor_disclosure'] = manual_assignments.get('sponsor_disclosure', deal_data.get('sponsorDisclosure'))
        self['is_large'] = manual_assignments.get('is_large', deal_data.get('large'))
        self['region_code'] = manual_assignments.get('region_code', deal_data.get('regionCode'))
        self['up_votes'] = manual_assignments.get('up_votes', deal_data.get('upVotes'))
        self['cover'] = manual_assignments.get('cover', deal_data['image']['url'] if deal_data.get('image') else None)