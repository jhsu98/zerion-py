import re
import inspect
import urllib.parse
import json
from pprint import pprint
from .api import API, Response

class DFA(API):
    def __init__(self, server, client_key, client_secret, params={}):
        super().__init__(server, client_key, client_secret, params)

        self.__server = server
        self.__isQA = True if params.get('isQA',False) or self.__server == 'qatest' or re.search(r'^support', self.__server) else False
        self.__host = f'https://{"qa-dataflownode" if self.__isQA else "dataflownode"}.zerionsoftware.com/zcrypt/v1.0'

    __resources = {
        'Dataflows': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'dataflows'
        },
        'DataflowCount': {
            'Methods': ('GET'),
            'URI': 'dataflows/count'
        },
        'DataflowExport': {
            'Methods': ('POST'),
            'URI': 'dataflows/%s/export'
        },
        'DataflowImport': {
            'Methods': ('POST'),
            'URI': 'dataflows/import'
        },
        'RecordSets': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'dataflows/%s/recordsets'
        },
        'RecordSetLinks': {
            'Methods': ('POST'),
            'URI': 'dataflows/%s/recordsets/%s/postactions'
        },
        'Records': {
            'Methods': ('GET', 'DELETE'),
            'URI': 'dataflows/%s/recordsets/%s/records'
        },
        'Webhooks': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'dataflows/%s/recordsets/%s/webhooks'
        },
        'Actions': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'dataflows/%s/recordsets/%s/postactions'
        },
        'ActionErrors': {
            'Methods': ('GET'),
            'URI': 'dataflows/%s/recordsets/%s/postactions/%s/errors'
        },
        'RerunActionErrors': {
            'Methods': ('POST'),
            'URI': 'dataflows/%s/recordsets/%s/postactions/%s/rerunErrorMessages'
        },
        'Events': {
            'Methods': ('GET'),
            'URI': 'dataflows/%s/recordsets/%s/events'
        }
    }

    def __methodCheck(self, method, resource):
        if method.upper() not in self.__resources[resource]['Methods']:
            raise ValueError(f'The "{method}" is not allowed for {resource}')
    
    def __getResourceURI(self, resource):
        return self.__resources[resource]['URI']

    def __completeURI(self, resource, resource_id=None, params=None):
        resource = f'{self.__host}/{resource}'

        if resource_id is not None:
            resource += f'/{resource_id}'
        
        if params is not None and len(params) > 0:

            for key in params:
                if params[key] is not None:
                    resource += f'/{key}/{params[key]}'

        return resource

    def describeResources(self):
        return self.__resources.keys()

    def describeResource(self, resource):
        return self.__resources.get(resource, 'Resource is not defined')

    """
    Dataflow Resources: https://gnosiz.docs.apiary.io/reference/dataflows-resource
    """
    def Dataflows(self, method, dataflow_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = f'{self.__getResourceURI(resource)}'
        request = self.__completeURI(request, dataflow_id, params)
        print(request)
        return API.call(self, method, request, body)

    def DataflowCount(self, dataflow_name):
        resource = inspect.currentframe().f_code.co_name
        request = f'{self.__getResourceURI(resource)}'
        request = self.__completeURI(request, dataflow_name, {})
        print(request)
        return API.call(self, 'GET', request)

    def DataflowExport(self, dataflow_id):
        resource = inspect.currentframe().f_code.co_name
        request = f'{self.__getResourceURI(resource)}' % dataflow_id
        request = self.__completeURI(request, None, {})
        return API.call(self, 'POST', request, {})

    def DataflowImport(self, body):
        resource = inspect.currentframe().f_code.co_name
        request = f'{self.__getResourceURI(resource)}'
        request = self.__completeURI(request, None, {})
        body = {
            'requestedServer': self.__host.split('/zcrypt')[0],
            'content': json.dumps(body)
        }
        return API.call(self, 'POST', request, body)

    def RecordSets(self, method, dataflow_id, recordset_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(inspect.currentframe().f_code.co_name) % dataflow_id
        request = self.__completeURI(request, recordset_id, params)
        print(request)
        return API.call(self, method, request, body)

    def RecordSetLinks(self, method, dataflow_id, recordset_id, destination_recordset_id):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id)
        request = self.__completeURI(request)
        return API.call(self, method, request, {'actionType': 'pushrs', 'actionOutputRecordSetId': destination_recordset_id})

    def Records(self, method, dataflow_id, recordset_id, record_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id)
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    def Webhooks(self, method, dataflow_id, recordset_id, webhook_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id)
        request = self.__completeURI(request, webhook_id, params)
        return API.call(self, method, request, body)

    def Actions(self, method, dataflow_id, recordset_id, action_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id)
        request = self.__completeURI(request, action_id, params)
        return API.call(self, method, request, body)

    def ActionErrors(self, method, dataflow_id, recordset_id, action_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id, action_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def RerunActionErrors(self, method, dataflow_id, recordset_id, action_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id, action_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def Events(self, method, dataflow_id, recordset_id, event_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (dataflow_id, recordset_id)
        request = self.__completeURI(request, event_id, params)
        return API.call(self, method, request, body)