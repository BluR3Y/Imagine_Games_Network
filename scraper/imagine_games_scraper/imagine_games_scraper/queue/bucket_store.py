import requests
import boto3

from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
from psycopg2.extensions import AsIs

from imagine_games_scraper.queue import activeQueue

settings = get_project_settings()

image_extensions = ['jpg','jpeg','png','gif','tiff','webp','svg']
video_extensions = ['mp4','avi','mov','wmv','flv','mkv','webm','mpeg','3gp','m4v']

# Set up the S3 client
s3 = boto3.client('s3',
    aws_access_key_id=settings.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=settings.get('AWS_SECRET_KEY'),
    region_name=settings.get('AWS_REGION'),
    endpoint_url=settings.get('AWS_ENDPOINT')
)
bucket_name = settings.get('AWS_BUCKET')

def bucket_store(item_key):
    table, id = item_key.split(':')
    activeQueue.postgres_cursor.execute("SELECT legacy_url FROM %s WHERE id = %s;", (AsIs(table), id,))
    
    url = activeQueue.postgres_cursor.fetchone()[0]
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = path.split('.')[-1]

    stream = None
    if extension in image_extensions:
        stream = False
    elif extension in video_extensions:
        stream = True
    else:
        raise Exception("Invalid media type")
    
    media_content = download_file(url, stream)
    media_key = path[1:]

    upload_file(media_content, media_key)

    activeQueue.postgres_cursor.execute("UPDATE %s SET key = %s WHERE id = %s;", (AsIs(table), media_key, id,))
    activeQueue.postgres_connection.commit()

def download_file(url, stream = False):
    # Send a GET request to the URL
    response = requests.get(url, stream=stream)

    # Check if the request was successful
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Failed to download media:", response.status_code)

def upload_file(content, key):
    # Upload the file to S3 bucket
    s3.put_object(
        Body=content,
        Bucket=bucket_name,
        Key=key
    )