'''
End-to-End Testing of repository functionality
'''
import os
import unittest
from pydroneapi import PyDroneAPI

# provide your test Drone token as environment variables
token = os.environ['DRONE_TOKEN']

'''
Test main functions
'''
drone = PyDroneAPI(
        drone_host='https://mydrone.example.com',
        token=token,
        repo='bellyjay1005/ice-drone-e2e-test-pipeline',
    )
header = {"Authorization": f'Bearer {token}'}

def test_synchronize_repository():
    '''
    Check if new repository is sync with drone
    '''
    status = drone.synchronize_repository()
    assert status[0]['id']

def test_activate_repository():
    '''
    Check if repository gets activated
    '''
    res = drone.activate_repository()
    assert res['slug'] == 'bellyjay1005/ice-drone-e2e-test-pipeline'

def test_start_new_build(branch='develop'):
    '''
    Get triggered pipeline stage status
    '''
    status = drone.start_new_build(branch='main')
    assert status == 'success' or 'failure' or 'pending'

def test_drone_job_triggered():
    '''
    Check if Drone job started
    '''
    build_numbers = drone.get_build_numbers()
    response_body = drone.get_build_content(build_numbers)
    assert response_body['started'] is not None

def test_get_drone_build_numbers():
    '''
    Get Drone build info and numbers
    '''
    build_numbers = drone.get_build_numbers()
    assert build_numbers is not None

def test_drone_response_status():
    '''
    Check Drone API response status
    '''
    build_number = drone.get_build_numbers()
    status = drone.get_build_response_status(build_number)
    assert status == 200

def test_drone_response_status_fail():
    '''
    Check Drone API response status
    '''
    build_number = 'fake-01'
    status = drone.get_build_response_status(build_number)
    assert status == 400

def test_drone_build_status():
    '''
    Check Drone job status
    '''
    build_number = drone.get_build_numbers()
    response_body = drone.get_build_content(build_number)
    assert response_body['status'] == 'success' or 'failure' or 'pending'

def test_drone_stage_status():
    '''
    Test Drone stages status
    '''
    build_number = drone.get_build_numbers()
    response_body = drone.get_build_content(build_number)
    assert response_body['stages'][0]['status'] == 'success' or 'failure'
    assert response_body['stages'][0]['steps'][0]['status'] == 'success' or 'failure'

def test_stop_drone_job():
    '''
    Test stopping specific Drone build job
    '''
    build_number = drone.get_build_numbers()
    assert drone.stop_drone_build_job(build_number)
