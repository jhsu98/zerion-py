import re
import urllib.parse
import inspect
from .api import API

class IFB(API):
    def __init__(self, server, client_key, client_secret, params={}):
        super().__init__(server, client_key, client_secret, params)
        self.__server = server
        self.__isQA = True if params.get('isQA',False) or self.__server == 'loadapp' or re.search(r'^support', self.__server) else False
        self.__version = params.get('version', 8.0)
        self.__region = params.get('region', 'us')
        self.__rate_limit_retry = params.get('rate_limit_retry',False)
        self.__host = f'https://{self.__region+"-api" if self.__region != "us" else "api"}.iformbuilder.com/exzact/api/v{str(self.__version).replace(".","")}/{self.__server}'

    __resources = {
        'Profiles': {
            'Methods': ('POST', 'GET', 'PUT'),
            'URI': 'profiles'
        },
        'CompanyInfo': {
            'Methods': ('GET', 'PUT'),
            'URI': 'profiles/%s/company_info'
        },
        'Users': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/users'
        },
        'UserPageAssignments': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/users/%s/page_assignments'
        },
        'UserRecordAssignments': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/users/%s/record_assignments'
        },
        'UserGroups': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/user_groups'
        },
        'UserGroupUserAssignments': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/user_groups/%s/users'
        },
        'UserGroupPageAssignments': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/user_groups%s/page_assignments'
        },
        'Pages': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages'
        },
        'PageFeeds': {
            'Methods': ('GET'),
            'URI': 'profiles/%s/pages/%s/feed'
        },
        'PageLocalizations': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/localizations'
        },
        'PageUserAssignments': 
        {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/assignments'
        },
        'PageRecordAssignments': {
            'Methods': ('GET', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/record_assignments'
        },
        'PageEndpoints': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/http_callbacks'
        },
        'PageEmailAlerts': {
            'Methods': ('POST', 'GET', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/email_alerts'
        },
        'PageTriggerPost': {
            'Methods': ('POST'),
            'URI': 'profiles/%s/pages/%s/trigger_posts'
        },
        'PageShares': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/shared_page'
        },
        'PageDynamicAttributes': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/dynamic_attributes'
        },
        'PageGroups': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/page_groups'
        },
        'PageGroupAssignments': {
            'Methods': ('POST', 'GET', 'DELETE'),
            'URI': 'profiles/%s/page_groups/%s/pages'
        },
        'PageGroupUserAssignments': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/page_groups/%s/assignments'
        },
        'Elements': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/elements'
        },
        'ElementLocalizations': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/elements/%s/localizations'
        },
        'ElementDynamicAttributes': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/elements/%s/dynamic_attributes'
        },
        'OptionLists': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE', 'COPY'),
            'URI': 'profiles/%s/optionlists'
        },
        'Options': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/optionlists/%s/options'
        },
        'OptionLocalizations': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/optionlists/%s/options/%s/localizations'
        },
        'Records': {
            'Methods': ('POST', 'GET', 'PUT', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/records'
        },
        'RecordAssignments': {
            'Methods': ('POST', 'GET', 'DELETE'),
            'URI': 'profiles/%s/pages/%s/records/%s/assignments'
        },
        'Notifications': {
            'Methods': ('POST'),
            'URI': 'profiles/%s/notifications'
        },
        'PrivateMedia': {
            'Methods': ('GET'),
            'URI': 'profiles/%s/media'
        },
        'DeviceLicenses': {
            'Methods': ('GET'),
            'URI': 'profiles/%s/licenses'
        }
    }

    def __methodCheck(self, method, resource):
        if method.upper() not in self.__resources[resource]['Methods']:
            raise ValueError(f'The "{method}" method is not allowed for {resource}')

    def __getResourceURI(self, resource):
        return self.__resources[resource]['URI']

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

    def describeResources(self):
        return self.__resources.keys()

    def describeResource(self, resource):
        return self.__resources.get(resource, 'Resource is not defined')

    def getVersion(self):
        return self.__version

    """
    Profile Resources: https://iformbuilder80.docs.apiary.io/reference/profile-resource
    """
    def Profiles(self, method, profile_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource)
        request = self.__completeURI(request, profile_id, params)
        return API.call(self, method, request, body)

    def CompanyInfo(self, method, profile_id, *, body=None):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request)
        return API.call(self, method, request, body)

    """
    User Resources: https://iformbuilder80.docs.apiary.io/reference/user-resource
    """
    def Users(self, method, profile_id, user_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def UserPageAssignments(self, method, profile_id, user_id, page_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, user_id)
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    def UserRecordAssignments(self, method, profile_id, user_id, record_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, user_id)
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    """
    User Group Resources: https://iformbuilder80.docs.apiary.io/reference/user-group-resource
    """
    def UserGroups(self, method, profile_id, usergroup_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, usergroup_id, params)
        return API.call(self, method, request, body)

    def UserGroupUserAssignments(self, method, profile_id, usergroup_id, user_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, usergroup_id)
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def UserGroupPageAssignments(self, method, profile_id, usergroup_id, page_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, usergroup_id)
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    """
    Page Resources: https://iformbuilder80.docs.apiary.io/reference/page-resource
    """
    def Pages(self, method, profile_id, page_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    def PageFeeds(self, method, profile_id, page_id, *, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request)

    def PageLocalizations(self, method, profile_id, page_id, language_code=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    def PageUserAssignments(self, method, profile_id, page_id, user_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def PageRecordAssignments(self, method, profile_id, page_id):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request)
        return API.call(self, method, request)
    
    def PageEndpoints(self, method, profile_id, page_id, endpoint_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, endpoint_id, params)
        return API.call(self, method, request, body)

    def PageEmailAlerts(self, method, profile_id, page_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageTriggerPost(self, method, profile_id, page_id, *, body=None):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request)
        return API.call(self, method, request, body)

    def PageShares(self, method, profile_id, page_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageDynamicAttributes(self, method, profile_id, page_id, dynamic_attribute=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, dynamic_attribute, params)
        return API.call(self, method, request, body)

    """
    Page Group Resources: https://iformbuilder80.docs.apiary.io/reference/page-group-resource
    """
    def PageGroups(self, method, profile_id, pagegroup_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, pagegroup_id, params)
        return API.call(self, method, request, body)

    def PageGroupAssignments(self, method, profile_id, pagegroup_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, pagegroup_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageGroupUserAssignments(self, method, profile_id, pagegroup_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, pagegroup_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    """
    Elements Resources: https://iformbuilder80.docs.apiary.io/reference/element-resource
    """
    def Elements(self, method, profile_id, page_id, element_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, element_id, params)
        return API.call(self, method, request, body)

    def ElementLocalizations(self, method, profile_id, page_id, element_id, language_code=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id, element_id)
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    def ElementDynamicAttributes(self, method, profile_id, page_id, element_id, dynamic_attribute=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id, element_id)
        request = self.__completeURI(request, dynamic_attribute, params)
        return API.call(self, method, request, body)

    """
    Option Lists Resources: https://iformbuilder80.docs.apiary.io/reference/optionlist-resource
    """
    def OptionLists(self, method, profile_id, optionlist_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, optionlist_id, params)
        return API.call(self, method, request, body)

    def Options(self, method, profile_id, optionlist_id, option_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, optionlist_id)
        request = self.__completeURI(request, option_id, params)
        return API.call(self, method, request, body)

    def OptionLocalizations(self, method, profile_id, optionlist_id, option_id, language_code=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, optionlist_id, option_id)
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    """
    Record Resources: https://iformbuilder80.docs.apiary.io/reference/record-resource
    """
    def Records(self, method, profile_id, page_id, record_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id)
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    def RecordAssignments(self, method, profile_id, page_id, record_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id, page_id, record_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    """
    Notification Resources: https://iformbuilder80.docs.apiary.io/reference/notification-resource
    """

    def Notifications(self, method, profile_id, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    """
    Private Media Resources: https://iformbuilder80.docs.apiary.io/reference/private-media-resource
    """
    def PrivateMedia(self, method, profile_id, media_url=None):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        request = self.__completeURI(request)
        return API.call(self, method, request, {'URL': media_url})

    """
    Device License Resources: https://iformbuilder80.docs.apiary.io/reference/device-license-resource
    """

    def DeviceLicenses(self, method, profile_id, license_id=None, *, body=None, params={}):
        resource = inspect.currentframe().f_code.co_name
        self.__methodCheck(method, resource)
        request = self.__getResourceURI(resource) % (profile_id)
        return API.call(self, method, request, body)