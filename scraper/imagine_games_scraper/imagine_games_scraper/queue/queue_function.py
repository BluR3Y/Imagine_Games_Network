import psycopg2
from redis import Redis
import json
from imagine_games_scraper.queue import activeQueue

def queue_function(item_key):

    dict_item = dict(json.loads(activeQueue.redis_connection.get(item_key)))
    obj = dict_item.get('obj')

    attribute_keys = []
    attribute_values = []
    print('******************************** ', dict_item.get('referrers'), obj)
    for key, value in obj.items():
        attribute_keys.append(key)
        if isinstance(value, dict) and value.get('__ref', None):
            key_parts = value.get('__ref').split(':')
            activeQueue.postgres_cursor.execute("SELECT COUNT(*) FROM %s WHERE id = '%s' LIMIT 1;" % (key_parts[0], key_parts[1]))
            if not activeQueue.postgres_cursor.fetchone()[0]:
                return
            
            attribute_values.append(f"'{key_parts[1]}'")
        else:
            # attribute_values.append(str(value))
            attribute_values.append(postgres_type_format(value))

    item_key_parts = item_key.split(':')
    # print('********************* ', item_key_parts, attribute_keys, attribute_values)
    insert_query = "INSERT INTO %s (%s) VALUES (%s);" % (item_key_parts[0] ,','.join(attribute_keys), ','.join(attribute_values))
    activeQueue.postgres_cursor.execute(insert_query)
    activeQueue.postgres_connection.commit()

    referrers = dict_item.get('referrers')
    if referrers:
        for referrer in referrers:
            activeQueue.enqueue_task(referrer)

    activeQueue.redis_connection.delete(item_key)
# Last Here
def postgres_type_format(value):
    if isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, list):
        return "{%s}" % (','.join(map(postgres_type_format, value)))
    elif value is None:
        return "null"
    else:
        return str(value)