'''
Unit test methods
'''
import unittest
import requests_mock
import mocks.ssm
from unittest import mock
from unittest.mock import MagicMock
from pydroneapi import PyDroneAPI


class TestGithub(unittest.TestCase):
    '''
    Define test cases for Github methods
    '''
    def setUp(self):
        self.drone = PyDroneAPI(
            drone_host='https://mydrone.example.com',
            token='abc',
            repo='bellyjay1005/foo-bar-app',
        )
        self.token = 'abc'
        self.header = {"Authorization": f'Bearer {self.token}'}

    def test_synchronize_repository(self):
        with mock.patch('requests.post') as drone_res:
            drone_res.return_value.id = 123
            status_id = self.drone.synchronize_repository()
            assert status_id

    def test_activate_repository(self):
        with mock.patch('requests.post') as drone_res_post:
            drone_res_post.return_value.json.return_value = {'slug': 'bellyjay1005/foo-bar-app'}
            res = self.drone.activate_repository()
            assert res['slug'] == 'bellyjay1005/foo-bar-app'

    def test_start_new_build(self):
        with mock.patch('requests.post') as drone_res_post:
            drone_res_post.return_value.json.return_value = {'status': 'success'}
            status = self.drone.start_new_build()
            assert status == 'success' or 'failure' or 'pending'

    def test_start_new_build_with_custom_params(self):
        parameters = {
            "AUTOSCALING_EVENT": "TERMINATING",
            "CLUSTER_NAME": "test-cluster",
            "NODE_INSTANCE_ID": "i-1234567890",
            "NODE_IP": "10.0.0.0",
            "NODE_AZ": "us-east-1a"
        }
        with mock.patch('requests.post') as drone_res_post:
            drone_res_post.return_value.json.return_value = {
                "status": "pending",
                "params": {
                    "AUTOSCALING_EVENT": "TERMINATING",
                    "CLUSTER_NAME": "test-cluster",
                    "NODE_INSTANCE_ID": "i-1234567890",
                    "NODE_IP": "10.0.0.0",
                    "node_az": "us-east-1a"
                }
            }
            response = self.drone.start_new_build_with_custom_parameters(params=parameters)
            assert response['status'] == 'success' or 'failure' or 'pending'
            assert response['params']['AUTOSCALING_EVENT'] == parameters['AUTOSCALING_EVENT']
            assert response['params']['AUTOSCALING_EVENT'] != parameters['NODE_AZ']

    def test_get_build_numbers(self):
        with mock.patch('requests.get') as drone_res_get:
            drone_res_get.return_value.json.return_value = [
                {
                    'id': 100000,
                    'number': 1234
                },
                {
                    'id': 200000,
                    'number': 5678
                },
                {
                    'id': 300000,
                    'number': 9012
                }
            ]
            builds = self.drone.get_build_numbers()
            assert builds[0] == 1234
            assert builds[1] == 5678
            assert builds[2] == 9012

    def test_get_build_response_status(self):
        with mock.patch('requests.get') as drone_res_get:
            drone_res_get.return_value.status_code = 200
            response = self.drone.get_build_response_status(build_number=[123])
            assert response == 200
        with mock.patch('requests.get') as drone_res_get:
            drone_res_get.return_value.status_code = 400
            response = self.drone.get_build_response_status(build_number=[123])
            assert response != 200

    def test_get_build_content(self):
        with mock.patch('requests.get') as drone_res_get:
            drone_res_get.return_value.status_code.json.return_value = {'status': 'success'}
            response_body = self.drone.get_build_content(build_number=[123])
            assert response_body['status'] == 'success' or 'failure' or 'pending'

    def test_get_drone_build_status(self):
        with mock.patch('requests.get') as drone_res_get:
            drone_res_get.return_value.status_code.json.return_value = {'status': 'success'}
            response_body = self.drone.get_drone_build_status(build_number=[123])
            assert response_body['status'] == 'success' or 'failure' or 'pending'

    def test_stop_drone_build_job(self):
        with mock.patch('requests.delete') as drone_res_delete:
            drone_res_delete.return_value = True
            status = self.drone.stop_drone_build_job(build_number=[123])
            assert status is True
            drone_res_delete.return_value = False
            status = self.drone.stop_drone_build_job(build_number=[456])
            assert status is True

    def test_restart_drone_build_job(self):
        with mock.patch('requests.post') as drone_res_post:
            drone_res_post.return_value.json.return_value = {'id': 100000, 'number': 1234}
            res = self.drone.restart_drone_build_job(build_number=[1234])
            assert res['id'] == 100000

    def tearDown(self):
        self.drone
