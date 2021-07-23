import boto3

from config import bucket_name


def get_file(file_name):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, file_name, file_name)
        return file_name
    except Exception as e:
        raise Exception("File in S3 is not present: " + str(file_name))