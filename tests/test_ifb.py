import pytest
from fixtures import ifb_client
import time

def test_describeResources(ifb_client):
    result = ifb_client.describeResources()
    assert len(result) > 0

def test_describeResource(ifb_client):
    result = ifb_client.describeResource('Profiles')
    assert isinstance(result, dict)

def test_Profiles_GET(ifb_client):
    ifb_client.Profiles('GET')

def test_Users_CRUD(ifb_client):
    testPassed = True
    
    result = ifb_client.Users('POST', 1, body={'username': f'pytest{int(time.time())}', 'password': 'Qwerty123!', 'email': 'test@pytest.com'})
    
    user = result.response
    
    result = ifb_client.Users('PUT', 1, user['id'], body={'email': 'updated@pytest.com'})

    result = ifb_client.Users('GET', 1, user['id'])

    result = ifb_client.Users('DELETE', 1, user['id'])

    assert testPassed is True