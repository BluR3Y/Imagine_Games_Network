import scrapy
from imagine_games_scraper.items.base_item import Item

class Attribute(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    short_name = scrapy.Field()
    slug = scrapy.Field()

    __tablename__ = 'attributes'

    def __init__(self, *args, **kwargs):
        super(Attribute, self).__init__(*args, **kwargs)

        



class TypedAttribute(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    type = scrapy.Field()
    attribute_id = scrapy.Field()

    __tablename__ = 'typed_attributes'

    def __init__(self, *args, **kwargs):
        super(TypedAttribute, self).__init__(*args, **kwargs)

        


class PollConfiguration(Item):
    id = scrapy.Field()
    require_authentication = scrapy.Field()
    require_authentication_for_results = scrapy.Field()
    multi_choice = scrapy.Field()
    auto_display_results = scrapy.Field()

    __tablename__ = 'poll_configurations'

    def __init__(self, *args, **kwargs):
        super(PollConfiguration, self).__init__(*args, **kwargs)

        



class Poll(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    content_id = scrapy.Field()
    configuration_id = scrapy.Field()
    image_id = scrapy.Field()
    voters = scrapy.Field()

    __tablename__ = 'polls'

    def __init__(self, *args, **kwargs):
        super(Poll, self).__init__(*args, **kwargs)

        

class PollAnswer(Item):
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    poll_id = scrapy.Field()
    answer = scrapy.Field()
    votes = scrapy.Field()

    __tablename__ = 'poll_answers'

    def __init__(self, *args, **kwargs):
        super(PollAnswer, self).__init__(*args, **kwargs)

        

class Catalog(Item):
    id = scrapy.Field()
    content_id = scrapy.Field()

    __tablename__ = 'catalogs'

    def __init__(self, *args, **kwargs):
        super(Catalog, self).__init__(*args, **kwargs)

        


class CommerceDeal(Item):
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
    cover_id = scrapy.Field()

    __tablename__ = 'commerce_deals'

    def __init__(self, *args, **kwargs):
        super(CommerceDeal, self).__init__(*args, **kwargs)

        



class DealConnection(Item):
    id = scrapy.Field()
    deal_id = scrapy.Field()
    catalog_id = scrapy.Field()

    __tablename__ = 'deal_connections'

    def __init__(self, *args, **kwargs):
        super(Catalog, self).__init__(*args, **kwargs)

        