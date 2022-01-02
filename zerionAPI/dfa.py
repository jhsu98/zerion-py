import re
import inspect
import urllib.parse
from .api import API

class DFA(API):
    def __init__(self, server, client_key, client_secret, params={}):
        super().__init__(server, client_key, client_secret, params)

        self.__server = server
        self.__client_key = client_key
        self.__client_secret = client_secret
        self.__isQA = True if params.get('isQA',False) or self.__server == 'qatest' or re.search(r'^support', self.__server) else False
        self.__host = f'https://{"qa-dataflownode" if self.__isQA else "dataflownode"}.zerionsoftware.com/zcrypt/v1.0'

    __allowed_methods = {
        'Dataflows': ('POST', 'GET', 'PUT', 'DELETE'),
        'RecordSets': ('POST', 'GET', 'PUT', 'DELETE'),
        'RecordSetLinks': ('POST'),
        'Records': ('DELETE'),
        'Webhooks': ('POST', 'GET', 'PUT', 'DELETE'),
        'Actions': ('POST', 'GET', 'PUT', 'DELETE')
    }

    def __methodCheck(self, method, resource):
        if method.upper() not in self.__allowed_methods[resource]:
            raise ValueError(f'The "{method}" is not allowed for {resource}')
    
    def __completeURI(self, resource, resource_id=None, params=None):
        resource = f'{self.__host}/{resource}'

        if resource_id is not None:
            resource += f'/{resource_id}'
        
        if params is not None and len(params) > 0:
            resource += '?'

            for key in params:
                if params[key] is not None:
                    resource += f'{key}={urllib.parse.quote(params[key])}&'

        return resource

    def Dataflows(self, method, dataflow_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows'
        request = self.__completeURI(request, dataflow_id, params)
        return API.call(self, method, request, body)

    def RecordSets(self, method, dataflow_id, recordset_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows/{dataflow_id}/recordsets'
        request = self.__completeURI(request, recordset_id, params)
        return API.call(self, method, request, body)

    def RecordSetLinks(self, method, dataflow_id, recordset_id, destination_recordset_id):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows/{dataflow_id}/recordsets/{recordset_id}/postactions'
        request = self.__completeURI(request)
        return API.call(self, method, request, {'actionType': 'pushrs', 'actionOutputRecordSetId': destination_recordset_id})

    def Records(self, method, dataflow_id, recordset_id, record_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows/{dataflow_id}/recordsets/{recordset_id}/records'
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    def Webhooks(self, method, dataflow_id, recordset_id, webhook_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows/{dataflow_id}/recordsets/{recordset_id}/webhooks'
        request = self.__completeURI(request, webhook_id, params)
        return API.call(self, method, request, body)

    def Actions(self, method, dataflow_id, recordset_id, action_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'dataflows/{dataflow_id}/recordsets/{recordset_id}/postactions'
        request = self.__completeURI(request, action_id, params)
        return API.call(self, method, request, body)