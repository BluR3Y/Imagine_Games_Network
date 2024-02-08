import scrapy

class Catalog(scrapy.Item):
    slug = scrapy.Field()
    content = scrapy.Field()
    items = scrapy.Field()

    def __init__(self, catalog_data=None, manual_assignments=None, *args, **kwargs):
        super(Catalog, self).__init__(*args, **kwargs)

        self['slug'] = manual_assignments.get('slug', catalog_data.get('slug'))
        self['content'] = manual_assignments.get('content', catalog_data.get('content'))
        self['items'] = manual_assignments.get('items', catalog_data.get('items'))

class CommerceDeal(scrapy.Item):
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
    cover = scrapy.Field()

    def __init__(self, deal_data=None, manual_assignments=None, *args, **kwargs):
        super(CommerceDeal, self).__init__(*args, **kwargs)

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
        self['coupon_code'] = manual_assignments.get('coupon_code', deal_data.get('coupon_code'))
        self['sponsor_disclosure'] = manual_assignments.get('sponsor_disclosure', deal_data.get('sponsor_disclosure'))
        self['is_large'] = manual_assignments.get('is_large', deal_data.get('is_large'))
        self['region_code'] = manual_assignments.get('region_code', deal_data.get('region_code'))
        self['cover'] = manual_assignments.get('cover', deal_data.get('cover'))

class Slideshow(scrapy.Item):
    slug = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()

    def __init__(self, slideshow_data=None, manual_assignments=None, *args, **kwargs):
        super(Slideshow, self).__init__(*args, **kwargs)

        self['slug'] = manual_assignments.get('slug', slideshow_data.get('slug'))
        self['content'] = manual_assignments.get('content', slideshow_data.get('content'))
        self['images'] = manual_assignments.get('images', slideshow_data.get('images'))

class Image(scrapy.Item):
    legacy_id = scrapy.Field()
    url = scrapy.Field()
    caption = scrapy.Field()
    embargo_date = scrapy.Field()

    def __init__(self, image_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', image_data.get('id', None))
        self['url'] = manual_assignments.get('url', image_data.get('url', None))
        self['caption'] = manual_assignments.get('caption', image_data.get('caption', None))
        self['embargo_date'] = manual_assignments.get('embargoDate', image_data.get('embargoDate', None))

class Brand(scrapy.Item):
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()

    def __init__(self, brand_data = {}, manual_assignments = {}, *args, **kwargs):
        super(Brand, self).__init__(*args, **kwargs)

        self['legacy_id'] = manual_assignments.get('id', brand_data.get('id', None))
        self['name'] = manual_assignments.get('name', brand_data.get('name', None))
        self['slug'] = manual_assignments.get('slug', brand_data.get('slug', None))