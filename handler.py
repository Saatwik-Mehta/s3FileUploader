import json
import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import logging

from common import request_successful
client = boto3.client('s3', config=Config(signature_version='s3v4'))
S3_BUCKET = os.getenv("FILE_BUCKET")
REGION = os.getenv("REGION")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    if event["path"] == "/presignedurl":
        return s3_presigned_url(event, context)

# POST /presignedurl
def s3_presigned_url(event, context):
    LOGGER.info(f"event received: {event}")
    body=json.loads(event["body"])
    presigned_url = create_presigned_url(bucket_name=S3_BUCKET, object_name=body["file_name"])
    return request_successful(presigned_url)

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response