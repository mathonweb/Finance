import configparser

import boto3
from botocore.exceptions import ClientError

from .logger import logger


def get_file(file_name):
    try:
        config = configparser.ConfigParser()
        config.read_file(open('config.ini'))

        s3 = boto3.client('s3')
        s3.download_file(config['DEFAULT']['bucket_name'], file_name, file_name)
        return file_name
    except Exception as e:
        logger.error(e)
        raise Exception("File in S3 is not present: " + str(file_name))


def send_file(file_name):
    try:
        config = configparser.ConfigParser()
        config.read_file(open('config.ini'))

        s3 = boto3.client('s3')
        response = s3.upload_file(file_name, config['DEFAULT']['bucket_name'], file_name)
        logger.info("S3 upload file response: " + str(response))
    except ClientError as e:
        logger.error(e)
        return False
    return True
