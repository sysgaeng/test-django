import json

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_id, aws_access_key_id=None, aws_secret_access_key=None):
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name="ap-northeast-2",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise e
        else:
            raise e
    else:
        return json.loads(get_secret_value_response["SecretString"])
