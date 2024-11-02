import json
import requests
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


def lambda_handler(event, context):
    if event["path"] == "/presignedurl":
        return s3_presigned_url(event, context)
    # elif event["path"] == "/uploadfile":
    #     return s3_doc_uploader(event, context)

# # PUT /uploadfile
# def s3_doc_uploader(event, context):
#     """
#     event contains two parameters: 
#     - content: content of the file
#     - presigned_url: url generated to upload the data
#     """
#     LOGGER.info(f"event received: {event}")
    
#     try:
#         response = requests.put()
#     except ClientError as e:
#         LOGGER.error(e)
#         return e
#     else:
#         LOGGER.info(response)
#         return request_successful(message="File upload successful")

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
        response = client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response