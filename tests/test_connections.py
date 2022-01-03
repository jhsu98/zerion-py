import zerionAPI
from zerionAPI import IFB, DFA
import pytest
from pprint import pprint
from fixtures import server, client_key, client_secret, ifb_client, dfa_client

def test_ifb_fixture(ifb_client):
    assert isinstance(ifb_client, zerionAPI.ifb.IFB)

def test_dfa_fixture(dfa_client):
    assert isinstance(dfa_client, zerionAPI.dfa.DFA)

def test_import_API():
    with pytest.raises(ImportError):
        from zerionAPI import API

def test_empty_IFB():
    with pytest.raises(TypeError):
        IFB()

def test_empty_DFA():
    with pytest.raises(TypeError):
        DFA()

def test_bad_IFB():
    with pytest.raises(TypeError):
        api = IFB('','',None)

def test_bad_DFA():
    with pytest.raises(TypeError):
        api = DFA('','',None)

def test_invalid_IFB():
    api = IFB('','','')
    assert api.getAccessToken() is None

def test_invalid_DFA():
    api = DFA('','','')
    assert api.getAccessToken() is None

def test_IFB(server, client_key, client_secret):
    api = IFB(server, client_key, client_secret)
    assert isinstance(api, zerionAPI.ifb.IFB)

def test_DFA(server, client_key, client_secret):
    api = DFA(server, client_key, client_secret)
    assert isinstance(api, zerionAPI.dfa.DFA)

def test_response_str(ifb_client):
    result = ifb_client.Profiles('GET')
    print(result)
    pprint(result)
    assert f'{result}' == '200'

def test_getParams(ifb_client):
    assert ifb_client.getParams() is not None

def test_getAccessToken(ifb_client):
    assert ifb_client.getVersion() is not None

def test_getAccessTokenExpiration(ifb_client):
    assert ifb_client.getAccessTokenExpiration() is not None

def test_getApiCount(ifb_client):
    assert ifb_client.getApiCount() is not None

def test_getLastExecution(ifb_client):
    assert ifb_client.getLastExecution() is None

def test_getStartTime(ifb_client):
    assert ifb_client.getStartTime() is not None

def test_getApiLifetime(ifb_client):
    assert ifb_client.getApiLifetime() is not None

def test_call(ifb_client):
    with pytest.raises(TypeError):
        ifb_client.call()

def test_call_invalid_method(ifb_client):
    with pytest.raises(ValueError):
        ifb_client.call('PATCH','')

def test_call_post_method(ifb_client):
    result = ifb_client.call('POST', 'https://reqbin.com/echo/post/json')

def test_abstract_methods():
    from zerionAPI.api import API
    class Example(API):
        def describeResources(self):
            raise NotImplementedError

        def describeResource(self, resource):
            raise NotImplementedError
