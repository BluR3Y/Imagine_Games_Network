import scrapy
from uuid import uuid4

class Item(scrapy.Item):
    id = scrapy.Field()
    referrers = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(self, *args, **kwargs)

        self['id'] = str(uuid4())
        self['referrers'] = kwargs.get('referrers', [])

    def to_dict(self):
        result = { 'referrers': self['referrers'], 'obj': {} }
        for key, value in self.items():
            if not key.startswith('__') and key != 'referrers':
                result['obj'][key] = value
        return result