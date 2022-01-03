"""
To use pytest, rename this file `fixtures.py` and add in values below
"""
from zerionAPI import IFB, DFA
import pytest

@pytest.fixture
def server():
    return ''

@pytest.fixture
def client_key():
    return ''

@pytest.fixture
def client_secret():
    return ''

@pytest.fixture
def ifb_client():
    return IFB('', '', '')

@pytest.fixture
def dfa_client():
    return DFA('', '', '')