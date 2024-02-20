import requests
import boto3

from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
from imagine_games_scraper.alchemy.models.misc import Image

settings = get_project_settings()

# Set up the S3 client
s3 = boto3.client('s3',
    aws_access_key_id=settings.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=settings.get('AWS_SECRET_KEY'),
    region_name=settings.get('AWS_REGION'),
    endpoint_url=settings.get('AWS_ENDPOINT')
)
bucket_name = settings.get('AWS_BUCKET')

def parse_image(self, **kwargs):
    # Download the image from the URL
    response = requests.get(kwargs.get('legacy_url'))
    if response.status_code == 200:
        parsed_url = urlparse(kwargs.get('legacy_url'))
        image_data = response.content
        image_key = parsed_url.path[1:]

        s3.put_object(
            Body=image_data,
            Bucket=bucket_name,
            Key=image_key
        )
        image_item = Image()
        image_item.legacy_id = kwargs.get('legacy_id')
        image_item.legacy_url = kwargs.get("legacy_url")
        # image_item.url = settings.get('AWS_ENDPOINT') + bucket_name + parsed_url.path
        image_item.url = f"{settings.get('AWS_ENDPOINT')}/{bucket_name}/{image_key}"
        image_item.link = kwargs.get('link')
        image_item.caption = kwargs.get('caption')
        image_item.embargo_date = kwargs.get('embargo_date')

        self.session.add(image_item)
        self.session.commit()
        return image_item.id
    else:
        print("Failed to download image")