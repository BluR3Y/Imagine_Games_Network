from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from scrapy.utils.project import get_project_settings

# def queue_function(item):
#     settings = get_project_settings()
#     # Establish a connection to the Postgres database
#     db_conn = psycopg2.connect(
#         database = settings.get('POSTGRES_DATABASE'),
#         user = settings.get('POSTGRES_ACCESS_USER'),
#         password = settings.get('POSTGRES_ACCESS_PASSWORD'),
#         host = settings.get('POSTGRES_HOST'),
#         port = settings.get('POSTGRES_PORT')
#     )
#     if not db_conn.closed:
#         print('Connection to postgres database established successfully.')
#     else:
#         raise Retry('Error occured while attempting to connect to postgres database.')
#     db_cursor = db_conn.cursor()
    
#     dict_item = dict(item)
#     attribute_keys = []
#     attribute_values = []
#     print('************************* tablename: ', item.__tablename__)
#     for key, value in dict_item.items():
#         attribute_keys.append(key)
#         if type(value) == dict:
#             print('************************* value: ', value)
#             table_name = value.get('__tablename__')
#             ref = value.get('__ref')

#             search_query = "SELECT COUNT(*) FROM %s WHERE id = '%s' LIMIT 1;" % (table_name, ref)
#             db_cursor.execute(search_query)
#             user_exists = db_cursor.fetchone()[0]

#             if not user_exists:
#                 raise Retry("Referenced item with an id of %s from table %s does not exist" % (ref, table_name))
            
#             attribute_values.append(f"'{ref}'")
#         else:
#             attribute_values.append(f"'{value}'" if type(value) == str else value)

#     insert_query = "INSERT INTO %s (%s) VALUES (%s);" % (item.__tablename__ ,','.join(attribute_keys), ','.join(attribute_values))
#     db_cursor.execute(insert_query)

#     db_conn.commit()
#     db_cursor.close()

def queue_function(item):
    print('************************** marker')

    settings = get_project_settings()
    # Define the SQLAlchemy engine
    engine = create_engine('postgresql://%s:%s@%s:%s/%s' % (settings.get('POSTGRES_ACCESS_USER'), quote_plus(settings.get('POSTGRES_ACCESS_PASSWORD')), settings.get('POSTGRES_HOST'), settings.get('POSTGRES_PORT'), settings.get('POSTGRES_DATABASE')))

    # Create a sessionmaker bound to the engine
    session = sessionmaker(bind=engine)

    # Create a session
    session = session()

    try:
        session.add(item)
    except:
        raise Exception('Error occured while attempting to insert entry to postgres.')

    # Commit the session to persist the changes to the database
    session.commit()

    # Close the session
    session.close()
    