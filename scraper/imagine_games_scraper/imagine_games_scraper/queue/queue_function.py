import json
from imagine_games_scraper.queue import activeQueue
from psycopg2.extras import Json
from psycopg2.extensions import AsIs

def queue_function(item_key):
    stored_item = activeQueue.redis_connection.get(item_key)
    if not stored_item:
        print(f"Item with key '{item_key}' does not exist in redis store")
        return
    
    dict_item = json.loads(stored_item)
    obj = dict_item.get('obj')

    attribute_keys = []
    attribute_values = []
    for key, value in obj.items():
        attribute_keys.append(key)
        if isinstance(value, dict):
            if value.get('__ref', None):
                key_parts = value.get('__ref').split(':')
                activeQueue.postgres_cursor.execute("SELECT COUNT(*) FROM %s WHERE id = '%s' LIMIT 1;" % (key_parts[0], key_parts[1]))
                if not activeQueue.postgres_cursor.fetchone()[0]:
                    print(f"Item in table '{key_parts[0]}' with the key '{key_parts[1]}' does not exist in postgres database")
                    return
                
                attribute_values.append(key_parts[1])
            elif value.get('__static', None):
                attribute_values.append(AsIs(value.get('__static')))
            else:
                attribute_values.append(Json(value))
        else:
            attribute_values.append(value)
                
    item_key_parts = item_key.split(':')
    # print('********************* ', item_key_parts, attribute_keys, attribute_values)
    insert_query = "INSERT INTO %s (%s) VALUES (%s);" % (item_key_parts[0], ','.join(attribute_keys), ','.join(['%s'] * len(attribute_values)))

    activeQueue.postgres_cursor.execute(insert_query, attribute_values)
    activeQueue.postgres_connection.commit()

    referrers = dict_item.get('referrers')
    for referrer in referrers:
        if activeQueue.redis_connection.get(referrer):
            activeQueue.enqueue_task(referrer)
        else:
            print(f"Item with the key {referrer} can't be found in the redis database")

    activeQueue.redis_connection.delete(item_key)