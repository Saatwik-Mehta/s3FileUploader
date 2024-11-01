import json
import os
import boto3
from botocore.exceptions import ClientError
import logging

from common import request_successful
client = boto3.client('s3')
S3_BUCKET = os.getenv("s3_bucket")
REGION = os.getenv("REGION")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def s3_doc_uploader(event, context):
    LOGGER.info(f"event received: {event}")
    file_name = event.get("file_name")
    s3_bucket = event.get("s3_bucket")
    key = event.get("object_name")
    if key is None:
        key = os.path.basename(file_name)
    try:
        response = client.upload_file(file_name, s3_bucket, key)
    except ClientError as e:
        LOGGER.error(e)
        return e
    else:
        LOGGER.info(response)
        return request_successful(message="File upload successful")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def s3_presigned_url(event, context):
    LOGGER.info(f"event received: {event}")
    presigned_url = create_presigned_url(bucket_name=S3_BUCKET, object_name=event["file_name"])
    return request_successful(presigned_url)
