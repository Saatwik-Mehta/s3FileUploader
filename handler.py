import json
import os
import boto3
from botocore.exceptions import ClientError
import logging
client = boto3.client('s3')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOGGER.INFO)

def s3_doc_uploader(event, context):
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
        return {"status": "200", "message": "Object Created Successfully"}
