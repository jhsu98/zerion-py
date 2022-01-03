import pytest
from fixtures import dfa_client
import time

def test_describeResources(dfa_client):
    result = dfa_client.describeResources()
    assert len(result) > 0

def test_describeResource(dfa_client):
    result = dfa_client.describeResource('Dataflows')
    assert isinstance(result, dict)

def test_Dataflows_GET(dfa_client):
    dfa_client.Dataflows('GET')

def test_Dataflow_GET(dfa_client):
    result = dfa_client.Dataflows('GET')
    if len(result.response) > 0:
        dataflow = result.response[0]
        result = dfa_client.Dataflows('GET', dataflow['_id'])

        assert result.status_code == 200

def test_invalid_method(dfa_client):
    with pytest.raises(ValueError):
        dfa_client.Dataflows('PATCH')