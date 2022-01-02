import re
import urllib.parse
import inspect
from .api import API

class IFB(API):
    def __init__(self, server, client_key, client_secret, params={}):
        super().__init__(server, client_key, client_secret, params)
        self.__server = server
        self.__client_key = client_key
        self.__client_secret = client_secret
        self.__isQA = True if params.get('isQA',False) or self.__server == 'loadapp' or re.search(r'^support', self.__server) else False
        self.__version = params.get('version', 8.0)
        self.__host = f'https://{"qa-api" if self.__isQA else "api"}.iformbuilder.com/exzact/api/v{str(self.__version).replace(".","")}/{self.__server}'
        self.__rate_limit_retry = params.get('rate_limit_retry',False)

    __allowed_methods = {
        'Profiles': ('POST', 'GET', 'PUT'),
        'CompanyInfo': ('GET', 'PUT'),
        'Users': ('POST', 'GET', 'PUT', 'DELETE'),
        'UserPageAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'UserRecordAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'UserGroups': ('POST', 'GET', 'PUT', 'DELETE'),
        'UserGroupUserAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'UserGroupPageAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'Pages': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageFeeds': ('GET'),
        'PageLocalizations': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageUserAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageRecordAssignments': ('GET', 'DELETE'),
        'PageEndpoints': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageEmailAlerts': ('POST', 'GET', 'DELETE'),
        'PageTriggerPost': ('POST'),
        'PageShares': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageDynamicAttributes': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageGroups': ('POST', 'GET', 'PUT', 'DELETE'),
        'PageGroupAssignments': ('POST', 'GET', 'DELETE'),
        'PageGroupUserAssignments': ('POST', 'GET', 'PUT', 'DELETE'),
        'Elements': ('POST', 'GET', 'PUT', 'DELETE', 'COPY'),
        'ElementLocalizations': ('POST', 'GET', 'PUT', 'DELETE'),
        'ElementDynamicAttributes': ('POST', 'GET', 'PUT', 'DELETE'),
        'OptionLists': ('POST', 'GET', 'PUT', 'DELETE', 'COPY'),
        'Options': ('POST', 'GET', 'PUT', 'DELETE'),
        'OptionLocalizations': ('POST', 'GET', 'PUT', 'DELETE'),
        'Records': ('POST', 'GET', 'PUT', 'DELETE', 'COPY'),
        'RecordAssignments': ('POST', 'GET', 'DELETE'),
        'Notifications': ('POST'),
        'PrivateMedia': ('GET'),
        'DeviceLicenses': ('GET')
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

    """
    Profile Resources: https://iformbuilder80.docs.apiary.io/reference/profile-resource
    """
    def Profiles(self, method, profile_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles'
        request = self.__completeURI(request, profile_id, params)
        return API.call(self, method, request, body)

    def CompanyInfo(self, method, profile_id, *, body=None):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/company_info'
        request = self.__completeURI(request)
        return API.call(self, method, request, body)

    """
    User Resources: https://iformbuilder80.docs.apiary.io/reference/user-resource
    """
    def Users(self, method, profile_id, user_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/users'
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def UserPageAssignments(self, method, profile_id, user_id, page_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/users/{user_id}/page_assignments'
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    def UserRecordAssignments(self, method, profile_id, user_id, record_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/users/{user_id}/record_assignments'
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    """
    User Group Resources: https://iformbuilder80.docs.apiary.io/reference/user-group-resource
    """
    def UserGroups(self, method, profile_id, usergroup_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/user_groups'
        request = self.__completeURI(request, usergroup_id, params)
        return API.call(self, method, request, body)

    def UserGroupUserAssignments(self, method, profile_id, usergroup_id, user_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/user_groups/{usergroup_id}/users'
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def UserGroupPageAssignments(self, method, profile_id, usergroup_id, page_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/user_groups/{usergroup_id}/page_assignments'
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    """
    Page Resources: https://iformbuilder80.docs.apiary.io/reference/page-resource
    """
    def Pages(self, method, profile_id, page_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages'
        request = self.__completeURI(request, page_id, params)
        return API.call(self, method, request, body)

    def PageFeeds(self, method, profile_id, page_id, *, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/feed'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request)

    def PageLocalizations(self, method, profile_id, page_id, language_code=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/localizations'
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    def PageUserAssignments(self, method, profile_id, page_id, user_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/assignments'
        request = self.__completeURI(request, user_id, params)
        return API.call(self, method, request, body)

    def PageRecordAssignments(self, method, profile_id, page_id):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/record_assignments'
        request = self.__completeURI(request)
        return API.call(self, method, request)
    
    def PageEndpoints(self, method, profile_id, page_id, endpoint_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/http_callbacks'
        request = self.__completeURI(request, endpoint_id, params)
        return API.call(self, method, request, body)

    def PageEmailAlerts(self, method, profile_id, page_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/email_alerts'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageTriggerPost(self, method, profile_id, page_id, *, body=None):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/trigger_posts'
        request = self.__completeURI(request)
        return API.call(self, method, request, body)

    def PageShares(self, method, profile_id, page_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/shared_page'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageDynamicAttributes(self, method, profile_id, page_id, dynamic_attribute=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/dynamic_attributes'
        request = self.__completeURI(request, dynamic_attribute, params)
        return API.call(self, method, request, body)

    """
    Page Group Resources: https://iformbuilder80.docs.apiary.io/reference/page-group-resource
    """
    def PageGroups(self, method, profile_id, pagegroup_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/page_groups'
        request = self.__completeURI(request, pagegroup_id, params)
        return API.call(self, method, request, body)

    def PageGroupAssignments(self, method, profile_id, pagegroup_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/page_groups/{pagegroup_id}/pages'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PageGroupUserAssignments(self, method, profile_id, pagegroup_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/page_groups/{pagegroup_id}/assignments'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    """
    Elements Resources: https://iformbuilder80.docs.apiary.io/reference/element-resource
    """
    def Elements(self, method, profile_id, page_id, element_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/elements'
        request = self.__completeURI(request, element_id, params)
        return API.call(self, method, request, body)

    def ElementLocalizations(self, method, profile_id, page_id, element_id, language_code=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/elements/{element_id}/localizations'
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    def ElementDynamicAttributes(self, method, profile_id, page_id, element_id, dynamic_attribute=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/elements/{element_id}/dynamic_attributes'
        request = self.__completeURI(request, dynamic_attribute, params)
        return API.call(self, method, request, body)

    """
    Option Lists Resources: https://iformbuilder80.docs.apiary.io/reference/optionlist-resource
    """
    def OptionLists(self, method, profile_id, optionlist_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/optionlists'
        request = self.__completeURI(request, optionlist_id, params)
        return API.call(self, method, request, body)

    def Options(self, method, profile_id, optionlist_id, option_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/optionlists/{optionlist_id}/options'
        request = self.__completeURI(request, option_id, params)
        return API.call(self, method, request, body)

    def OptionLocalizations(self, method, profile_id, optionlist_id, option_id, language_code=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/optionlists/{optionlist_id}/options/{option_id}/localizations'
        request = self.__completeURI(request, language_code, params)
        return API.call(self, method, request, body)

    """
    Record Resources: https://iformbuilder80.docs.apiary.io/reference/record-resource
    """
    def Records(self, method, profile_id, page_id, record_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/records'
        request = self.__completeURI(request, record_id, params)
        return API.call(self, method, request, body)

    def RecordAssignments(self, method, profile_id, page_id, record_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/pages/{page_id}/records/{record_id}/assignments'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    """
    Notification Resources: https://iformbuilder80.docs.apiary.io/reference/notification-resource
    """

    def Notifications(self, method, profile_id, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/notifications'
        request = self.__completeURI(request, None, params)
        return API.call(self, method, request, body)

    def PrivateMedia(self, method, profile_id, media_url=None):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/media'
        request = self.__completeURI(request)
        return API.call(self, method, request, {'URL': media_url})

    """
    Device License Resources: https://iformbuilder80.docs.apiary.io/reference/device-license-resource
    """

    def DeviceLicenses(self, method, profile_id, license_id=None, *, body=None, params={}):
        self.__methodCheck(method, inspect.currentframe().f_code.co_name)
        request = f'profiles/{profile_id}/licenses'
        return API.call(self, method, request, body)