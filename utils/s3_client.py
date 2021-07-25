import boto3
from botocore.exceptions import ClientError

from config import bucket_name
from utils.logger import logger


def get_file(file_name):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, file_name, file_name)
        return file_name
    except Exception as e:
        logger.error(e)
        raise Exception("File in S3 is not present: " + str(file_name))


def send_file(file_name):
    try:
        s3 = boto3.client('s3')
        response = s3.upload_file(file_name, bucket_name, file_name)
    except ClientError as e:
        logger.error(e)
        return False
    return True
