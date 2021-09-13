import boto3
import botocore
import config
from botocore.stub import Stubber

def get_parameter(get_parameter_response, expected_params):
    client = boto3.client(
        'ssm',
        'us-east-2',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=config.AWS_SESSION_TOKEN,
    )
    stubber = Stubber(client)
    stubber.add_response('get_parameter', get_parameter_response, expected_params)
    stubber.activate()
    return client
