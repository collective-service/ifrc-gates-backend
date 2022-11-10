from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_STATIC
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'
    file_overwrite = True
    querystring_auth = False


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_MEDIA
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    querystring_auth = True
