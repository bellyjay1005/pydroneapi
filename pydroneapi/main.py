'''
Drone API Helper Scripts
'''
import os
import sys
import logging
from urllib.parse import urlencode
import boto3
import requests

# Initialize LOGGER
LOGGER = logging.getLogger('droneApi-helper')
LOGGER.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

class PyDroneAPI():
    '''
    Manage Drone CI API
    '''
    def __init__(
            self,
            drone_host: str = None,
            token: str = None,
            ssm_token_name: str = None,
            repo: str = None,
        ):
        '''
        Declare API variable
        '''
        # If the token is not set, get token from AWS using boto3 client
        self.host = drone_host
        self.repository = repo
        self.region = os.environ['AWS_DEFAULT_REGION']
        self.token = token
        if token is None:
            self.ssm = boto3.client('ssm', region_name=self.region)
            self.token = self.get_secret(ssm_token_name)
        self.header = {"Authorization": f'Bearer {self.token}'}

    def get_secret(self, secret_name):
        '''
        Get secret from ssm
        '''
        LOGGER.info('Getting ssm token %s for auth', secret_name)
        secret = self.ssm.get_parameter(Name=secret_name, WithDecryption=True)
        return secret['Parameter']['Value']

    def synchronize_repository(self):
        '''
        Synchronize the currently authenticated user’s repository list
        '''
        LOGGER.info('Synchronizing latest repository list')
        sync_url = f'{self.host}/api/user/repos'
        response = requests.post(sync_url, headers=self.header)
        json_response = response.json()
        return json_response

    def activate_repository(self):
        '''
        Register a named repository with Drone
        '''
        LOGGER.info('Registering repository with Drone CI')
        activate_url = f'{self.host}/api/repos/{self.repository}'
        response = requests.post(activate_url, headers=self.header)
        json_response = response.json()
        return json_response

    def start_new_build(self, branch: str = 'main'):
        '''
        Create a build using the latest commit for the specified branch.
        '''
        LOGGER.info('Starting a new build using the latest commit')
        create_build_url = f'{self.host}/api/repos/{self.repository}/builds?branch={branch}'
        response = requests.post(create_build_url, headers=self.header)
        build_info = response.json()
        return build_info['status']

    def start_new_build_with_custom_parameters(self, params: dict, branch: str = 'main'):
        '''
        Create a build using the latest commit for the specified branch.

        - branch: target branch name
        - params: Dictionary of parameters available to pipeline steps as environment variables.
            example:
            {
                "AUTOSCALING_EVENT": "TERMINATING",
                "CLUSTER_NAME": "test-cluster",
                "NODE_INSTANCE_ID": "i-1234567890",
                "NODE_IP": "10.0.0.0",
                "node_az": "us-east-1a"
            }
        '''
        LOGGER.info('Starting a new build using the latest commit')
        url_string = urlencode(params)
        create_build_url = f'{self.host}/api/repos/{self.repository}/builds?branch={branch}&{url_string}' # pylint: disable=line-too-long
        response = requests.post(create_build_url, headers=self.header)
        build_info = response.json()
        return build_info

    def get_build_numbers(self):
        '''
        Get Drone build id from list of builds
        '''
        build_ids = []
        LOGGER.info('Getting list of deployed build ids')
        builds_url = f'{self.host}/api/repos/{self.repository}/builds'
        response = requests.get(builds_url, headers=self.header)
        LOGGER.info('Response - %s', response)
        json_response = response.json()
        for build in json_response:
            build_ids.append(build['number'])
        LOGGER.info('Got build id = %s', build_ids)
        return build_ids

    def get_build_response_status(self, build_number):
        '''
        Get API response status
        '''
        LOGGER.info('Getting build info for repository - %s', self.repository)
        get_url = f'{self.host}/api/repos/{self.repository}/builds/{build_number[0]}'
        response = requests.get(get_url, headers=self.header)
        return response.status_code

    def get_build_content(self, build_number):
        '''
        Get Drone build API response
        '''
        LOGGER.info('Getting build event contents for - %s', self.repository)
        content_url = f'{self.host}/api/repos/{self.repository}/builds/{build_number[0]}'
        response = requests.get(content_url, headers=self.header)
        return response.json()

    def get_drone_build_status(self, build_number):
        '''
        Get build info for a single build
        '''
        LOGGER.info('Getting build event info for build id =  %s', build_number[0])
        build_url = f'{self.host}/api/repos/{self.repository}/builds/{build_number[0]}'
        response = requests.get(build_url, headers=self.header)
        json_response = response.json()
        return json_response['status']

    def stop_drone_build_job(self, build_number):
        '''
        Stop specific Drone job
        '''
        LOGGER.info('Stopping target build job for build id =  %s', build_number[0])
        delete_url = f'{self.host}/api/repos/{self.repository}/builds/{build_number[0]}'
        requests.delete(delete_url, headers=self.header)
        return True

    def restart_drone_build_job(self, build_number):
        '''
        Restart specific Drone job
        '''
        LOGGER.info('Restarting target build job for build id =  %s', build_number[0])
        restart_url = f'{self.host}/api/repos/{self.repository}/builds/{build_number[0]}'
        response = requests.post(restart_url, headers=self.header)
        json_response = response.json()
        return json_response
